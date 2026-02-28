from __future__ import annotations

from typing import Any

from idleonlib.profiles.parsers.utils import (
    coerce_float,
    coerce_int,
    extract_float_list,
    extract_int_list,
    try_parse_json,
)
from idleonlib.profiles.parsers.errors import ProfileParseError
from idleonlib.profiles.profile_data.world5.hole import HoleProfileData


_WELL_SEDIMENT_INDEX = 9
_ENGINEER_SCHEMATICS_INDEX = 13


def parse_hole_profile_data(raw: dict[str, Any], *, strict: bool) -> HoleProfileData | None:
    """Parse World 5 → Hole profile data.

    Prefer parsing from the exported ``Holes`` blob (per upstream
    reference parser). If not present, fall back to key-path extraction.

    Args:
        raw: Top-level decoded JSON dict.
        strict: If True, type mismatches raise :class:`ProfileParseError`.

    Returns:
        Parsed :class:`HoleProfileData`, or None if not found.
    """

    hole_from_blob = _parse_from_holes_blob(raw, strict=strict)
    if hole_from_blob is not None:
        return hole_from_blob

    return _parse_from_key_paths(raw, strict=strict)


def _parse_from_holes_blob(raw: dict[str, Any], *, strict: bool) -> HoleProfileData | None:
    """Parse hole data from the exported ``Holes`` blob."""

    if "Holes" not in raw:
        return None

    holes_value = try_parse_json(raw.get("Holes"))
    if not isinstance(holes_value, list):
        if strict:
            raise ProfileParseError("Expected 'Holes' to decode to a list", path="Holes")
        return None

    well_raw = holes_value[_WELL_SEDIMENT_INDEX] if len(holes_value) > _WELL_SEDIMENT_INDEX else None
    engineer_raw = (
        holes_value[_ENGINEER_SCHEMATICS_INDEX]
        if len(holes_value) > _ENGINEER_SCHEMATICS_INDEX
        else None
    )

    well_sediment = _coerce_float_list(
        well_raw,
        strict=strict,
        path_prefix=f"Holes[{_WELL_SEDIMENT_INDEX}]",
    )
    engineer_schematics = _coerce_int_list(
        engineer_raw,
        strict=strict,
        path_prefix=f"Holes[{_ENGINEER_SCHEMATICS_INDEX}]",
    )

    if well_sediment is None and engineer_schematics is None:
        return None

    return HoleProfileData(
        well_sediment=well_sediment or [],
        engineer_schematics=engineer_schematics or [],
    )


def _parse_from_key_paths(raw: dict[str, Any], *, strict: bool) -> HoleProfileData | None:
    """Parse hole data from more structured key paths (future-proof)."""

    well_sediment = extract_float_list(
        raw,
        paths=(
            ("world5", "hole", "wellSediment"),
            ("worlds", "world5", "hole", "wellSediment"),
            ("hole", "wellSediment"),
            ("wellSediment",),
        ),
        strict=strict,
        name="wellSediment",
    )

    engineer_schematics = extract_int_list(
        raw,
        paths=(
            ("world5", "hole", "engineerSchematics"),
            ("worlds", "world5", "hole", "engineerSchematics"),
            ("hole", "engineerSchematics"),
            ("engineerSchematics",),
        ),
        strict=strict,
        name="engineerSchematics",
    )

    if well_sediment is None and engineer_schematics is None:
        return None

    return HoleProfileData(
        well_sediment=well_sediment or [],
        engineer_schematics=engineer_schematics or [],
    )


def _coerce_float_list(
    value: Any,
    *,
    strict: bool,
    path_prefix: str,
) -> list[float] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        if strict:
            raise ProfileParseError("Expected a list", path=path_prefix)
        return None

    out: list[float] = []
    for i, item in enumerate(value):
        coerced = coerce_float(item)
        if coerced is None:
            if strict:
                raise ProfileParseError("Invalid float", path=f"{path_prefix}[{i}]")
            continue
        out.append(coerced)

    return out


def _coerce_int_list(
    value: Any,
    *,
    strict: bool,
    path_prefix: str,
) -> list[int] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        if strict:
            raise ProfileParseError("Expected a list", path=path_prefix)
        return None

    out: list[int] = []
    for i, item in enumerate(value):
        coerced = coerce_int(item)
        if coerced is None:
            if strict:
                raise ProfileParseError("Invalid int", path=f"{path_prefix}[{i}]")
            continue
        out.append(coerced)

    return out
