from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from numpy.random import Generator

from gaming_monte_carlo.simulation.rules import Rules, attempt_cost, p_reset_base, p_success
from gaming_monte_carlo.simulation.state import TrialConfig, TrialState


@dataclass(frozen=True, slots=True)
class TrialResult:
    """Outcome of a single run (one run ends at success or k <= 0)."""

    success: bool
    attempts: int
    resets: int
    energy_spent: int
    k_final: int


def _make_rng() -> Generator:
    """Create an RNG seeded from time.

    Returns:
        NumPy Generator.
    """
    # time_ns is plenty here; no reproducibility required.
    return np.random.default_rng(time.time_ns())


def run_one_trial(*, config: TrialConfig, rules: Rules, rng: Generator) -> TrialResult:
    """Run one trial (single run) until success or k <= 0.

    Termination:
      - success -> stop
      - k <= 0  -> fail -> stop

    Resets:
      - If an attempt fails, we may roll a "reset" event that increments
        a counter. The semantics of reset (if any) should be represented
        in how TrialState is updated below.

    Args:
        config: Trial configuration.
        rules: Rules.
        rng: RNG to use.

    Returns:
        TrialResult.
    """
    state = TrialState.from_config(config)

    attempts = 0
    resets = 0
    energy_spent = state.k*30

    while True:
        if state.success:
            return TrialResult(
                success=True,
                attempts=attempts,
                resets=resets,
                energy_spent=energy_spent,
                k_final=int(state.k),
            )

        if state.k <= 0:
            return TrialResult(
                success=False,
                attempts=attempts,
                resets=resets,
                energy_spent=energy_spent,
                k_final=int(state.k),
            )

        # Pay attempt cost.
        attempts += 1
        energy_spent += int(attempt_cost(state, rules))

        # Success roll.
        ps = float(p_success(state, config))
        if rng.random() < ps:
            state = state.with_success(True)
            continue

        # Failure path. Apply your "k decay on failure" rule.
        #
        # If your actual rule differs (e.g., resets force k=0, or reset
        # changes k more aggressively), implement it here in one place.
        state = state.with_k(state.k - 1)

        # Reset roll (only after failure).
        pr_base = float(p_reset_base(state, config))
        if rng.random() < pr_base:
            resets += 1
            state = state.with_reset_event()


def run_simulation(*, config: TrialConfig, rules: Rules, n_trials: int) -> list[TrialResult]:
    """Run many trials.

    Args:
        config: Trial configuration.
        rules: Rules.
        n_trials: Number of trials.

    Returns:
        List of TrialResult.
    """
    rng = _make_rng()
    results: list[TrialResult] = []

    for _ in range(int(n_trials)):
        results.append(run_one_trial(config=config, rules=rules, rng=rng))

    return results
