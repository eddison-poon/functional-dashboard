"""Tests for the Phase 3.5 dashboard snapshot."""

from __future__ import annotations

import json
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
from dashboard_engine.indexing import RepositoryIndex
from dashboard_engine.kpi import RepositoryKpiCalculator
from dashboard_engine.snapshot import DashboardSnapshotBuilder


def lifecycle(total: int) -> AssetLifecycleSummary:
    return AssetLifecycleSummary(
        total=total,
        pending_review=total,
        reviewed=0,
        published=0,
        unknown=0,
    )


def aggregation() -> RepositoryAggregation:
    return RepositoryAggregation(
        scenarios=lifecycle(2),
        manual_tests=lifecycle(1),
        automation_tests=lifecycle(1),
        all_test_definitions=lifecycle(2),
        manual_coverage=CoverageSummary(
            total_scenarios=2,
            covered_scenarios=1,
            uncovered_scenarios=1,
        ),
        automation_coverage=CoverageSummary(
            total_scenarios=2,
            covered_scenarios=1,
            uncovered_scenarios=1,
        ),
        overall_test_coverage=CoverageSummary(
            total_scenarios=2,
            covered_scenarios=2,
            uncovered_scenarios=0,
        ),
        scenario_composition=ScenarioCompositionSummary(
            total_scenarios=2,
            manual_only=1,
            automation_only=1,
            manual_and_automation=0,
            no_test_definitions=0,
        ),
        indexing_issue_count=0,
        ignored_asset_count=0,
    )


class DashboardSnapshotBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.discovery = DiscoveryReport(
            repository_root=Path("/repo"),
            assets=(),
            issues=(),
            scanned_files=0,
            ignored_files=0,
        )
        self.index = RepositoryIndex(
            scenarios=(),
            test_definitions=(),
            issues=(),
            ignored_assets=(),
        )
        self.aggregation = aggregation()
        self.kpis = RepositoryKpiCalculator().calculate(self.aggregation)
        self.generated_at = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)

    def test_builds_snapshot_with_stable_schema_version(self) -> None:
        snapshot = DashboardSnapshotBuilder().build(
            discovery=self.discovery,
            repository_index=self.index,
            aggregation=self.aggregation,
            kpis=self.kpis,
            generated_at=self.generated_at,
        )

        self.assertEqual("1.0", snapshot.metadata.schema_version)
        self.assertEqual(self.generated_at, snapshot.metadata.generated_at)

    def test_marks_clean_snapshot_when_no_issues_exist(self) -> None:
        snapshot = DashboardSnapshotBuilder().build(
            discovery=self.discovery,
            repository_index=self.index,
            aggregation=self.aggregation,
            kpis=self.kpis,
            generated_at=self.generated_at,
        )

        self.assertTrue(snapshot.quality.is_clean)
        self.assertEqual(0, snapshot.quality.total_issue_count)

    def test_serialization_contains_ui_contract_sections(self) -> None:
        snapshot = DashboardSnapshotBuilder().build(
            discovery=self.discovery,
            repository_index=self.index,
            aggregation=self.aggregation,
            kpis=self.kpis,
            generated_at=self.generated_at,
        )

        payload = snapshot.to_dict()

        self.assertIn("metadata", payload)
        self.assertIn("quality", payload)
        self.assertIn("summary", payload)
        self.assertIn("kpis", payload)
        self.assertIn("repository", payload)

    def test_serialization_is_json_compatible(self) -> None:
        snapshot = DashboardSnapshotBuilder().build(
            discovery=self.discovery,
            repository_index=self.index,
            aggregation=self.aggregation,
            kpis=self.kpis,
            generated_at=self.generated_at,
        )

        rendered = json.dumps(snapshot.to_dict())

        self.assertIn('"schema_version": "1.0"', rendered)

    def test_naive_timestamp_is_normalized_to_utc(self) -> None:
        naive = datetime(2026, 8, 4, 12, 0)

        snapshot = DashboardSnapshotBuilder().build(
            discovery=self.discovery,
            repository_index=self.index,
            aggregation=self.aggregation,
            kpis=self.kpis,
            generated_at=naive,
        )

        self.assertEqual(UTC, snapshot.metadata.generated_at.tzinfo)


if __name__ == "__main__":
    unittest.main()
