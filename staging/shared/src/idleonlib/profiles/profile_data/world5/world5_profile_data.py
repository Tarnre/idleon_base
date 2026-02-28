from __future__ import annotations

from dataclasses import dataclass, field

from idleonlib.profiles.profile_data.world5.hole import HoleProfileData


@dataclass(frozen=True, slots=True)
class World5ProfileData:
    """Parsed profile data for World 5.

    This module stores user/account state only. It must not contain any
    game mechanics calculations.

    Attributes:
        hole: Parsed Hole data, if present.
    """

    hole: HoleProfileData = field(default_factory=HoleProfileData.empty)
