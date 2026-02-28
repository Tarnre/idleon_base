from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import struct
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PNG_SIG = b"\x89PNG\r\n\x1a\n"
LIME_HEADER = b"lime-asset-pack"


@dataclass(frozen=True)
class PngMeta:
    idx: int
    offset: int
    length: int
    width: int
    height: int
    sha256: str


def _gunzip_payload(pak_path: Path) -> bytes:
    raw = pak_path.read_bytes()
    if not raw.startswith(LIME_HEADER):
        raise ValueError("Not a lime-asset-pack file (missing header).")

    gz = raw[len(LIME_HEADER) :]
    if not gz.startswith(b"\x1f\x8b"):
        raise ValueError("Expected gzip stream immediately after header.")

    return gzip.decompress(gz)


def _split_pngs(payload: bytes) -> list[PngMeta]:
    metas: list[PngMeta] = []
    pos = 0
    idx = 0
    total = len(payload)

    while pos < total:
        if payload[pos : pos + 8] != PNG_SIG:
            nxt = payload.find(PNG_SIG, pos + 1)
            if nxt == -1:
                break
            pos = nxt
            continue

        start = pos
        pos += 8

        width = 0
        height = 0

        # Walk PNG chunks until IEND
        while True:
            if pos + 8 > total:
                raise EOFError("Truncated PNG chunk header")

            length = struct.unpack(">I", payload[pos : pos + 4])[0]
            ctype = payload[pos + 4 : pos + 8]
            pos += 8

            if pos + length + 4 > total:
                raise EOFError("Truncated PNG chunk data")

            chunk_data = payload[pos : pos + length]
            pos += length
            pos += 4  # CRC

            if ctype == b"IHDR":
                width = struct.unpack(">I", chunk_data[0:4])[0]
                height = struct.unpack(">I", chunk_data[4:8])[0]

            if ctype == b"IEND":
                break

        end = pos
        png_bytes = payload[start:end]
        sha = hashlib.sha256(png_bytes).hexdigest()

        metas.append(
            PngMeta(
                idx=idx,
                offset=start,
                length=end - start,
                width=width,
                height=height,
                sha256=sha,
            )
        )
        idx += 1

    return metas


def _print_summary(metas: list[PngMeta], top: int) -> None:
    by_size = Counter((m.width, m.height) for m in metas)
    uniq = len({m.sha256 for m in metas})
    squares = sum(c for (w, h), c in by_size.items() if w == h)

    print(f"Total PNGs: {len(metas)}")
    print(f"Unique SHA256: {uniq}  (dupes: {len(metas) - uniq})")
    print(f"Distinct sizes: {len(by_size)}")
    print(f"Square images: {squares}")

    print("\nTop sizes by count:")
    for (w, h), c in by_size.most_common(top):
        print(f"  {w}x{h}: {c}")


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def export_all(pak: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = _gunzip_payload(pak)
    metas = _split_pngs(payload)

    # Group by size, create directories, export, and per-size manifest
    per_size_rows: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)

    for m in metas:
        size_dir = out_dir / f"{m.width}x{m.height}"
        size_dir.mkdir(parents=True, exist_ok=True)

        fn = f"png_{m.idx:05d}_{m.width}x{m.height}.png"
        (size_dir / fn).write_bytes(payload[m.offset : m.offset + m.length])

        per_size_rows[(m.width, m.height)].append(
            {
                "idx": m.idx,
                "file": fn,
                "width": m.width,
                "height": m.height,
                "sha256": m.sha256,
                "length": m.length,
                "offset": m.offset,
            }
        )

    # Write per-size manifests
    for (w, h), rows in per_size_rows.items():
        size_dir = out_dir / f"{w}x{h}"
        _write_json(
            size_dir / "manifest.json",
            {
                "source_pak": str(pak),
                "export_dir": str(size_dir),
                "exported": len(rows),
                "filter": f"{w}x{h}",
                "images": rows,
            },
        )

    # Write a root summary manifest
    by_size = Counter((m.width, m.height) for m in metas)
    sizes = [
        {"size": f"{w}x{h}", "width": w, "height": h, "count": c}
        for (w, h), c in by_size.most_common()
    ]

    _write_json(
        out_dir / "manifest_sizes.json",
        {
            "source_pak": str(pak),
            "export_dir": str(out_dir),
            "total_pngs": len(metas),
            "distinct_sizes": len(by_size),
            "sizes": sizes,
        },
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pak", type=Path, help="Path to default.pak")
    ap.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Base output folder. Subfolders like 56x56/ will be created here.",
    )
    ap.add_argument(
        "--export-all",
        action="store_true",
        help="Export every PNG into <out>/<WxH>/ and write manifests.",
    )
    ap.add_argument(
        "--summary",
        action="store_true",
        help="Print a size summary (works with or without --export-all).",
    )
    ap.add_argument("--top", type=int, default=50, help="How many top sizes to print")
    args = ap.parse_args()

    payload = _gunzip_payload(args.pak)
    metas = _split_pngs(payload)

    if args.summary:
        _print_summary(metas, args.top)

    if args.export_all:
        # We already decompressed/split once for summary;
        # but export needs payload bytes, so reuse the same payload+metas
        # by calling export_all which redoes work. Keep it simple/robust.
        export_all(args.pak, args.out)
        print(f"\nExported all PNGs into: {args.out}")
        print(f"Wrote: {args.out / 'manifest_sizes.json'}")

    if not args.summary and not args.export_all:
        raise SystemExit("No action requested. Use --summary and/or --export-all.")


if __name__ == "__main__":
    main()