from __future__ import annotations

import math


def clamp01(value: float) -> float:
    """Clamp a float into the range [0.0, 1.0]."""
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def average_attempts_from_success(ps: float) -> float:
    """Compute E[attempts] for geometric success with probability ps.

    Args:
        ps: Success probability per attempt.

    Returns:
        Expected attempts. inf if ps <= 0.
    """
    if ps <= 0.0:
        return float("inf")
    return 1.0 / ps


def succeed_before_reset_js(ps: float, real_reset: float) -> float:
    """Replicate the JS UI formula exactly.

    succeedBeforeReset = 1 - (1 - ps)^(1 / realResetChance)

    This is mainly for matching a UI display; it can behave oddly for
    extreme values (e.g., real_reset -> 0).

    Args:
        ps: Success probability.
        real_reset: Per-attempt reset probability (already mutually
            exclusive, i.e. P(reset on a given attempt)).

    Returns:
        Probability in [0.0, 1.0].
    """
    if ps <= 0.0:
        return 0.0
    if real_reset <= 0.0:
        return 1.0
    return clamp01(1.0 - math.pow(1.0 - ps, 1.0 / real_reset))


def expected_runs_per_success(p_run_success: float) -> float:
    """Expected number of independent runs until first success.

    Args:
        p_run_success: Probability a single run succeeds.

    Returns:
        1 / p_run_success, or inf if p_run_success <= 0.
    """
    if p_run_success <= 0.0:
        return float("inf")
    return 1.0 / p_run_success


def expected_failed_runs_before_success(p_run_success: float) -> float:
    """Expected number of failed runs before the first success.

    Args:
        p_run_success: Probability a single run succeeds.

    Returns:
        (1 - p) / p, or inf if p <= 0.
    """
    if p_run_success <= 0.0:
        return float("inf")
    q = 1.0 - p_run_success
    return q / p_run_success


def encouragement_needed_for_success_chance(
    *,
    snail_level: int,
    desired_success: float,
    hole_bonus: float,
    p_success_fn: callable[[int, float, float], float],
    low: int = 0,
    high: int = 1000,
) -> int:
    """Binary search encouragement to reach a desired success chance.

    This mirrors the common JS approach of using whole-number
    encouragement.

    Args:
        snail_level: Snail level (L).
        desired_success: Target success probability.
        hole_bonus: Hole bonus percent (H), e.g. 12.5 for +12.5%.
        p_success_fn: Callable computing success probability given
            (snail_level, encouragement, hole_bonus).
        low: Lower bound for search (inclusive).
        high: Upper bound for search (inclusive).

    Returns:
        Minimum integer encouragement E such that
        p_success_fn(L, E, H) >= desired_success.
    """
    target = clamp01(float(desired_success))

    lo = int(low)
    hi = int(high)
    while lo < hi:
        mid = (lo + hi) // 2
        ps = float(p_success_fn(snail_level, float(mid), hole_bonus))
        if ps >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
