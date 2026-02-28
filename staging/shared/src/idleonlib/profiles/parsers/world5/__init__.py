from __future__ import annotations

from typing import Any

from idleonlib.profiles.parsers.world5.hole import parse_hole_profile_data
from idleonlib.profiles.profile_data.world5.world5_profile_data import World5ProfileData


def parse_world5_profile_data(raw: dict[str, Any], *, strict: bool) -> World5ProfileData:
    """Parse all World 5 related profile data.

    This is an orchestrator that calls per-system parsers. Add new World 5
    sections by:
      1) implementing ``parse_<section>_profile_data``
      2) wiring it in here
      3) adding a field to :class:`World5ProfileData`

    Args:
        raw: Top-level decoded JSON dict.
        strict: If True, type mismatches raise ProfileParseError.

    Returns:
        Parsed :class:`World5ProfileData`.

    Raises:
        ProfileParseError: If required World 5 data is missing in strict
            mode.
    """

    hole = parse_hole_profile_data(raw, strict=strict)

    if hole is None:
        if strict:
            from idleonlib.profiles.parsers.errors import ProfileParseError

            raise ProfileParseError("World 5 Hole data not found", path="Holes")

        return World5ProfileData()

    return World5ProfileData(hole=hole)
