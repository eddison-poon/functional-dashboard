"""Configuration for the public Dashboard Engine API."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DashboardEngineConfig:
    """Immutable configuration for one dashboard-generation run."""

    repository_root: Path
    asset_roots: tuple[Path, ...] | None = None
    strict_discovery: bool = False
    green_minimum: float = 80.0
    amber_minimum: float = 70.0
    source: str = "repository"
    current_phase: str = "Test Design and Review"

    def __post_init__(self) -> None:
        repository_root = Path(self.repository_root).expanduser().resolve()
        object.__setattr__(self, "repository_root", repository_root)

        if self.asset_roots is not None:
            normalized = tuple(Path(value) for value in self.asset_roots)
            object.__setattr__(self, "asset_roots", normalized)

        if not self.source.strip():
            raise ValueError("source must not be empty")
        if not self.current_phase.strip():
            raise ValueError("current_phase must not be empty")
