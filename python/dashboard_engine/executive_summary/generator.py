"""Generate management-ready narrative from a Phase 3.5 snapshot."""

from __future__ import annotations

from dashboard_engine.kpi import HealthStatus
from dashboard_engine.snapshot import DashboardSnapshot

from .models import ExecutiveSummary, SummaryHighlight
from .rules import OverallHealthEvaluator


class ExecutiveSummaryGenerator:
    """Create concise management narrative from repository snapshot data."""

    def __init__(
        self,
        *,
        current_phase: str = "Test Design and Review",
        health_evaluator: OverallHealthEvaluator | None = None,
    ) -> None:
        self.current_phase = current_phase
        self.health_evaluator = health_evaluator or OverallHealthEvaluator()

    def generate(self, snapshot: DashboardSnapshot) -> ExecutiveSummary:
        selected_kpis = (
            snapshot.kpis.overall_test_coverage,
            snapshot.kpis.all_test_review_completion,
            snapshot.kpis.repository_data_quality,
        )
        overall_health = self.health_evaluator.evaluate(selected_kpis)

        achievements = self._achievements(snapshot)
        risks = self._risks(snapshot)
        headline = self._headline(snapshot, overall_health)
        readiness = self._readiness(snapshot, overall_health)
        standup = self._standup_update(
            snapshot,
            overall_health,
            achievements,
            risks,
        )

        return ExecutiveSummary(
            current_phase=self.current_phase,
            overall_health=overall_health,
            headline=headline,
            achievements=tuple(achievements),
            risks=tuple(risks),
            readiness_assessment=readiness,
            standup_update=standup,
        )

    def _achievements(
        self,
        snapshot: DashboardSnapshot,
    ) -> list[SummaryHighlight]:
        results: list[SummaryHighlight] = []
        summary = snapshot.aggregation

        if summary.scenarios.total:
            results.append(
                SummaryHighlight(
                    category="coverage",
                    message=(
                        f"{summary.overall_test_coverage.covered_scenarios} of "
                        f"{summary.overall_test_coverage.total_scenarios} "
                        "Business Scenarios have at least one linked Test Definition."
                    ),
                )
            )

        reviewed_tests = (
            summary.all_test_definitions.reviewed
            + summary.all_test_definitions.published
        )
        if reviewed_tests:
            results.append(
                SummaryHighlight(
                    category="review",
                    message=(
                        f"{reviewed_tests} of "
                        f"{summary.all_test_definitions.total} Test Definitions "
                        "are reviewed or published."
                    ),
                )
            )

        if snapshot.quality.is_clean:
            results.append(
                SummaryHighlight(
                    category="quality",
                    message="Repository discovery and indexing completed without quality issues.",
                )
            )

        return results[:3]

    def _risks(
        self,
        snapshot: DashboardSnapshot,
    ) -> list[SummaryHighlight]:
        results: list[SummaryHighlight] = []
        summary = snapshot.aggregation

        if summary.overall_test_coverage.uncovered_scenarios:
            results.append(
                SummaryHighlight(
                    category="coverage_gap",
                    message=(
                        f"{summary.overall_test_coverage.uncovered_scenarios} "
                        "Business Scenarios have no linked Manual or Automation Test Definition."
                    ),
                )
            )

        pending_tests = summary.all_test_definitions.pending_review
        if pending_tests:
            results.append(
                SummaryHighlight(
                    category="review_backlog",
                    message=(
                        f"{pending_tests} Test Definitions remain in pending review."
                    ),
                )
            )

        if not snapshot.quality.is_clean:
            results.append(
                SummaryHighlight(
                    category="data_quality",
                    message=(
                        f"{snapshot.quality.total_issue_count} repository quality "
                        "issues require review before the snapshot can be treated as clean."
                    ),
                )
            )

        return results[:3]

    def _headline(
        self,
        snapshot: DashboardSnapshot,
        health: HealthStatus,
    ) -> str:
        coverage = snapshot.kpis.overall_test_coverage.value
        review = snapshot.kpis.all_test_review_completion.value

        if health is HealthStatus.NOT_APPLICABLE:
            return (
                "No repository assets are currently available for management assessment."
            )

        return (
            f"Repository preparation health is {health.value.upper()}: "
            f"overall test coverage is {coverage:.2f}% and "
            f"test review completion is {review:.2f}%."
        )

    def _readiness(
        self,
        snapshot: DashboardSnapshot,
        health: HealthStatus,
    ) -> str:
        if health is HealthStatus.GREEN and snapshot.quality.is_clean:
            return (
                "Repository content is sufficiently prepared to proceed to dashboard "
                "presentation and later execution reporting."
            )
        if health is HealthStatus.AMBER:
            return (
                "Repository content is partially ready. Close remaining coverage or "
                "review gaps before treating the test library as management-ready."
            )
        if health is HealthStatus.RED:
            return (
                "Repository content is not ready for management reliance. Prioritise "
                "coverage gaps, review backlog, and data-quality issues."
            )
        return (
            "Readiness cannot be assessed until Business Scenarios and Test Definitions "
            "are available."
        )

    def _standup_update(
        self,
        snapshot: DashboardSnapshot,
        health: HealthStatus,
        achievements: list[SummaryHighlight],
        risks: list[SummaryHighlight],
    ) -> str:
        yesterday = (
            achievements[0].message
            if achievements
            else "Repository assets were assessed and no completed milestone was identified."
        )
        today = (
            "Continue reviewing pending assets and close remaining Scenario coverage gaps."
        )
        blockers = (
            risks[0].message
            if risks
            else "No current repository blockers were identified."
        )

        return (
            f"Yesterday: {yesterday}\n"
            f"Today: {today}\n"
            f"Blockers: {blockers}\n"
            f"Testing Health: {health.value.upper()}."
        )
