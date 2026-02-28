from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProfileParseError(Exception):
    """Raised when a profile config file cannot be parsed.

    Attributes:
        message: Human-readable error message.
        path: Optional JSON path (dot/bracket notation) to the failing
            value.
    """

    message: str
    path: str | None = None

    def __str__(self) -> str:
        if self.path is None:
            return self.message
        return f"{self.message} (path={self.path})"
