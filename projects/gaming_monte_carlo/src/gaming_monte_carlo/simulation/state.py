from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrialConfig:
    """Configuration for one simulation run.

    Attributes:
        snail_level: Snail level used by probability rules.
        initial_k: Starting encouragement value for the run.
        hole_bonus: Hole bonus percent (e.g., 12.5 for +12.5%).
    """

    snail_level: int
    initial_k: int
    hole_bonus: float = 0.0


@dataclass(frozen=True, slots=True)
class TrialState:
    """Mutable-by-copy state for a single run.

    Notes:
        - A run starts at k=initial_k.
        - Each attempt may succeed. If not, k decays (in engine).
        - A reset event is tracked but does not necessarily change state,
          unless you choose to encode reset semantics here.
    """

    k: int
    success: bool
    energy_spent: int
    reset_events: int

    @classmethod
    def from_config(cls, config: TrialConfig) -> TrialState:
        """Create a fresh state from config."""
        return cls(
            k=max(0, int(config.initial_k)),
            success=False,
            energy_spent=0,
            reset_events=0,
        )

    def with_success(self, success: bool) -> TrialState:
        """Return a copy with updated success flag."""
        return TrialState(
            k=self.k,
            success=bool(success),
            energy_spent=self.energy_spent,
            reset_events=self.reset_events,
        )

    def with_k(self, k: int) -> TrialState:
        """Return a copy with updated encouragement k."""
        return TrialState(
            k=int(k),
            success=self.success,
            energy_spent=self.energy_spent,
            reset_events=self.reset_events,
        )

    def with_energy_spent(self, energy_spent: int) -> TrialState:
        """Return a copy with updated energy spent."""
        return TrialState(
            k=self.k,
            success=self.success,
            energy_spent=int(energy_spent),
            reset_events=self.reset_events,
        )

    def with_reset_event(self) -> TrialState:
        """Return a copy reflecting a reset event.

        By default, this only increments the counter. If you decide a reset
        should also modify k or other state, encode it here so the engine
        stays clean.

        Returns:
            Updated TrialState.
        """
        return TrialState(
            k=self.k,
            success=self.success,
            energy_spent=self.energy_spent,
            reset_events=self.reset_events + 1,
        )
