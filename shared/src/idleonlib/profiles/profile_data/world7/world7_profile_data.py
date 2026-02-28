from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from idleonlib.profiles.profile_data.world7.minehead import (
    MineheadCore,
    MineheadProfileData,
    MineheadUpgrades,
)
from idleonlib.profiles.profile_data.world7.research import ResearchProfileData


@dataclass(frozen=True, slots=True)
class World7ProfileData:
    """Normalized profile data for World 7 (named fields).

    Attributes:
        research: Parsed Research blob (raw preserved).
        minehead: Named Minehead data derived from Research.
    """

    research: ResearchProfileData
    minehead: MineheadProfileData

    @staticmethod
    def empty() -> World7ProfileData:
        """Return an empty World 7 profile with sane defaults."""
        research = ResearchProfileData(raw=[])
        minehead = MineheadProfileData(
            core=MineheadCore.from_list([]),
            upgrades=MineheadUpgrades.from_list([]),
        )
        return World7ProfileData(research=research, minehead=minehead)

    @classmethod
    def from_research_blob(cls, blob: list[list[Any]]) -> World7ProfileData:
        """Build World 7 profile data from a decoded Research blob."""
        research = ResearchProfileData(raw=blob)

        core_raw = research.get_list(7)
        upgrades_raw = research.get_list(8)

        minehead = MineheadProfileData(
            core=MineheadCore.from_list(core_raw),
            upgrades=MineheadUpgrades.from_list(upgrades_raw),
        )

        return World7ProfileData(research=research, minehead=minehead)