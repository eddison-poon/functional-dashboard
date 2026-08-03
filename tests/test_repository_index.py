"""Tests for the Phase 3.2 relationship-aware repository index."""

from __future__ import annotations

import unittest
from pathlib import Path

from dashboard_engine.discovery import (
    AssetKind,
    DiscoveredAsset,
    DiscoveryReport,
    ReviewState,
)
from dashboard_engine.indexing import RepositoryIndexBuilder


def asset(
    asset_id: str | None,
    kind: AssetKind,
    *,
    path: str,
    metadata: dict | None = None,
    title: str | None = None,
    state: ReviewState = ReviewState.PENDING_REVIEW,
) -> DiscoveredAsset:
    return DiscoveredAsset(
        path=Path("/repo") / path,
        relative_path=path,
        asset_kind=kind,
        review_state=state,
        asset_id=asset_id,
        title=title,
        source_format="markdown",
        metadata=metadata or {},
    )


def report(*assets: DiscoveredAsset) -> DiscoveryReport:
    return DiscoveryReport(
        repository_root=Path("/repo"),
        assets=tuple(assets),
        issues=(),
        scanned_files=len(assets),
        ignored_files=0,
    )


class RepositoryIndexBuilderTests(unittest.TestCase):
    def test_links_multiple_manual_and_automation_tests_to_one_scenario(self) -> None:
        scenario = asset(
            "MCP-JIRA-001",
            AssetKind.BUSINESS_SCENARIO,
            path="test_cases/pending_review/scenarios/scenario.md",
        )
        manual_1 = asset(
            "MCP-JIRA-M-001",
            AssetKind.MANUAL_TEST,
            path="test_cases/pending_review/manual/manual-1.md",
            metadata={"parent_scenario_id": "MCP-JIRA-001"},
        )
        manual_2 = asset(
            "MCP-JIRA-M-002",
            AssetKind.MANUAL_TEST,
            path="test_cases/pending_review/manual/manual-2.md",
            metadata={"business_scenario_id": "MCP-JIRA-001"},
        )
        automation = asset(
            "MCP-JIRA-A-001",
            AssetKind.AUTOMATION_TEST,
            path="test_cases/pending_review/automation/auto.md",
            metadata={"scenario_id": "MCP-JIRA-001"},
        )

        index = RepositoryIndexBuilder().build(
            report(scenario, manual_1, manual_2, automation)
        )

        self.assertTrue(index.is_clean)
        indexed_scenario = index.scenario_by_id["MCP-JIRA-001"]
        self.assertEqual(2, len(indexed_scenario.manual_tests))
        self.assertEqual(1, len(indexed_scenario.automation_tests))
        self.assertTrue(indexed_scenario.has_manual)
        self.assertTrue(indexed_scenario.has_automation)

    def test_allows_scenario_without_test_definitions(self) -> None:
        scenario = asset(
            "MCP-JIRA-002",
            AssetKind.BUSINESS_SCENARIO,
            path="test_cases/pending_review/scenarios/scenario.md",
        )

        index = RepositoryIndexBuilder().build(report(scenario))

        self.assertTrue(index.is_clean)
        indexed_scenario = index.scenario_by_id["MCP-JIRA-002"]
        self.assertFalse(indexed_scenario.has_manual)
        self.assertFalse(indexed_scenario.has_automation)

    def test_reports_missing_parent_scenario_id(self) -> None:
        test_definition = asset(
            "MCP-JIRA-M-003",
            AssetKind.MANUAL_TEST,
            path="test_cases/pending_review/manual/manual.md",
        )

        index = RepositoryIndexBuilder().build(report(test_definition))

        self.assertIn(
            "MISSING_PARENT_SCENARIO_ID",
            [issue.code for issue in index.issues],
        )
        self.assertEqual(0, len(index.test_definitions))

    def test_reports_orphan_test_definition(self) -> None:
        test_definition = asset(
            "MCP-JIRA-A-003",
            AssetKind.AUTOMATION_TEST,
            path="test_cases/pending_review/automation/auto.md",
            metadata={"parent_scenario_id": "MCP-JIRA-999"},
        )

        index = RepositoryIndexBuilder().build(report(test_definition))

        self.assertIn(
            "ORPHAN_TEST_DEFINITION",
            [issue.code for issue in index.issues],
        )

    def test_reports_duplicate_test_definition_id(self) -> None:
        scenario = asset(
            "MCP-JIRA-004",
            AssetKind.BUSINESS_SCENARIO,
            path="test_cases/pending_review/scenarios/scenario.md",
        )
        first = asset(
            "MCP-JIRA-M-004",
            AssetKind.MANUAL_TEST,
            path="test_cases/pending_review/manual/first.md",
            metadata={"scenario_id": "MCP-JIRA-004"},
        )
        second = asset(
            "MCP-JIRA-M-004",
            AssetKind.MANUAL_TEST,
            path="test_cases/reviewed/manual/second.md",
            metadata={"scenario_id": "MCP-JIRA-004"},
        )

        index = RepositoryIndexBuilder().build(report(scenario, first, second))

        self.assertIn(
            "DUPLICATE_TEST_DEFINITION_ID",
            [issue.code for issue in index.issues],
        )
        self.assertEqual(1, len(index.test_definitions))

    def test_supports_multiple_scenarios(self) -> None:
        scenario_1 = asset(
            "S-001",
            AssetKind.BUSINESS_SCENARIO,
            path="test_cases/pending_review/scenarios/s1.md",
        )
        scenario_2 = asset(
            "S-002",
            AssetKind.BUSINESS_SCENARIO,
            path="test_cases/pending_review/scenarios/s2.md",
        )
        manual = asset(
            "M-001",
            AssetKind.MANUAL_TEST,
            path="test_cases/pending_review/manual/m1.md",
            metadata={"scenario_id": "S-002"},
        )

        index = RepositoryIndexBuilder().build(report(scenario_1, scenario_2, manual))

        self.assertEqual(2, len(index.scenarios))
        self.assertEqual(0, len(index.scenario_by_id["S-001"].manual_tests))
        self.assertEqual(1, len(index.scenario_by_id["S-002"].manual_tests))

    def test_index_serialization_contains_relationships_and_counts(self) -> None:
        scenario = asset(
            "S-010",
            AssetKind.BUSINESS_SCENARIO,
            path="test_cases/pending_review/scenarios/s10.md",
        )
        manual = asset(
            "M-010",
            AssetKind.MANUAL_TEST,
            path="test_cases/pending_review/manual/m10.md",
            metadata={"parent_scenario_id": "S-010"},
        )

        payload = RepositoryIndexBuilder().build(report(scenario, manual)).to_dict()

        self.assertEqual(1, payload["counts"]["scenarios"])
        self.assertEqual(1, payload["counts"]["manual_tests"])
        self.assertEqual(
            "M-010",
            payload["scenarios"][0]["manual_tests"][0]["asset_id"],
        )


if __name__ == "__main__":
    unittest.main()
