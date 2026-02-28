from __future__ import annotations

import math


def lava_log(num: float) -> float:
    """Idleon lavaLog implementation.

    JS:
        Math.log(Math.max(num, 1)) / 2.30259

    Notes:
        We intentionally keep the 2.30259 constant (approx ln(10)) rather than
        using math.log10 to preserve parity with the game/toolbox behavior.
    """
    return math.log(max(num, 1.0)) / 2.30259
