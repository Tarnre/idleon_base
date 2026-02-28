from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ResearchProfileData:
    """World 7: Research raw state.

    Research is exported as a JSON string that decodes to a list of sublists.
    We preserve the decoded blob for completeness, but downstream systems
    should prefer named wrappers (e.g. MineheadCore/MineheadUpgrades).

    Attributes:
        raw: Decoded Research blob (list of sublists).
    """

    raw: list[list[Any]]

    def get_list(self, index: int) -> list[Any]:
        """Return a sublist by index, or an empty list if missing."""
        if index < 0 or index >= len(self.raw):
            return []
        sub = self.raw[index]
        return sub if isinstance(sub, list) else []