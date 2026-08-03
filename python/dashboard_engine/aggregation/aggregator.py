"""Aggregate repository-index contents into management-ready summary counts."""

from __future__ import annotations

from collections.abc import Iterable

from dashboard_engine.discovery import AssetKind, ReviewState
from dashboard_engine.indexing import (
    IndexedScenario,
    IndexedTestDefinition,
    RepositoryIndex,
)

from .models import (
    AssetLifecycleSummary,
    CoverageSummary,
    RepositoryAggregation,
    ScenarioCompositionSummary,
)


class RepositoryAggregator:
    """Create Phase 3.3 summaries from a Phase 3.2 RepositoryIndex."""

    def aggregate(self, index: RepositoryIndex) -> RepositoryAggregation:
        scenarios = self._scenario_lifecycle(index.scenarios)
        manual_tests = self._test_lifecycle(
            item
            for item in index.test_definitions
            if item.asset_kind is AssetKind.MANUAL_TEST
        )
        automation_tests = self._test_lifecycle(
            item
            for item in index.test_definitions
            if item.asset_kind is AssetKind.AUTOMATION_TEST
        )
        all_test_definitions = self._test_lifecycle(index.test_definitions)

        total_scenarios = len(index.scenarios)
        manual_covered = sum(1 for scenario in index.scenarios if scenario.has_manual)
        automation_covered = sum(
            1 for scenario in index.scenarios if scenario.has_automation
        )
        overall_covered = sum(
            1
            for scenario in index.scenarios
            if scenario.has_manual or scenario.has_automation
        )

        manual_only = sum(
            1
            for scenario in index.scenarios
            if scenario.has_manual and not scenario.has_automation
        )
        automation_only = sum(
            1
            for scenario in index.scenarios
            if scenario.has_automation and not scenario.has_manual
        )
        manual_and_automation = sum(
            1
            for scenario in index.scenarios
            if scenario.has_manual and scenario.has_automation
        )
        no_test_definitions = total_scenarios - overall_covered

        return RepositoryAggregation(
            scenarios=scenarios,
            manual_tests=manual_tests,
            automation_tests=automation_tests,
            all_test_definitions=all_test_definitions,
            manual_coverage=self._coverage(total_scenarios, manual_covered),
            automation_coverage=self._coverage(
                total_scenarios,
                automation_covered,
            ),
            overall_test_coverage=self._coverage(
                total_scenarios,
                overall_covered,
            ),
            scenario_composition=ScenarioCompositionSummary(
                total_scenarios=total_scenarios,
                manual_only=manual_only,
                automation_only=automation_only,
                manual_and_automation=manual_and_automation,
                no_test_definitions=no_test_definitions,
            ),
            indexing_issue_count=len(index.issues),
            ignored_asset_count=len(index.ignored_assets),
        )

    @staticmethod
    def _scenario_lifecycle(
        scenarios: Iterable[IndexedScenario],
    ) -> AssetLifecycleSummary:
        states = [scenario.review_state for scenario in scenarios]
        return RepositoryAggregator._lifecycle(states)

    @staticmethod
    def _test_lifecycle(
        tests: Iterable[IndexedTestDefinition],
    ) -> AssetLifecycleSummary:
        states = [test.review_state for test in tests]
        return RepositoryAggregator._lifecycle(states)

    @staticmethod
    def _lifecycle(states: Iterable[ReviewState]) -> AssetLifecycleSummary:
        values = list(states)
        return AssetLifecycleSummary(
            total=len(values),
            pending_review=sum(
                1 for state in values if state is ReviewState.PENDING_REVIEW
            ),
            reviewed=sum(1 for state in values if state is ReviewState.REVIEWED),
            published=sum(1 for state in values if state is ReviewState.PUBLISHED),
            unknown=sum(1 for state in values if state is ReviewState.UNKNOWN),
        )

    @staticmethod
    def _coverage(total: int, covered: int) -> CoverageSummary:
        return CoverageSummary(
            total_scenarios=total,
            covered_scenarios=covered,
            uncovered_scenarios=total - covered,
        )
