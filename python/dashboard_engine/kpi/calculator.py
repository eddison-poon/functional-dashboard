"""Calculate Phase 3.4 repository KPIs."""

from __future__ import annotations

from dashboard_engine.aggregation import (
    AssetLifecycleSummary,
    CoverageSummary,
    RepositoryAggregation,
)

from .enums import HealthStatus, KpiDirection
from .models import KpiResult, RepositoryKpiSet, ThresholdBand
from .thresholds import PercentageThresholds


class RepositoryKpiCalculator:
    """Convert Phase 3.3 aggregation summaries into traffic-light KPIs."""

    def __init__(
        self,
        *,
        thresholds: PercentageThresholds | None = None,
    ) -> None:
        self.thresholds = thresholds or PercentageThresholds()

    def calculate(self, aggregation: RepositoryAggregation) -> RepositoryKpiSet:
        return RepositoryKpiSet(
            manual_coverage=self._coverage_kpi(
                key="manual_coverage",
                title="Manual Coverage",
                coverage=aggregation.manual_coverage,
                description=(
                    "Percentage of Business Scenarios with at least one linked "
                    "Manual Test Definition."
                ),
            ),
            automation_coverage=self._coverage_kpi(
                key="automation_coverage",
                title="Automation Coverage",
                coverage=aggregation.automation_coverage,
                description=(
                    "Percentage of Business Scenarios with at least one linked "
                    "Automation Test Definition."
                ),
            ),
            overall_test_coverage=self._coverage_kpi(
                key="overall_test_coverage",
                title="Overall Test Coverage",
                coverage=aggregation.overall_test_coverage,
                description=(
                    "Percentage of Business Scenarios with at least one linked "
                    "Manual or Automation Test Definition."
                ),
            ),
            scenario_review_completion=self._review_kpi(
                key="scenario_review_completion",
                title="Scenario Review Completion",
                lifecycle=aggregation.scenarios,
                description=(
                    "Percentage of Business Scenarios that are reviewed or published."
                ),
            ),
            manual_test_review_completion=self._review_kpi(
                key="manual_test_review_completion",
                title="Manual Test Review Completion",
                lifecycle=aggregation.manual_tests,
                description=(
                    "Percentage of Manual Test Definitions that are reviewed or published."
                ),
            ),
            automation_test_review_completion=self._review_kpi(
                key="automation_test_review_completion",
                title="Automation Test Review Completion",
                lifecycle=aggregation.automation_tests,
                description=(
                    "Percentage of Automation Test Definitions that are reviewed "
                    "or published."
                ),
            ),
            all_test_review_completion=self._review_kpi(
                key="all_test_review_completion",
                title="All Test Review Completion",
                lifecycle=aggregation.all_test_definitions,
                description=(
                    "Percentage of all Test Definitions that are reviewed or published."
                ),
            ),
            repository_data_quality=self._quality_kpi(aggregation),
        )

    def _coverage_kpi(
        self,
        *,
        key: str,
        title: str,
        coverage: CoverageSummary,
        description: str,
    ) -> KpiResult:
        return self._percentage_kpi(
            key=key,
            title=title,
            numerator=coverage.covered_scenarios,
            denominator=coverage.total_scenarios,
            description=description,
        )

    def _review_kpi(
        self,
        *,
        key: str,
        title: str,
        lifecycle: AssetLifecycleSummary,
        description: str,
    ) -> KpiResult:
        completed = lifecycle.reviewed + lifecycle.published
        return self._percentage_kpi(
            key=key,
            title=title,
            numerator=completed,
            denominator=lifecycle.total,
            description=description,
        )

    def _quality_kpi(
        self,
        aggregation: RepositoryAggregation,
    ) -> KpiResult:
        issue_count = (
            aggregation.indexing_issue_count
            + aggregation.ignored_asset_count
        )
        total_assets = (
            aggregation.scenarios.total
            + aggregation.all_test_definitions.total
            + issue_count
        )
        clean_assets = max(total_assets - issue_count, 0)

        return self._percentage_kpi(
            key="repository_data_quality",
            title="Repository Data Quality",
            numerator=clean_assets,
            denominator=total_assets,
            description=(
                "Percentage of discovered repository assets that were indexed "
                "without indexing or ignored-asset quality issues."
            ),
        )

    def _percentage_kpi(
        self,
        *,
        key: str,
        title: str,
        numerator: int,
        denominator: int,
        description: str,
    ) -> KpiResult:
        threshold = ThresholdBand(
            green_minimum=self.thresholds.green_minimum,
            amber_minimum=self.thresholds.amber_minimum,
        )

        if denominator == 0:
            return KpiResult(
                key=key,
                title=title,
                value=0.0,
                unit="percent",
                status=HealthStatus.NOT_APPLICABLE,
                direction=KpiDirection.HIGHER_IS_BETTER,
                numerator=numerator,
                denominator=denominator,
                threshold=threshold,
                description=description,
            )

        value = round((numerator / denominator) * 100, 2)
        return KpiResult(
            key=key,
            title=title,
            value=value,
            unit="percent",
            status=self.thresholds.classify(value),
            direction=KpiDirection.HIGHER_IS_BETTER,
            numerator=numerator,
            denominator=denominator,
            threshold=threshold,
            description=description,
        )
