from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class HoleProfileData:
    """Parsed profile data for World 5 → Hole.

    This class stores user/account state only and contains no mechanics.
    An empty instance represents a valid but uninitialized Hole state.
    """

    #TODO: well sediment includes sediments[0-9] notes[10-19] and rupies [20-29]
    # Update the class to store that in a readable format
    well_sediment: list[float] = field(default_factory=list)
    engineer_schematics: list[int] = field(default_factory=list)

    @classmethod
    def empty(cls) -> HoleProfileData:
        """Return an empty Hole profile."""
        return cls()