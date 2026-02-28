from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from gaming_monte_carlo.simulation.engine import TrialResult
from gaming_monte_carlo.simulation.rules import Rules
from gaming_monte_carlo.simulation.state import TrialConfig


@dataclass(frozen=True, slots=True)
class Summary:
    """Aggregate metrics for a simulation run.

    Notes:
        - A "trial" is one run that ends on success or when k <= 0.
        - "Until success" metrics are computed analytically from per-run
          success probability (geometric runs-to-success), to avoid
          simulating repeated runs inside each trial.
    """

    n_trials: int

    # Per-run probabilities.
    success_rate: float
    fail_rate: float
    p_needs_reset_before_success: float

    # Per-run observed means.
    mean_attempts: float
    mean_resets: float
    mean_energy: float

    # Conditional per-run means.
    mean_attempts_success: float
    mean_attempts_fail: float
    mean_energy_success: float
    mean_energy_fail: float

    # "Until success" expectations (geometric over runs).
    expected_runs_per_success: float
    expected_resets_before_success: float
    expected_attempts_per_success: float
    expected_energy_per_success: float
    expected_encouragement_upgrades_per_success: float

    def __str__(self) -> str:
        lines = [
            f"Trials: {self.n_trials}",
            f"Success rate (per run): {self.success_rate:.6f}",
            f"Fail rate (per run): {self.fail_rate:.6f}",
            f"P(needs at least one reset before success): "
            f"{self.p_needs_reset_before_success:.6f}",
            "",
            f"Mean attempts (per run): {self.mean_attempts:.3f}",
            f"Mean resets (per run): {self.mean_resets:.3f}",
            f"Mean energy (per run): {self.mean_energy:.3f}",
            "",
            f"Mean attempts | success: {self.mean_attempts_success:.3f}",
            f"Mean attempts | fail: {self.mean_attempts_fail:.3f}",
            f"Mean energy | success: {self.mean_energy_success:.3f}",
            f"Mean energy | fail: {self.mean_energy_fail:.3f}",
            "",
            f"Expected runs per success: {self.expected_runs_per_success:.3f}",
            f"Expected resets before success: {self.expected_resets_before_success:.3f}",
            f"Expected attempts per success: {self.expected_attempts_per_success:.3f}",
            f"Expected energy per success: {self.expected_energy_per_success:.3f}",
            f"Expected encouragement upgrades per success: "
            f"{self.expected_encouragement_upgrades_per_success:.3f}",
        ]
        return "\n".join(lines)


def summarize_results(
    results: list[TrialResult],
    config: TrialConfig,
    rules: Rules,
) -> Summary:
    """Summarize a batch of trial results.

    Metrics are observational only (LOCKED) except the "until success"
    expectations, which are computed analytically from per-run success
    probability to avoid nested simulation.
    """
    _ = rules

    n = len(results)
    if n == 0:
        return Summary(
            n_trials=0,
            success_rate=0.0,
            fail_rate=1.0,
            p_needs_reset_before_success=1.0,
            mean_attempts=0.0,
            mean_resets=0.0,
            mean_energy=0.0,
            mean_attempts_success=0.0,
            mean_attempts_fail=0.0,
            mean_energy_success=0.0,
            mean_energy_fail=0.0,
            expected_runs_per_success=float("inf"),
            expected_resets_before_success=float("inf"),
            expected_attempts_per_success=float("inf"),
            expected_energy_per_success=float("inf"),
            expected_encouragement_upgrades_per_success=float("inf"),
        )

    success = np.fromiter((1.0 if r.success else 0.0 for r in results), dtype=float, count=n)
    energy = np.fromiter((float(r.energy_spent) for r in results), dtype=float, count=n)
    attempts = np.fromiter((float(r.attempts) for r in results), dtype=float, count=n)
    resets = np.fromiter((float(r.resets) for r in results), dtype=float, count=n)

    p = float(success.mean())
    q = 1.0 - p

    mean_attempts = float(attempts.mean())
    mean_resets = float(resets.mean())
    mean_energy = float(energy.mean())

    # Conditional means. If there are no successes/failures, define as 0.
    mask_s = success == 1.0
    mask_f = ~mask_s

    mean_attempts_success = float(attempts[mask_s].mean()) if mask_s.any() else 0.0
    mean_attempts_fail = float(attempts[mask_f].mean()) if mask_f.any() else 0.0
    mean_energy_success = float(energy[mask_s].mean()) if mask_s.any() else 0.0
    mean_energy_fail = float(energy[mask_f].mean()) if mask_f.any() else 0.0

    # "Until success" expectations (geometric over runs).
    #
    # Expected #runs until first success: 1/p
    # Expected #failed runs before success: q/p
    # P(needs at least one reset before success): q
    #
    # Expected total attempts until success:
    #   E[A | success] + (q/p) * E[A | fail]
    #
    # Same for energy.
    if p == 0.0:
        expected_runs_per_success = float("inf")
        expected_resets_before_success = float("inf")
        expected_attempts_per_success = float("inf")
        expected_energy_per_success = float("inf")
        expected_encouragement_upgrades_per_success = float("inf")
    else:
        expected_runs_per_success = 1.0 / p
        expected_resets_before_success = q / p

        expected_attempts_per_success = mean_attempts_success + (q / p) * mean_attempts_fail
        expected_energy_per_success = mean_energy_success + (q / p) * mean_energy_fail

        # Your "encouragement upgrades" model:
        # one "run" costs initial_k encouragement upgrades to build back up.
        expected_encouragement_upgrades_per_success = float(config.initial_k) * (1.0 / p)

    return Summary(
        n_trials=n,
        success_rate=p,
        fail_rate=q,
        p_needs_reset_before_success=q,
        mean_attempts=mean_attempts,
        mean_resets=mean_resets,
        mean_energy=mean_energy,
        mean_attempts_success=mean_attempts_success,
        mean_attempts_fail=mean_attempts_fail,
        mean_energy_success=mean_energy_success,
        mean_energy_fail=mean_energy_fail,
        expected_runs_per_success=expected_runs_per_success,
        expected_resets_before_success=expected_resets_before_success,
        expected_attempts_per_success=expected_attempts_per_success,
        expected_energy_per_success=expected_energy_per_success,
        expected_encouragement_upgrades_per_success=expected_encouragement_upgrades_per_success,
    )
