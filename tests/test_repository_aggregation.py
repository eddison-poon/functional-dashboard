"""Tests for the Phase 3.3 repository aggregation engine."""

from __future__ import annotations

import unittest
from pathlib import Path

from dashboard_engine.aggregation import RepositoryAggregator
from dashboard_engine.discovery import AssetKind, DiscoveredAsset, ReviewState
from dashboard_engine.indexing import (
    IndexedScenario,
    IndexedTestDefinition,
    RepositoryIndex,
    RepositoryIndexIssue,
)


def source_asset(
    asset_id: str,
    kind: AssetKind,
    state: ReviewState,
    path: str,
) -> DiscoveredAsset:
    return DiscoveredAsset(
        path=Path("/repo") / path,
        relative_path=path,
        asset_kind=kind,
        review_state=state,
        asset_id=asset_id,
        title=asset_id,
        source_format="markdown",
        metadata={},
    )


def test_definition(
    asset_id: str,
    parent_id: str,
    kind: AssetKind,
    state: ReviewState,
) -> IndexedTestDefinition:
    path = f"test_cases/{state.value}/{kind.value}/{asset_id}.md"
    return IndexedTestDefinition(
        asset_id=asset_id,
        parent_scenario_id=parent_id,
        title=asset_id,
        asset_kind=kind,
        review_state=state,
        relative_path=path,
        source_asset=source_asset(asset_id, kind, state, path),
    )


def scenario(
    asset_id: str,
    state: ReviewState,
    manual_tests: tuple[IndexedTestDefinition, ...] = (),
    automation_tests: tuple[IndexedTestDefinition, ...] = (),
) -> IndexedScenario:
    path = f"test_cases/{state.value}/scenarios/{asset_id}.md"
    return IndexedScenario(
        asset_id=asset_id,
        title=asset_id,
        review_state=state,
        relative_path=path,
        manual_tests=manual_tests,
        automation_tests=automation_tests,
        source_asset=source_asset(
            asset_id,
            AssetKind.BUSINESS_SCENARIO,
            state,
            path,
        ),
    )


