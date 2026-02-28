from __future__ import annotations

from gaming_monte_carlo.simulation.engine import run_simulation
from gaming_monte_carlo.simulation.rules import Rules
from gaming_monte_carlo.simulation.state import TrialConfig


def test_smoke_run_is_deterministic() -> None:
    config = TrialConfig(initial_k=10, max_attempts=50, max_energy=5_000, seed=123)
    rules = Rules()

    r1 = run_simulation(config=config, rules=rules, n_trials=2_000)
    r2 = run_simulation(config=config, rules=rules, n_trials=2_000)

    # Deterministic given the same seed and run order.
    assert [x.success for x in r1] == [x.success for x in r2]
    assert [x.energy_spent for x in r1] == [x.energy_spent for x in r2]
