from __future__ import annotations

"""Minehead upgrade adapters.

Historically, this module provided a temporary adapter that treated a
raw upgrade *level* as the quantity. Minehead formulas use UpgradeQTY,
which is the upgrade-specific multiplier times level.

Now that :class:`~idleonlib.profiles.profile_data.world7.minehead.MineheadUpgrades`
implements UpgradeQTY correctly, these adapters simply expose a stable
protocol surface for formula/simulation code.
"""

from dataclasses import dataclass

from idleonlib.profiles.profile_data.world7.minehead import MineheadProfileData


@dataclass(frozen=True, slots=True)
class ProfileUpgradeSet:
    """Adapter that exposes UpgradeQTY from a parsed Minehead profile."""

    minehead: MineheadProfileData

    def upgrade_qty(self, index: int) -> float:
        """Return UpgradeQTY for a given upgrade index."""
        return float(self.minehead.upgrade_qty(index))
