import { useEffect, useMemo, useState } from "react";

type ManifestImage = {
  idx: number;
  file: string;
  width: number;
  height: number;
  sha256: string;
};

type Manifest = {
  exported: number;
  total_pngs_in_pack: number;
  images: ManifestImage[];
};

export default function IconPicker() {
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [q, setQ] = useState("");
  const [limit, setLimit] = useState(300);

  useEffect(() => {
    fetch("/assets/defaultpak/56x56/manifest.json")
      .then((r) => r.json())
      .then((j) => setManifest(j))
      .catch((e) => {
        console.error(e);
        setManifest(null);
      });
  }, []);

  const images = useMemo(() => {
    const imgs = manifest?.images ?? [];
    if (!q.trim()) return imgs.slice(0, limit);
    const qq = q.trim().toLowerCase();
    // You can paste either an idx number or part of a filename.
    return imgs
      .filter((im) => String(im.idx).includes(qq) || im.file.toLowerCase().includes(qq))
      .slice(0, limit);
  }, [manifest, q, limit]);

  const base = "/assets/defaultpak/56x56/";

  return (
    <div style={{ padding: 16 }}>
      <h1 style={{ marginTop: 0 }}>default.pak Icon Picker (56×56)</h1>

      <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Filter (idx or filename)…"
          style={{ padding: 8, minWidth: 260 }}
        />
        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          Limit
          <input
            type="number"
            value={limit}
            onChange={(e) => setLimit(Math.max(50, Number(e.target.value)))}
            style={{ width: 100, padding: 6 }}
          />
        </label>
        <div style={{ opacity: 0.8 }}>
          {manifest ? `${manifest.images.length} images loaded` : "Loading…"}
        </div>
      </div>

      <div
        style={{
          marginTop: 16,
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
          gap: 12,
        }}
      >
        {images.map((im) => {
          const url = `${base}${im.file}`;
          return (
            <button
              key={im.idx}
              onClick={() => {
                navigator.clipboard.writeText(String(im.idx)).catch(() => {});
                console.log("Picked idx:", im.idx, url);
              }}
              title="Click to copy idx to clipboard"
              style={{
                border: "1px solid rgba(255,255,255,0.15)",
                borderRadius: 10,
                padding: 10,
                background: "rgba(255,255,255,0.04)",
                textAlign: "left",
                cursor: "pointer",
              }}
            >
              <img
                src={url}
                width={56}
                height={56}
                alt={`png ${im.idx}`}
                style={{
                  display: "block",
                  marginBottom: 8,
                  imageRendering: "pixelated",
                }}
              />
              <div style={{ fontSize: 12, opacity: 0.9 }}>idx {im.idx}</div>
              <div style={{ fontSize: 11, opacity: 0.7 }}>{im.file}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}