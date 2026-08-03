"""Build the stable dashboard snapshot contract."""

from __future__ import annotations

from datetime import UTC, datetime

from dashboard_engine.aggregation import RepositoryAggregation
from dashboard_engine.discovery import DiscoveryReport
from dashboard_engine.indexing import RepositoryIndex
from dashboard_engine.kpi import RepositoryKpiSet

from .models import (
    DashboardSnapshot,
    SnapshotMetadata,
    SnapshotQualitySummary,
)


class DashboardSnapshotBuilder:
    """Combine Phase 3.1–3.4 outputs into one UI-ready snapshot."""

    SCHEMA_VERSION = "1.0"

    def build(
        self,
        *,
        discovery: DiscoveryReport,
        repository_index: RepositoryIndex,
        aggregation: RepositoryAggregation,
        kpis: RepositoryKpiSet,
        generated_at: datetime | None = None,
        source: str = "repository",
    ) -> DashboardSnapshot:
        timestamp = generated_at or datetime.now(UTC)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=UTC)

        discovery_issue_count = len(discovery.issues)
        indexing_issue_count = len(repository_index.issues)
        ignored_asset_count = len(repository_index.ignored_assets)
        total_issue_count = (
            discovery_issue_count
            + indexing_issue_count
            + ignored_asset_count
        )

        return DashboardSnapshot(
            metadata=SnapshotMetadata(
                schema_version=self.SCHEMA_VERSION,
                generated_at=timestamp,
                source=source,
            ),
            quality=SnapshotQualitySummary(
                discovery_issue_count=discovery_issue_count,
                indexing_issue_count=indexing_issue_count,
                ignored_asset_count=ignored_asset_count,
                total_issue_count=total_issue_count,
                is_clean=total_issue_count == 0,
            ),
            aggregation=aggregation,
            kpis=kpis,
            repository_index=repository_index,
        )
