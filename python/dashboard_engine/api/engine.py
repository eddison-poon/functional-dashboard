"""Stable orchestration API for the complete Phase 3 pipeline."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from dashboard_engine.aggregation import RepositoryAggregator
from dashboard_engine.discovery import RepositoryDiscovery
from dashboard_engine.executive_summary import ExecutiveSummaryGenerator
from dashboard_engine.indexing import RepositoryIndexBuilder
from dashboard_engine.kpi import (
    PercentageThresholds,
    RepositoryKpiCalculator,
)
from dashboard_engine.snapshot import DashboardSnapshotBuilder

from .configuration import DashboardEngineConfig
from .exceptions import DashboardEngineError
from .models import DashboardOutput


class DashboardEngine:
    """Orchestrate discovery through executive-summary generation."""

    def __init__(
        self,
        repository_root: str | Path | None = None,
        *,
        config: DashboardEngineConfig | None = None,
    ) -> None:
        if config is not None and repository_root is not None:
            raise ValueError("Provide repository_root or config, not both")

        if config is None:
            if repository_root is None:
                raise ValueError("repository_root or config is required")
            config = DashboardEngineConfig(
                repository_root=Path(repository_root),
            )

        self.config = config

    def generate_snapshot(
        self,
        *,
        generated_at: datetime | None = None,
    ):
        """Generate and return only the Phase 3.5 dashboard snapshot."""

        return self._run_pipeline(
            generated_at=generated_at,
            include_summary=False,
        ).snapshot

    def generate_executive_summary(
        self,
        *,
        generated_at: datetime | None = None,
    ):
        """Generate and return only the Phase 3.6 executive summary."""

        return self._run_pipeline(
            generated_at=generated_at,
            include_summary=True,
        ).executive_summary

    def generate_dashboard(
        self,
        *,
        generated_at: datetime | None = None,
    ) -> DashboardOutput:
        """Generate the complete public dashboard output."""

        return self._run_pipeline(
            generated_at=generated_at,
            include_summary=True,
        )

    def _run_pipeline(
        self,
        *,
        generated_at: datetime | None,
        include_summary: bool,
    ) -> DashboardOutput:
        try:
            discovery = RepositoryDiscovery(
                self.config.repository_root,
                asset_roots=self.config.asset_roots,
                strict_unknown_kind=self.config.strict_discovery,
                strict_unknown_state=self.config.strict_discovery,
            ).discover()

            repository_index = RepositoryIndexBuilder().build(discovery)
            aggregation = RepositoryAggregator().aggregate(repository_index)
            thresholds = PercentageThresholds(
                green_minimum=self.config.green_minimum,
                amber_minimum=self.config.amber_minimum,
            )
            kpis = RepositoryKpiCalculator(
                thresholds=thresholds
            ).calculate(aggregation)

            snapshot = DashboardSnapshotBuilder().build(
                discovery=discovery,
                repository_index=repository_index,
                aggregation=aggregation,
                kpis=kpis,
                generated_at=generated_at or datetime.now(UTC),
                source=self.config.source,
            )

            summary = ExecutiveSummaryGenerator(
                current_phase=self.config.current_phase
            ).generate(snapshot)

            return DashboardOutput(
                snapshot=snapshot,
                executive_summary=summary,
            )
        except (OSError, ValueError) as exc:
            raise DashboardEngineError(
                f"Dashboard generation failed: {exc}"
            ) from exc
