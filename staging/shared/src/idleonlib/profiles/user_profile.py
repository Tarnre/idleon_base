from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from idleonlib.profiles.profile_data.world5.world5_profile_data import World5ProfileData


@dataclass(frozen=True, slots=True)
class UserProfile:
    """Normalized user profile data parsed from an account export.

    This class represents a stable, library-controlled view of a user's
    Idleon state. It is intentionally decoupled from any specific export
    format. Parsers (e.g., ``config.json``) should populate these fields.

    Attributes:
        world5: Parsed profile data for World 5.
    """

    world5: World5ProfileData

    def to_dict(self) -> dict[str, Any]:
        """Serialize the profile to a plain-Python dict.

        This is intended for debugging, tests, and logging. The structure
        is library-defined and may expand over time.

        Returns:
            A JSON-serializable dict representation.
        """

        return {
            "world5": _world5_to_dict(self.world5),
        }

    @classmethod
    def from_config_json(
        cls,
        config_path: str | Path,
        *,
        strict: bool = True,
    ) -> UserProfile:
        """Load a profile from a flat ``config.json`` file.

        This is a convenience wrapper around
        :func:`idleonlib.profiles.parsers.config_json.load_user_profile_from_config_json`.
        The import is local to avoid import cycles.

        Args:
            config_path: Path to the ``config.json`` file.
            strict: If True, parsing errors raise an exception. If False,
                invalid/missing fields degrade to defaults.

        Returns:
            A populated :class:`UserProfile`.
        """

        from idleonlib.profiles.parsers.config_json import (  # noqa: WPS433
            load_user_profile_from_config_json,
        )

        return load_user_profile_from_config_json(config_path, strict=strict)


def _world5_to_dict(world5: World5ProfileData) -> dict[str, Any]:
    """Serialize World 5 profile data to a dict."""
    hole = world5.hole
    return {
        "hole": {
            "well_sediment": list(hole.well_sediment),
            "engineer_schematics": list(hole.engineer_schematics),
        },
    }

