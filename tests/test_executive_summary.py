"""Tests for the Phase 3.6 executive summary generator."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime
from pathlib import Path

from dashboard_engine.aggregation import (
    AssetLifecycleSummary,
    CoverageSummary,
    RepositoryAggregation,
    ScenarioCompositionSummary,
)
from dashboard_engine.discovery import DiscoveryReport
from dashboard_engine.executive_summary import ExecutiveSummaryGenerator
from dashboard_engine.indexing import RepositoryIndex
from dashboard_engine.kpi import HealthStatus, RepositoryKpiCalculator
from dashboard_engine.snapshot import DashboardSnapshotBuilder


def lifecycle(
    total: int,
    *,
    pending: int = 0,
    reviewed: int = 0,
    published: int = 0,
) -> AssetLifecycleSummary:
    return AssetLifecycleSummary(
        total=total,
        pending_review=pending,
        reviewed=reviewed,
        published=published,
        unknown=0,
    )


def build_snapshot(
    *,
    total_scenarios: int,
    covered_scenarios: int,
    test_total: int,
    test_pending: int,
    test_reviewed: int,
    test_published: int,
):
    aggregation = RepositoryAggregation(
        scenarios=lifecycle(
            total_scenarios,
            reviewed=total_scenarios,
        ),
        manual_tests=lifecycle(
            test_total,
            pending=test_pending,
            reviewed=test_reviewed,
            published=test_published,
        ),
        automation_tests=lifecycle(0),
        all_test_definitions=lifecycle(
            test_total,
            pending=test_pending,
            reviewed=test_reviewed,
            published=test_published,
        ),
        manual_coverage=CoverageSummary(
            total_scenarios=total_scenarios,
            covered_scenarios=covered_scenarios,
            uncovered_scenarios=total_scenarios - covered_scenarios,
        ),
        automation_coverage=CoverageSummary(
            total_scenarios=total_scenarios,
            covered_scenarios=0,
            uncovered_scenarios=total_scenarios,
        ),
        overall_test_coverage=CoverageSummary(
            total_scenarios=total_scenarios,
            covered_scenarios=covered_scenarios,
            uncovered_scenarios=total_scenarios - covered_scenarios,
        ),
        scenario_composition=ScenarioCompositionSummary(
            total_scenarios=total_scenarios,
            manual_only=covered_scenarios,
            automation_only=0,
            manual_and_automation=0,
            no_test_definitions=total_scenarios - covered_scenarios,
        ),
        indexing_issue_count=0,
        ignored_asset_count=0,
    )
    kpis = RepositoryKpiCalculator().calculate(aggregation)
    discovery = DiscoveryReport(
        repository_root=Path("/repo"),
        assets=(),
        issues=(),
        scanned_files=0,
        ignored_files=0,
    )
    index = RepositoryIndex(
        scenarios=(),
        test_definitions=(),
        issues=(),
        ignored_assets=(),
    )
    return DashboardSnapshotBuilder().build(
        discovery=discovery,
        repository_index=index,
        aggregation=aggregation,
        kpis=kpis,
        generated_at=datetime(2026, 8, 4, 12, 0, tzinfo=UTC),
    )


class ExecutiveSummaryGeneratorTests(unittest.TestCase):
    def test_generates_green_summary(self) -> None:
        snapshot = build_snapshot(
            total_scenarios=10,
            covered_scenarios=9,
            test_total=10,
            test_pending=1,
            test_reviewed=2,
            test_published=7,
        )

        summary = ExecutiveSummaryGenerator().generate(snapshot)

        self.assertEqual(HealthStatus.GREEN, summary.overall_health)
        self.assertIn("GREEN", summary.headline)
        self.assertIn("90.00%", summary.headline)

    def test_generates_amber_summary(self) -> None:
        snapshot = build_snapshot(
            total_scenarios=10,
            covered_scenarios=8,
            test_total=10,
            test_pending=3,
            test_reviewed=2,
            test_published=5,
        )

        summary = ExecutiveSummaryGenerator().generate(snapshot)

        self.assertEqual(HealthStatus.AMBER, summary.overall_health)

    def test_generates_red_summary_when_any_core_kpi_is_red(self) -> None:
        snapshot = build_snapshot(
            total_scenarios=10,
            covered_scenarios=6,
            test_total=10,
            test_pending=5,
            test_reviewed=2,
            test_published=3,
        )

        summary = ExecutiveSummaryGenerator().generate(snapshot)

        self.assertEqual(HealthStatus.RED, summary.overall_health)
        self.assertTrue(summary.risks)

    def test_reports_coverage_and_review_risks(self) -> None:
        snapshot = build_snapshot(
            total_scenarios=10,
            covered_scenarios=7,
            test_total=10,
            test_pending=4,
            test_reviewed=3,
            test_published=3,
        )

        summary = ExecutiveSummaryGenerator().generate(snapshot)
        messages = " ".join(item.message for item in summary.risks)

        self.assertIn("3 Business Scenarios", messages)
        self.assertIn("4 Test Definitions", messages)

    def test_generates_standup_format(self) -> None:
        snapshot = build_snapshot(
            total_scenarios=5,
            covered_scenarios=5,
            test_total=5,
            test_pending=0,
            test_reviewed=2,
            test_published=3,
        )

        summary = ExecutiveSummaryGenerator().generate(snapshot)

        self.assertIn("Yesterday:", summary.standup_update)
        self.assertIn("Today:", summary.standup_update)
        self.assertIn("Blockers:", summary.standup_update)
        self.assertIn("Testing Health:", summary.standup_update)

    def test_serialization_contains_management_sections(self) -> None:
        snapshot = build_snapshot(
            total_scenarios=5,
            covered_scenarios=5,
            test_total=5,
            test_pending=0,
            test_reviewed=2,
            test_published=3,
        )

        payload = ExecutiveSummaryGenerator().generate(snapshot).to_dict()

        self.assertIn("headline", payload)
        self.assertIn("achievements", payload)
        self.assertIn("risks", payload)
        self.assertIn("readiness_assessment", payload)
        self.assertIn("standup_update", payload)


if __name__ == "__main__":
    unittest.main()
