from __future__ import annotations

"""Minehead grid simulation.

This simulates the *initial* tile generation for a given user state:

- Tile numbers (1..)
- Multiplier tiles (20..29)
- Additive tiles (40..49)
- Single jackpot tile (30)
- Mine placement (0)
- Blue crown backgrounds
- Gold tile top overlays

It does **not** simulate gameplay decisions. The goal is to compute the
distribution of the generated grids.
"""

import math
from dataclasses import dataclass
from typing import Iterable

from idleonlib.worlds.world7.minehead.formulas import (
    MineheadUpgradeSet,
    bluecrown_odds,
    jackpot_odds,
    total_tiles,
)


@dataclass(frozen=True, slots=True)
class MineheadGeneratedGrid:
    """A generated Minehead grid.

    Attributes:
        tiles: Tile codes for the current grid (length == total tiles).
            0 => mine, 1..19 => number tiles, 20..29 => multiplier,
            30 => jackpot, 40..49 => additive.
        crowns: 1 if a tile is a bluecrown tile, else 0.
        gold: 1 if a tile is a gold tile, else 0.
    """

    tiles: tuple[int, ...]
    crowns: tuple[int, ...]
    gold: tuple[int, ...]


class _Rng:
    """Adapter over Python's random.Random-like interface."""

    def __init__(self, rand) -> None:
        self._r = rand

    def float(self) -> float:
        return float(self._r.random())

    def int_inclusive(self, a: int, b: int) -> int:
        # Stencyl randomInt is inclusive of both ends.
        return int(self._r.randint(a, b))

    def float_between(self, a: float, b: float) -> float:
        return float(a + (b - a) * self.float())


def generate_grid(
    upgrades: MineheadUpgradeSet,
    *,
    opponent_index: int,
    grid_expansion_level: int,
    rng,
) -> MineheadGeneratedGrid:
    """Generate a Minehead grid using decompiled generation logic."""

    r = _Rng(rng)
    n_tiles = total_tiles(grid_expansion_level)

    tiles: list[int] = [0] * n_tiles
    revealed: list[int] = [0] * n_tiles
    crowns: list[int] = [0] * n_tiles

    # --- Base tile numbers (runs in decompile for 72, but only the first
    #     TotalTiles are used). ------------------------------------------
    max_numbah = upgrades.upgrade_qty(1)
    bettah = upgrades.upgrade_qty(3)
    for s in range(n_tiles):
        dn1 = int(
            (1
             + min(
                 min(12.0, bettah / 150.0) + r.float(),
                 max_numbah,
             ))
        )
        for _ in range(17):
            if round(dn1) > round(max_numbah):
                break
            if r.float() >= (
                0.14
                + min(0.06, bettah / 2000.0)
                + min(0.5, (bettah / (bettah + 1500.0)) * 0.5)
            ):
                break
            dn1 = int(round(dn1 + 1))

        tiles[s] = int(dn1)
        if bettah > 10 and r.int_inclusive(1, 5000) == 1:
            tiles[s] = 19
        revealed[s] = 0
        crowns[s] = 0

    # --- Multiplier tiles (20..29) -------------------------------------
    multi_max = upgrades.upgrade_qty(12)
    multi_odds_boost = upgrades.upgrade_qty(13)
    got_jackpot = False
    for s in range(n_tiles):
        if (
            r.float()
            < 0.05 + (multi_odds_boost / (multi_odds_boost + 1000.0)) * 0.08
            and multi_max > 0
        ):
            dn1 = int(math.floor(min(3.0, multi_odds_boost / 400.0) + r.float()))
            for _ in range(9):
                if round(dn1 + 1) >= round(multi_max):
                    break
                if r.float() >= (
                    0.18
                    + min(0.07, multi_odds_boost / 2000.0)
                    + (multi_odds_boost / (multi_odds_boost + 1200.0)) * 0.3
                ):
                    break
                dn1 = int(round(dn1 + 1))
            tiles[s] = int(round(min(29, 20 + dn1)))

        # --- Jackpot tile (30) ----------------------------------------
        if not got_jackpot and r.float() < jackpot_odds(upgrades):
            tiles[s] = 30
            got_jackpot = True

        # --- Additive tiles (40..49) ----------------------------------
        add_max = upgrades.upgrade_qty(17)
        add_odds_boost = upgrades.upgrade_qty(18)
        if (
            r.float() < 0.07 + (add_odds_boost / (add_odds_boost + 1000.0)) * 0.1
            and add_max > 0
        ):
            dn1 = int(math.floor(min(3.0, add_odds_boost / 400.0) + r.float()))
            for _ in range(9):
                if round(dn1 + 1) >= round(add_max):
                    break
                if r.float() >= (
                    0.14
                    + min(0.06, add_odds_boost / 2000.0)
                    + (add_odds_boost / (add_odds_boost + 1200.0)) * 0.25
                ):
                    break
                dn1 = int(round(dn1 + 1))
            tiles[s] = int(round(min(49, 40 + dn1)))

    # --- Mine placement (0) --------------------------------------------
    from idleonlib.worlds.world7.minehead.formulas import mines_opp

    mines = min(n_tiles, mines_opp(opponent_index))
    for _ in range(mines):
        idx = r.int_inclusive(0, n_tiles - 1)
        while tiles[idx] == 0:
            idx = r.int_inclusive(0, n_tiles - 1)
        tiles[idx] = 0

    # --- Blue crowns ----------------------------------------------------
    bc_odds = bluecrown_odds(upgrades)
    for s in range(n_tiles):
        if tiles[s] != 0 and r.float() < bc_odds:
            crowns[s] = 1

    # --- Gold tiles -----------------------------------------------------
    # In-game, GenINFO[38] is decremented per gold tile.
    gold_remaining = int(round(upgrades.upgrade_qty(8)))
    gold: list[int] = [0] * n_tiles
    for s in range(n_tiles):
        if gold_remaining <= 0 or tiles[s] == 0:
            continue
        p = max(2.0, r.float_between(0.12, 0.4) * upgrades.upgrade_qty(8)) / float(n_tiles)
        if r.float() < p:
            gold[s] = 1
            gold_remaining -= 1

    return MineheadGeneratedGrid(tiles=tuple(tiles), crowns=tuple(crowns), gold=tuple(gold))


def sample_grids(
    upgrades: MineheadUpgradeSet,
    *,
    opponent_index: int,
    grid_expansion_level: int,
    rng,
    trials: int,
) -> Iterable[MineheadGeneratedGrid]:
    """Yield a stream of generated grids."""

    for _ in range(int(trials)):
        yield generate_grid(
            upgrades,
            opponent_index=opponent_index,
            grid_expansion_level=grid_expansion_level,
            rng=rng,
        )
