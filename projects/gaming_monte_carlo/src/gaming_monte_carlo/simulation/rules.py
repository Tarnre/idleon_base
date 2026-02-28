from __future__ import annotations

import math
from dataclasses import dataclass

from gaming_monte_carlo.simulation.analysis import clamp01
from gaming_monte_carlo.simulation.state import TrialConfig, TrialState


@dataclass(frozen=True, slots=True)
class Rules:
    """Tunable parameters for the simulation.

    Only tunable knobs belong here. Core mechanics and trial termination
    rules live in `engine.py`.
    """

    attempt_energy_cost: int = 5


def attempt_cost(state: TrialState, rules: Rules) -> int:
    """Energy cost per attempt.

    Args:
        state: Current trial state (unused in the default rule).
        rules: Tunable rules.

    Returns:
        Integer energy cost for a single attempt.
    """
    _ = state
    return int(rules.attempt_energy_cost)


def snail_success_chance(
    snail_level: int,
    encouragement: float,
    hole_bonus: float = 0.0,
) -> float:
    """Compute snail success probability using your piecewise equation.

    Args:
        snail_level: Snail level (L). Piecewise boundary at 24.
        encouragement: Encouragement value (E).
        hole_bonus: Hole bonus percent (H), e.g. 12.5 for +12.5%.

    Returns:
        Probability in [0.0, 1.0].
    """
    l = float(snail_level)
    e = float(encouragement)

    hole_mult = 1.0 + float(hole_bonus) / 100.0

    if snail_level > 24:
        base = 1.0 - 0.6 * math.pow(l - 24.0, 0.16)
        enc_mult = 1.0 + (50.0 * e) / (3.0 + e) / 100.0
    else:
        base = 1.0 - 0.1 * math.pow(l, 0.71)
        enc_mult = 1.0 + (110.0 * e) / (25.0 + e) / 100.0

    return clamp01(base * hole_mult * enc_mult)


def snail_reset_base_chance(snail_level: int, encouragement: float) -> float:
    """Compute reset *base* probability using your piecewise equation.

    Important:
        This is a base reset chance that should be rolled ONLY after a
        failure (i.e., after not succeeding).

    Args:
        snail_level: Snail level (L). Piecewise boundary at 24.
        encouragement: Encouragement value (E).

    Returns:
        Probability in [0.0, 1.0].
    """
    l = float(snail_level)
    e = float(encouragement)

    if snail_level > 24:
        numerator = math.pow(l - 24.0, 0.19) - 0.9
        denom = 1.0 + (60.0 * e) / (3.0 + e) / 100.0
    else:
        numerator = math.pow(l + 1.0, 0.07) - 1.0
        denom = 1.0 + (300.0 * e) / (100.0 + e) / 100.0

    raw = 0.0 if denom == 0.0 else numerator / denom
    return clamp01(max(0.0, raw))


def p_success(state: TrialState, config: TrialConfig) -> float:
    """Success probability for the current attempt."""
    return snail_success_chance(
        snail_level=int(config.snail_level),
        encouragement=float(state.k),
        hole_bonus=float(config.hole_bonus),
    )


def p_reset_base(state: TrialState, config: TrialConfig) -> float:
    """Reset base probability for the current attempt (evaluated on failure)."""
    return snail_reset_base_chance(
        snail_level=int(config.snail_level),
        encouragement=float(state.k),
    )


def real_reset_chance_per_attempt(
    *,
    snail_level: int,
    encouragement: float,
    hole_bonus: float = 0.0,
) -> float:
    """Compute per-attempt probability of a reset event.

    With simulation order:
      1) roll success with p_success
      2) if failure, roll reset with p_reset_base

    So:
      P(reset on an attempt) = (1 - p_success) * p_reset_base
    """
    ps = snail_success_chance(snail_level, encouragement, hole_bonus)
    pr_base = snail_reset_base_chance(snail_level, encouragement)
    return clamp01((1.0 - ps) * pr_base)
