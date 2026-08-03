"""Tests for the Phase 3.4 repository KPI engine."""

from __future__ import annotations

import unittest

from dashboard_engine.aggregation import (
    AssetLifecycleSummary,
    CoverageSummary,
    RepositoryAggregation,
    ScenarioCompositionSummary,
)
from dashboard_engine.kpi import (
    HealthStatus,
    PercentageThresholds,
    RepositoryKpiCalculator,
)


def lifecycle(
    *,
    total: int,
    pending: int = 0,
    reviewed: int = 0,
    published: int = 0,
    unknown: int = 0,
) -> AssetLifecycleSummary:
    return AssetLifecycleSummary(
        total=total,
        pending_review=pending,
        reviewed=reviewed,
        published=published,
        unknown=unknown,
    )


def coverage(total: int, covered: int) -> CoverageSummary:
    return CoverageSummary(
        total_scenarios=total,
        covered_scenarios=covered,
        uncovered_scenarios=total - covered,
    )


def aggregation(
    *,
    manual_covered: int = 8,
    automation_covered: int = 7,
    overall_covered: int = 9,
    total_scenarios: int = 10,
    issues: int = 0,
    ignored: int = 0,
) -> RepositoryAggregation:
    return RepositoryAggregation(
        scenarios=lifecycle(
            total=total_scenarios,
            reviewed=2,
            published=6,
            pending=max(total_scenarios - 8, 0),
        ),
        manual_tests=lifecycle(
            total=10,
            reviewed=2,
            published=6,
            pending=2,
        ),
        automation_tests=lifecycle(
            total=10,
            reviewed=1,
            published=6,
            pending=3,
        ),
        all_test_definitions=lifecycle(
            total=20,
            reviewed=3,
            published=12,
            pending=5,
        ),
        manual_coverage=coverage(total_scenarios, manual_covered),
        automation_coverage=coverage(total_scenarios, automation_covered),
        overall_test_coverage=coverage(total_scenarios, overall_covered),
        scenario_composition=ScenarioCompositionSummary(
            total_scenarios=total_scenarios,
            manual_only=2,
            automation_only=1,
            manual_and_automation=6,
            no_test_definitions=1,
        ),
        indexing_issue_count=issues,
        ignored_asset_count=ignored,
    )


class PercentageThresholdTests(unittest.TestCase):
    def test_default_threshold_boundaries(self) -> None:
        thresholds = PercentageThresholds()

        self.assertEqual(HealthStatus.GREEN, thresholds.classify(80.0))
        self.assertEqual(HealthStatus.AMBER, thresholds.classify(79.99))
        self.assertEqual(HealthStatus.AMBER, thresholds.classify(70.0))
        self.assertEqual(HealthStatus.RED, thresholds.classify(69.99))

    def test_rejects_invalid_thresholds(self) -> None:
        with self.assertRaises(ValueError):
            PercentageThresholds(green_minimum=60.0, amber_minimum=70.0)


class RepositoryKpiCalculatorTests(unittest.TestCase):
    def test_calculates_coverage_health(self) -> None:
        kpis = RepositoryKpiCalculator().calculate(aggregation())

        self.assertEqual(80.0, kpis.manual_coverage.value)
        self.assertEqual(HealthStatus.GREEN, kpis.manual_coverage.status)
        self.assertEqual(70.0, kpis.automation_coverage.value)
        self.assertEqual(HealthStatus.AMBER, kpis.automation_coverage.status)
        self.assertEqual(90.0, kpis.overall_test_coverage.value)
        self.assertEqual(HealthStatus.GREEN, kpis.overall_test_coverage.status)

    def test_calculates_review_completion(self) -> None:
        kpis = RepositoryKpiCalculator().calculate(aggregation())

        self.assertEqual(80.0, kpis.scenario_review_completion.value)
        self.assertEqual(80.0, kpis.manual_test_review_completion.value)
        self.assertEqual(70.0, kpis.automation_test_review_completion.value)
        self.assertEqual(75.0, kpis.all_test_review_completion.value)

    def test_returns_not_applicable_for_empty_denominator(self) -> None:
        empty = RepositoryAggregation(
            scenarios=lifecycle(total=0),
            manual_tests=lifecycle(total=0),
            automation_tests=lifecycle(total=0),
            all_test_definitions=lifecycle(total=0),
            manual_coverage=coverage(0, 0),
            automation_coverage=coverage(0, 0),
            overall_test_coverage=coverage(0, 0),
            scenario_composition=ScenarioCompositionSummary(
                total_scenarios=0,
                manual_only=0,
                automation_only=0,
                manual_and_automation=0,
                no_test_definitions=0,
            ),
            indexing_issue_count=0,
            ignored_asset_count=0,
        )

        kpis = RepositoryKpiCalculator().calculate(empty)

        self.assertEqual(
            HealthStatus.NOT_APPLICABLE,
            kpis.overall_test_coverage.status,
        )
        self.assertEqual(
            HealthStatus.NOT_APPLICABLE,
            kpis.repository_data_quality.status,
        )

    def test_calculates_repository_data_quality(self) -> None:
        kpis = RepositoryKpiCalculator().calculate(
            aggregation(issues=2, ignored=1)
        )

        self.assertEqual(90.91, kpis.repository_data_quality.value)
        self.assertEqual(
            HealthStatus.GREEN,
            kpis.repository_data_quality.status,
        )

    def test_supports_custom_thresholds(self) -> None:
        calculator = RepositoryKpiCalculator(
            thresholds=PercentageThresholds(
                green_minimum=90.0,
                amber_minimum=75.0,
            )
        )

        kpis = calculator.calculate(aggregation())

        self.assertEqual(HealthStatus.AMBER, kpis.manual_coverage.status)
        self.assertEqual(HealthStatus.RED, kpis.automation_coverage.status)

    def test_serialization_contains_all_kpis(self) -> None:
        payload = RepositoryKpiCalculator().calculate(aggregation()).to_dict()

        self.assertEqual(8, len(payload["kpis"]))
        self.assertIn("overall_test_coverage", payload["kpis"])
        self.assertIn("repository_data_quality", payload["kpis"])


if __name__ == "__main__":
    unittest.main()
