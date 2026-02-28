from __future__ import annotations

"""Minehead (World 7) mechanics.

This module provides display-only formulas and lightweight types for
simulating or presenting Minehead values.
"""

from idleonlib.worlds.world7.minehead.data import (  # noqa: F401
    GRID_SIZES,
    MINEHEAD_UPGRADES,
    MineheadUpgradeDef,
    grid_dims,
)
from idleonlib.worlds.world7.minehead.formulas import (  # noqa: F401
    MineheadUpgradeSet,
    bluecrown_multi,
    bluecrown_odds,
    jackpot_odds,
    jackpot_tiles,
    max_hp_opp,
    mines_opp,
    total_tiles,
    upg_cost,
    upg_lv_req,
)
from idleonlib.worlds.world7.minehead.simulator import (  # noqa: F401
    MineheadGeneratedGrid,
    generate_grid,
    sample_grids,
)
from idleonlib.worlds.world7.minehead.stats import MineheadTileStats, summarize  # noqa: F401
