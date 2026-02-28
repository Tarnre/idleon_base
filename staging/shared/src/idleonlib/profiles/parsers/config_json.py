from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idleonlib.profiles.parsers.errors import ProfileParseError
from idleonlib.profiles.parsers.world5 import parse_world5_profile_data
from idleonlib.profiles.user_profile import UserProfile


def load_user_profile_from_config_json(
    config_path: str | Path,
    *,
    strict: bool = True,
) -> UserProfile:
    """Load a :class:`~idleonlib.profiles.user_profile.UserProfile` from a config file.

    This function is responsible only for reading/parsing JSON and
    dispatching into section parsers that populate normalized profile data
    objects.

    Args:
        config_path: Path to the JSON file.
        strict: If True, parsing errors raise :class:`ProfileParseError`.
            If False, missing/invalid sections degrade to defaults.

    Returns:
        A normalized :class:`~idleonlib.profiles.user_profile.UserProfile`.

    Raises:
        ProfileParseError: If the JSON is invalid or required coercions
            fail in strict mode.
    """

    path = Path(config_path)
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProfileParseError(f"Failed to read config file: {exc}") from exc

    try:
        raw_obj = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ProfileParseError(f"Invalid JSON: {exc.msg}") from exc

    if not isinstance(raw_obj, dict):
        raise ProfileParseError("Top-level JSON must be an object")

    return parse_user_profile_dict(raw_obj, strict=strict)


def parse_user_profile_dict(
    raw: dict[str, Any],
    *,
    strict: bool = True,
) -> UserProfile:
    """Parse a raw JSON dict into a normalized :class:`UserProfile`.

    Args:
        raw: The decoded JSON object (top-level must be a dict).
        strict: If True, type mismatches raise :class:`ProfileParseError`.

    Returns:
        A :class:`UserProfile` with any recognized data populated.
    """

    world5 = parse_world5_profile_data(raw, strict=strict)

    return UserProfile(
        world5=world5,
    )
