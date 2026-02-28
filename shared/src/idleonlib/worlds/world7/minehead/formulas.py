from __future__ import annotations

"""Minehead formulas (World 7).

These functions are direct transliterations of the Minehead-related
logic found in the decompiled Stencyl code (idleon1.06).
"""

import math
from typing import Protocol

from idleonlib.worlds.world7.minehead.data import MINEHEAD_UPGRADES, grid_dims


class MineheadUpgradeSet(Protocol):
    """Provides Minehead upgrade quantities used by formulas."""

    def upgrade_qty(self, index: int) -> float:
        """Return Minehead UpgradeQTY for the given upgrade index."""


def upg_lv_req(upgrade_index: int) -> int:
    """Return the level requirement to purchase an upgrade.

    Decompiled:
        1 + (3*t + (floor(t/3) + floor(t/11)))
    """
    t = int(upgrade_index)
    return 1 + (3 * t + (t // 3 + t // 11))


def upg_cost(
    upgrade_index: int,
    level: int,
    upgrades: MineheadUpgradeSet,
    *,
    mine_cost_server_var: float = 1.0,
) -> float:
    """Return Minehead upgrade cost at a given level.

    Decompiled (simplified):

        (5 + t + pow(max(0,t-2), 1.3))
        * pow(2, max(0,t-4))
        * pow(max(1, A_MineCost), max(0,t-9))
        * (1 / (1 + UpgradeQTY(26)/100))
        * pow(MineheadUPG[t][2], level)
    """
    t = int(upgrade_index)
    base = (5 + t + (max(0.0, t - 2) ** 1.3))
    base *= 2.0 ** max(0.0, t - 4)
    base *= max(1.0, float(mine_cost_server_var)) ** max(0.0, t - 9)
    base *= 1.0 / (1.0 + upgrades.upgrade_qty(26) / 100.0)

    mult = MINEHEAD_UPGRADES[t].cost_multiplier if 0 <= t < len(MINEHEAD_UPGRADES) else 1.0
    return base * (float(mult) ** float(level))


def mines_opp(opponent_index: int) -> int:
    """Return the number of mines the opponent uses."""
    t = int(opponent_index)
    return round(min(40, 1 + (t // 3 + (t // 7 + (t // 13 + min(1, t // 15) + t // 17)))))


def max_hp_opp(opponent_index: int, *, mine_hp_server_var: float = 1.0) -> float:
    """Return opponent max HP.

    Decompiled:

        (5 + (2*t + t^2))
        * 1.8^t
        * 1.85^floor(max(0,t-4)/3)
        * 4^floor(max(0,t-5)/7)
        * max(1, A_MineHP)^max(0,t-9)
    """
    t = int(opponent_index)
    return (
        (5.0 + (2.0 * t + (t**2)))
        * (1.8**t)
        * (1.85 ** math.floor(max(0.0, t - 4) / 3.0))
        * (4.0 ** math.floor(max(0.0, t - 5) / 7.0))
        * (max(1.0, float(mine_hp_server_var)) ** max(0.0, t - 9))
    )


def total_tiles(grid_expansion_level: int) -> int:
    """Return total tiles for a given grid expansion level."""
    r, c = grid_dims(grid_expansion_level)
    return int(r * c)


def bluecrown_multi(upgrades: MineheadUpgradeSet) -> float:
    """Return Blue Crown multiplier base."""
    return 1.5 + upgrades.upgrade_qty(14) / 100.0


def bluecrown_odds(upgrades: MineheadUpgradeSet) -> float:
    """Return odds that an eligible tile is a Blue Crown tile."""
    if upgrades.upgrade_qty(14) == 0:
        return 0.0
    return min(0.1, (1.0 / 15.0) * (1.0 + upgrades.upgrade_qty(15) / 100.0))


def jackpot_odds(upgrades: MineheadUpgradeSet) -> float:
    """Return odds that a tile becomes the single Jackpot tile."""
    if upgrades.upgrade_qty(23) == 0:
        return 0.0
    return 0.01 * (1.0 + upgrades.upgrade_qty(23) / 100.0)


def jackpot_tiles(upgrades: MineheadUpgradeSet) -> int:
    """Return number of tiles revealed by a Jackpot tile."""
    return round(3 + upgrades.upgrade_qty(24))
