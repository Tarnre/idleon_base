from __future__ import annotations

"""Minehead probability summaries."""

from dataclasses import dataclass

from idleonlib.worlds.world7.minehead.simulator import MineheadGeneratedGrid


@dataclass(frozen=True, slots=True)
class MineheadTileStats:
    """Aggregate statistics for Minehead grid generation."""

    trials: int
    total_tiles: int
    # Average counts per grid.
    avg_mines: float
    avg_jackpot: float
    avg_numbers: float
    avg_minus_one: float
    avg_multiplier_tiles: float
    avg_additive_tiles: float
    avg_bluecrowns: float
    avg_gold_tiles: float
    # Per-code probabilities (tile-level; within the grid).
    p_by_code: dict[int, float]


def summarize(grids: list[MineheadGeneratedGrid]) -> MineheadTileStats:
    if not grids:
        raise ValueError("Need at least 1 grid")

    trials = len(grids)
    n_tiles = len(grids[0].tiles)

    code_counts: dict[int, int] = {}
    mines = jackpot = numbers = minus_one = mults = adds = crowns = gold = 0

    for g in grids:
        if len(g.tiles) != n_tiles:
            raise ValueError("All grids must have the same tile count")
        crowns += sum(g.crowns)
        gold += sum(g.gold)
        for v in g.tiles:
            code_counts[v] = code_counts.get(v, 0) + 1
            if v == 0:
                mines += 1
            elif v == 30:
                jackpot += 1
            elif 1 <= v <= 18:
                numbers += 1
            elif v == 19:
                minus_one += 1
            elif 20 <= v <= 29:
                mults += 1
            elif 40 <= v <= 49:
                adds += 1

    denom = trials * n_tiles
    p_by_code = {k: v / denom for k, v in sorted(code_counts.items())}

    return MineheadTileStats(
        trials=trials,
        total_tiles=n_tiles,
        avg_mines=mines / trials,
        avg_jackpot=jackpot / trials,
        avg_numbers=numbers / trials,
        avg_minus_one=minus_one / trials,
        avg_multiplier_tiles=mults / trials,
        avg_additive_tiles=adds / trials,
        avg_bluecrowns=crowns / trials,
        avg_gold_tiles=gold / trials,
        p_by_code=p_by_code,
    )
