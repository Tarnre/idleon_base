from __future__ import annotations

"""Minehead formulas (World 7).

These functions are direct transliterations of the decompiled Stencyl
logic for Minehead where currently known.

Notes:
    - These are intended for *display/simulation* usage.
    - They deliberately avoid any purchase/unlock flow.

Known source keys (from the decompile):
    - MaxHP_Opp
    - Mines_Opp
    - Tiles_RowCol
    - Tiles_XY
    - BluecrownOdds
"""

import math


def max_hp_opp(opponent: int) -> int:
    """Compute boss max HP for a given Minehead opponent index.

    Args:
        opponent: 0-based opponent index.

    Returns:
        Max HP (rounded to nearest integer).
    """

    x = opponent + 1
    return round(4.5 * (x**1.5) + 32.0 * (x**2.9))


def mines_opp(opponent: int) -> int:
    """Compute the number of mines for a given Minehead opponent index.

    Args:
        opponent: 0-based opponent index.

    Returns:
        Mine count (rounded to nearest integer).
    """

    x = opponent
    return round(1 + math.floor(0.65 * x + 1) + math.floor(0.04 * ((x + 1) ** 3)))


def tiles_rowcol(opponent: int) -> int:
    """Compute the row/column size factor used by Minehead.

    The underlying logic clamps the value into [4, 72].

    Args:
        opponent: 0-based opponent index.

    Returns:
        Row/column size factor.
    """

    x = opponent + 1
    return max(4, min(72, math.floor(3 + 3.2 * (x**0.54))))


def tiles_xy(opponent: int) -> int:
    """Compute the XY sizing factor used by Minehead.

    The underlying logic clamps the value into [4, 72].

    Args:
        opponent: 0-based opponent index.

    Returns:
        XY sizing factor.
    """

    x = opponent + 1
    return max(4, min(72, round(4 + math.floor(3.9 * (x**0.63)))))


def bluecrown_odds(*, upgrade_1: float, upgrade_4: float, bonus_14: float) -> float:
    """Compute Blue Crown odds.

    This is a pure formula implementation:

    min(
        0.6,
        0.005 * (1 + bonus_14)
          * (upgrade_4 / (upgrade_4 + 1400))
          * (upgrade_1 / (upgrade_1 + 600))
    )

    Args:
        upgrade_1: Quantity/value of Minehead upgrade index 1.
        upgrade_4: Quantity/value of Minehead upgrade index 4.
        bonus_14: Quantity/value of Minehead bonus index 14.

    Returns:
        Probability in [0, 0.6].
    """

    term = (
        0.005
        * (1.0 + bonus_14)
        * (upgrade_4 / (upgrade_4 + 1400.0) if upgrade_4 > 0 else 0.0)
        * (upgrade_1 / (upgrade_1 + 600.0) if upgrade_1 > 0 else 0.0)
    )
    return min(0.6, term)
