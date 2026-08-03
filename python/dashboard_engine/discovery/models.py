"""Immutable output models for repository discovery."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .enums import AssetKind, ReviewState


@dataclass(frozen=True, slots=True)
class DiscoveredAsset:
    """One repository asset found by the discovery scanner."""

    path: Path
    relative_path: str
    asset_kind: AssetKind
    review_state: ReviewState
    asset_id: str | None
    title: str | None
    source_format: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "relative_path": self.relative_path,
            "asset_kind": self.asset_kind.value,
            "review_state": self.review_state.value,
            "asset_id": self.asset_id,
            "title": self.title,
            "source_format": self.source_format,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class DiscoveryIssue:
    """Non-fatal issue found while scanning the repository."""

    path: Path
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "path": str(self.path),
            "code": self.code,
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class DiscoveryReport:
    """Complete Phase 3.1 discovery result."""

    repository_root: Path
    assets: tuple[DiscoveredAsset, ...]
    issues: tuple[DiscoveryIssue, ...]
    scanned_files: int
    ignored_files: int

    @property
    def is_clean(self) -> bool:
        return not self.issues

    def count_by_kind(self) -> dict[str, int]:
        counts = {kind.value: 0 for kind in AssetKind}
        for asset in self.assets:
            counts[asset.asset_kind.value] += 1
        return counts

    def count_by_state(self) -> dict[str, int]:
        counts = {state.value: 0 for state in ReviewState}
        for asset in self.assets:
            counts[asset.review_state.value] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository_root": str(self.repository_root),
            "scanned_files": self.scanned_files,
            "ignored_files": self.ignored_files,
            "is_clean": self.is_clean,
            "counts": {
                "by_kind": self.count_by_kind(),
                "by_state": self.count_by_state(),
            },
            "assets": [asset.to_dict() for asset in self.assets],
            "issues": [issue.to_dict() for issue in self.issues],
        }
