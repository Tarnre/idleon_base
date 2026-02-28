from __future__ import annotations

from typing import Any

from idleonlib.profiles.parsers.errors import ProfileParseError
from idleonlib.profiles.parsers.utils import try_parse_json
from idleonlib.profiles.profile_data.world7.world7_profile_data import World7ProfileData


def parse_world7_profile_data(raw: dict[str, Any], *, strict: bool) -> World7ProfileData:
    """Parse World 7 profile data from a top-level export dict.

    The export stores Research as a JSON-encoded string under key "Research".

    Args:
        raw: Top-level decoded JSON dict.
        strict: If True, type mismatches raise ProfileParseError.

    Returns:
        Parsed World7ProfileData, or empty defaults if missing.
    """
    if "Research" not in raw:
        return World7ProfileData.empty()

    decoded = try_parse_json(raw.get("Research"))
    if decoded is None:
        if strict:
            raise ProfileParseError("Failed to decode 'Research' JSON", path="Research")
        return World7ProfileData.empty()

    if not isinstance(decoded, list):
        if strict:
            raise ProfileParseError("Expected 'Research' to decode to a list", path="Research")
        return World7ProfileData.empty()

    blob: list[list[Any]] = []
    for i, sub in enumerate(decoded):
        if isinstance(sub, list):
            blob.append(sub)
        else:
            if strict:
                raise ProfileParseError("Expected sublist", path=f"Research[{i}]")
            blob.append([])

    return World7ProfileData.from_research_blob(blob)