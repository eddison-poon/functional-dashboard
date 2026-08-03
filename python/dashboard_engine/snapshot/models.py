"""Immutable models for the Phase 3.5 dashboard snapshot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from dashboard_engine.aggregation import RepositoryAggregation
from dashboard_engine.indexing import RepositoryIndex
from dashboard_engine.kpi import RepositoryKpiSet


@dataclass(frozen=True, slots=True)
class SnapshotMetadata:
    """Metadata describing one generated dashboard snapshot."""

    schema_version: str
    generated_at: datetime
    source: str

    def to_dict(self) -> dict[str, str]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at.isoformat(),
            "source": self.source,
        }


@dataclass(frozen=True, slots=True)
class SnapshotQualitySummary:
    """Combined data-quality summary across discovery and indexing."""

    discovery_issue_count: int
    indexing_issue_count: int
    ignored_asset_count: int
    total_issue_count: int
    is_clean: bool

    def to_dict(self) -> dict[str, int | bool]:
        return {
            "discovery_issue_count": self.discovery_issue_count,
            "indexing_issue_count": self.indexing_issue_count,
            "ignored_asset_count": self.ignored_asset_count,
            "total_issue_count": self.total_issue_count,
            "is_clean": self.is_clean,
        }


@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    """Stable UI-facing snapshot contract."""

    metadata: SnapshotMetadata
    quality: SnapshotQualitySummary
    aggregation: RepositoryAggregation
    kpis: RepositoryKpiSet
    repository_index: RepositoryIndex

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "quality": self.quality.to_dict(),
            "summary": self.aggregation.to_dict(),
            "kpis": self.kpis.to_dict()["kpis"],
            "repository": {
                "scenarios": [
                    scenario.to_dict()
                    for scenario in self.repository_index.scenarios
                ],
                "counts": self.repository_index.to_dict()["counts"],
            },
        }
