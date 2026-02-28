from __future__ import annotations

"""Minehead formulas (World 7).

These functions are direct transliterations of the decompiled Stencyl
logic for Minehead where currently known.

Notes:
    - These are intended for *display/simulation* usage.
    - They deliberately avoid any purchase/unlock flow.
"""

import math
from typing import Protocol


class MineheadUpgradeSet(Protocol):
    """Provides Minehead upgrade quantities used by formulas."""

    def upgrade_qty(self, index: int) -> float:
        """Return Minehead UpgradeQTY for the given upgrade index."""


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


def bluecrown_odds(upgrades: MineheadUpgradeSet) -> float:
    """Compute Blue Crown odds.

    Decompiled logic:

        if UpgradeQTY(14) == 0:
            0
        else:
            min(0.1, (1/15) * (1 + UpgradeQTY(15)/100))

    Args:
        upgrades: Provider for Minehead UpgradeQTY(i).

    Returns:
        Probability in [0, 0.1].
    """
    if upgrades.upgrade_qty(14) == 0:
        return 0.0
    return min(0.1, (1.0 / 15.0) * (1.0 + upgrades.upgrade_qty(15) / 100.0))