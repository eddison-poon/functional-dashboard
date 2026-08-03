"""Immutable summary models produced by the Phase 3.3 aggregation engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AssetLifecycleSummary:
    """Lifecycle totals for one asset category."""

    total: int
    pending_review: int
    reviewed: int
    published: int
    unknown: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "pending_review": self.pending_review,
            "reviewed": self.reviewed,
            "published": self.published,
            "unknown": self.unknown,
        }


@dataclass(frozen=True, slots=True)
class CoverageSummary:
    """Scenario coverage counts based on linked Test Definitions."""

    total_scenarios: int
    covered_scenarios: int
    uncovered_scenarios: int

    @property
    def coverage_percentage(self) -> float:
        if self.total_scenarios == 0:
            return 0.0
        return round((self.covered_scenarios / self.total_scenarios) * 100, 2)

    def to_dict(self) -> dict[str, int | float]:
        return {
            "total_scenarios": self.total_scenarios,
            "covered_scenarios": self.covered_scenarios,
            "uncovered_scenarios": self.uncovered_scenarios,
            "coverage_percentage": self.coverage_percentage,
        }


@dataclass(frozen=True, slots=True)
class ScenarioCompositionSummary:
    """Breakdown of Scenario test-definition composition."""

    total_scenarios: int
    manual_only: int
    automation_only: int
    manual_and_automation: int
    no_test_definitions: int

    def to_dict(self) -> dict[str, int]:
        return {
            "total_scenarios": self.total_scenarios,
            "manual_only": self.manual_only,
            "automation_only": self.automation_only,
            "manual_and_automation": self.manual_and_automation,
            "no_test_definitions": self.no_test_definitions,
        }


@dataclass(frozen=True, slots=True)
class RepositoryAggregation:
    """Complete Phase 3.3 aggregation result."""

    scenarios: AssetLifecycleSummary
    manual_tests: AssetLifecycleSummary
    automation_tests: AssetLifecycleSummary
    all_test_definitions: AssetLifecycleSummary
    manual_coverage: CoverageSummary
    automation_coverage: CoverageSummary
    overall_test_coverage: CoverageSummary
    scenario_composition: ScenarioCompositionSummary
    indexing_issue_count: int
    ignored_asset_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "assets": {
                "scenarios": self.scenarios.to_dict(),
                "manual_tests": self.manual_tests.to_dict(),
                "automation_tests": self.automation_tests.to_dict(),
                "all_test_definitions": self.all_test_definitions.to_dict(),
            },
            "coverage": {
                "manual": self.manual_coverage.to_dict(),
                "automation": self.automation_coverage.to_dict(),
                "overall": self.overall_test_coverage.to_dict(),
            },
            "scenario_composition": self.scenario_composition.to_dict(),
            "quality": {
                "indexing_issue_count": self.indexing_issue_count,
                "ignored_asset_count": self.ignored_asset_count,
            },
        }
