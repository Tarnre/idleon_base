from __future__ import annotations

import json
from typing import Any, Iterable, Sequence

from idleonlib.profiles.parsers.errors import ProfileParseError


class _Missing:
    pass


MISSING = _Missing()


def try_parse_json(value: Any) -> Any:
    """Parse JSON if value is a JSON string; otherwise return as-is."""

    if not isinstance(value, str):
        return value

    stripped = value.strip()
    if not stripped:
        return value

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return value


def get_in(obj: Any, path: Sequence[str]) -> Any | _Missing:
    """Traverse dicts by key sequence; return MISSING if not present."""

    cur: Any = obj
    for key in path:
        if not isinstance(cur, dict):
            return MISSING
        if key not in cur:
            return MISSING
        cur = cur[key]
    return cur


def first_path_value(
    raw: dict[str, Any],
    paths: Sequence[Sequence[str]],
) -> tuple[Any, tuple[str, ...]] | _Missing:
    """Return the first found (value, path) for candidate JSON key paths."""

    for path in paths:
        value = get_in(raw, path)
        if value is not MISSING:
            return value, tuple(path)
    return MISSING


def extract_float_list(
    raw: dict[str, Any],
    *,
    paths: Sequence[Sequence[str]],
    strict: bool,
    name: str,
) -> list[float] | None:
    """Find and coerce a list of floats from the first matching path."""

    found = first_path_value(raw, paths)
    if found is MISSING:
        return None

    value, found_path = found
    if not isinstance(value, list):
        if strict:
            raise ProfileParseError(f"Expected a list for '{name}'", path=fmt_path(found_path))
        return None

    out: list[float] = []
    for i, item in enumerate(value):
        coerced = coerce_float(item)
        if coerced is None:
            if strict:
                raise ProfileParseError(
                    f"Invalid float at index {i} for '{name}'",
                    path=fmt_path((*found_path, str(i))),
                )
            continue
        out.append(coerced)

    return out


def extract_int_list(
    raw: dict[str, Any],
    *,
    paths: Sequence[Sequence[str]],
    strict: bool,
    name: str,
) -> list[int] | None:
    """Find and coerce a list of ints from the first matching path."""

    found = first_path_value(raw, paths)
    if found is MISSING:
        return None

    value, found_path = found
    if not isinstance(value, list):
        if strict:
            raise ProfileParseError(f"Expected a list for '{name}'", path=fmt_path(found_path))
        return None

    out: list[int] = []
    for i, item in enumerate(value):
        coerced = coerce_int(item)
        if coerced is None:
            if strict:
                raise ProfileParseError(
                    f"Invalid int at index {i} for '{name}'",
                    path=fmt_path((*found_path, str(i))),
                )
            continue
        out.append(coerced)

    return out


def coerce_float(value: Any) -> float | None:
    """Best-effort float coercion."""

    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def coerce_int(value: Any) -> int | None:
    """Best-effort int coercion."""

    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        return None
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def fmt_path(path: Iterable[str]) -> str:
    """Format a JSON path as dot/bracket notation."""

    parts: list[str] = []
    for p in path:
        if p.isdigit() and parts:
            parts[-1] = f"{parts[-1]}[{p}]"
            continue
        parts.append(p)
    return ".".join(parts)
