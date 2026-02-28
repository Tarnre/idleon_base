from __future__ import annotations

from dataclasses import dataclass

from idleonlib.profiles.profile_data.world7.minehead import MineheadProfileData


@dataclass(frozen=True, slots=True)
class RawLevelUpgradeSet:
    """UpgradeSet that treats upgrade level as the quantity.

    This is a *temporary* adapter for display-only work, until we wire in
    CustomLists.MineheadUPG multipliers (UpgradeQTY = mult * level).

    Attributes:
        minehead: Parsed Minehead profile data.
    """

    minehead: MineheadProfileData

    def upgrade_qty(self, index: int) -> float:
        return float(self.minehead.upgrade_level(index))