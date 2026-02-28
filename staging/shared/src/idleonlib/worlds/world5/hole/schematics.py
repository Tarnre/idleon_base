from __future__ import annotations

import math

from idleonlib.math_utils.logs import lava_log
from idleonlib.profiles.user_profile import UserProfile


def get_schematic_bonus(
    *,
    t: int,
    well_sediment: list[float],
    engineer_schematics: list[int],
) -> float:
    if t >= len(engineer_schematics) or engineer_schematics[t] == 0:
        return 0.0

    if t == 53:
        if 13 >= len(well_sediment):
            return 0.0
        return 4.0 * math.floor(lava_log(well_sediment[13]))

    return 0.0


def get_schematic_bonus_from_profile(*, t: int, profile: UserProfile) -> float:
    """Convenience wrapper using the parsed user profile."""
    hole = profile.world5.hole
    return get_schematic_bonus(
        t=t,
        well_sediment=hole.well_sediment,
        engineer_schematics=hole.engineer_schematics,
    )