class RepositoryAggregatorTests(unittest.TestCase):
    def test_aggregates_asset_lifecycle_counts(self) -> None:
        manual = test_definition(
            "M-001",
            "S-001",
            AssetKind.MANUAL_TEST,
            ReviewState.PENDING_REVIEW,
        )
        automation = test_definition(
            "A-001",
            "S-001",
            AssetKind.AUTOMATION_TEST,
            ReviewState.REVIEWED,
        )
        item = scenario(
            "S-001",
            ReviewState.PUBLISHED,
            manual_tests=(manual,),
            automation_tests=(automation,),
        )
        index = RepositoryIndex(
            scenarios=(item,),
            test_definitions=(manual, automation),
            issues=(),
            ignored_assets=(),
        )

        aggregation = RepositoryAggregator().aggregate(index)

        self.assertEqual(1, aggregation.scenarios.published)
        self.assertEqual(1, aggregation.manual_tests.pending_review)
        self.assertEqual(1, aggregation.automation_tests.reviewed)
        self.assertEqual(2, aggregation.all_test_definitions.total)

    def test_calculates_manual_automation_and_overall_coverage(self) -> None:
        manual = test_definition(
            "M-001",
            "S-001",
            AssetKind.MANUAL_TEST,
            ReviewState.PENDING_REVIEW,
        )
        automation = test_definition(
            "A-001",
            "S-002",
            AssetKind.AUTOMATION_TEST,
            ReviewState.PENDING_REVIEW,
        )
        both_manual = test_definition(
            "M-003",
            "S-003",
            AssetKind.MANUAL_TEST,
            ReviewState.PENDING_REVIEW,
        )
        both_auto = test_definition(
            "A-003",
            "S-003",
            AssetKind.AUTOMATION_TEST,
            ReviewState.PENDING_REVIEW,
        )
        scenarios = (
            scenario("S-001", ReviewState.PENDING_REVIEW, manual_tests=(manual,)),
            scenario(
                "S-002",
                ReviewState.PENDING_REVIEW,
                automation_tests=(automation,),
            ),
            scenario(
                "S-003",
                ReviewState.PENDING_REVIEW,
                manual_tests=(both_manual,),
                automation_tests=(both_auto,),
            ),
            scenario("S-004", ReviewState.PENDING_REVIEW),
        )
        index = RepositoryIndex(
            scenarios=scenarios,
            test_definitions=(manual, automation, both_manual, both_auto),
            issues=(),
            ignored_assets=(),
        )

        aggregation = RepositoryAggregator().aggregate(index)

        self.assertEqual(50.0, aggregation.manual_coverage.coverage_percentage)
        self.assertEqual(50.0, aggregation.automation_coverage.coverage_percentage)
        self.assertEqual(75.0, aggregation.overall_test_coverage.coverage_percentage)

    def test_calculates_scenario_composition(self) -> None:
        manual = test_definition(
            "M-001",
            "S-001",
            AssetKind.MANUAL_TEST,
            ReviewState.PENDING_REVIEW,
        )
        automation = test_definition(
            "A-002",
            "S-002",
            AssetKind.AUTOMATION_TEST,
            ReviewState.PENDING_REVIEW,
        )
        both_manual = test_definition(
            "M-003",
            "S-003",
            AssetKind.MANUAL_TEST,
            ReviewState.PENDING_REVIEW,
        )
        both_auto = test_definition(
            "A-003",
            "S-003",
            AssetKind.AUTOMATION_TEST,
            ReviewState.PENDING_REVIEW,
        )
        index = RepositoryIndex(
            scenarios=(
                scenario("S-001", ReviewState.PENDING_REVIEW, manual_tests=(manual,)),
                scenario(
                    "S-002",
                    ReviewState.PENDING_REVIEW,
                    automation_tests=(automation,),
                ),
                scenario(
                    "S-003",
                    ReviewState.PENDING_REVIEW,
                    manual_tests=(both_manual,),
                    automation_tests=(both_auto,),
                ),
                scenario("S-004", ReviewState.PENDING_REVIEW),
            ),
            test_definitions=(manual, automation, both_manual, both_auto),
            issues=(),
            ignored_assets=(),
        )

        composition = RepositoryAggregator().aggregate(index).scenario_composition

        self.assertEqual(1, composition.manual_only)
        self.assertEqual(1, composition.automation_only)
        self.assertEqual(1, composition.manual_and_automation)
        self.assertEqual(1, composition.no_test_definitions)

    def test_handles_empty_repository(self) -> None:
        index = RepositoryIndex(
            scenarios=(),
            test_definitions=(),
            issues=(),
            ignored_assets=(),
        )

        aggregation = RepositoryAggregator().aggregate(index)

        self.assertEqual(0, aggregation.scenarios.total)
        self.assertEqual(0.0, aggregation.manual_coverage.coverage_percentage)
        self.assertEqual(0.0, aggregation.overall_test_coverage.coverage_percentage)

    def test_preserves_upstream_quality_counts(self) -> None:
        ignored = source_asset(
            "UNKNOWN-001",
            AssetKind.UNKNOWN,
            ReviewState.UNKNOWN,
            "test_cases/misc/unknown.md",
        )
        index = RepositoryIndex(
            scenarios=(),
            test_definitions=(),
            issues=(
                RepositoryIndexIssue(
                    code="ORPHAN_TEST_DEFINITION",
                    message="Example issue",
                ),
            ),
            ignored_assets=(ignored,),
        )

        aggregation = RepositoryAggregator().aggregate(index)

        self.assertEqual(1, aggregation.indexing_issue_count)
        self.assertEqual(1, aggregation.ignored_asset_count)

    def test_serialization_is_json_compatible(self) -> None:
        index = RepositoryIndex(
            scenarios=(),
            test_definitions=(),
            issues=(),
            ignored_assets=(),
        )

        payload = RepositoryAggregator().aggregate(index).to_dict()

        self.assertIn("assets", payload)
        self.assertIn("coverage", payload)
        self.assertIn("scenario_composition", payload)
        self.assertIn("quality", payload)


if __name__ == "__main__":
    unittest.main()
