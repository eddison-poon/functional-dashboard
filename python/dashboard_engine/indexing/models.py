"""Immutable models produced by the Phase 3.2 repository index."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dashboard_engine.discovery import AssetKind, DiscoveredAsset, ReviewState


@dataclass(frozen=True, slots=True)
class RepositoryIndexIssue:
    """A non-fatal indexing or relationship issue."""

    code: str
    message: str
    asset_id: str | None = None
    relative_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "asset_id": self.asset_id,
            "relative_path": self.relative_path,
        }


@dataclass(frozen=True, slots=True)
class IndexedTestDefinition:
    """A Manual or Automation Test Definition linked to a parent Scenario."""

    asset_id: str
    parent_scenario_id: str
    title: str | None
    asset_kind: AssetKind
    review_state: ReviewState
    relative_path: str
    source_asset: DiscoveredAsset

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "parent_scenario_id": self.parent_scenario_id,
            "title": self.title,
            "asset_kind": self.asset_kind.value,
            "review_state": self.review_state.value,
            "relative_path": self.relative_path,
        }


@dataclass(frozen=True, slots=True)
class IndexedScenario:
    """A Business Scenario with its linked Manual and Automation definitions."""

    asset_id: str
    title: str | None
    review_state: ReviewState
    relative_path: str
    manual_tests: tuple[IndexedTestDefinition, ...]
    automation_tests: tuple[IndexedTestDefinition, ...]
    source_asset: DiscoveredAsset

    @property
    def has_manual(self) -> bool:
        return bool(self.manual_tests)

    @property
    def has_automation(self) -> bool:
        return bool(self.automation_tests)

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "title": self.title,
            "review_state": self.review_state.value,
            "relative_path": self.relative_path,
            "has_manual": self.has_manual,
            "has_automation": self.has_automation,
            "manual_tests": [item.to_dict() for item in self.manual_tests],
            "automation_tests": [item.to_dict() for item in self.automation_tests],
        }


@dataclass(frozen=True, slots=True)
class RepositoryIndex:
    """Complete relationship-aware index built from discovered assets."""

    scenarios: tuple[IndexedScenario, ...]
    test_definitions: tuple[IndexedTestDefinition, ...]
    issues: tuple[RepositoryIndexIssue, ...]
    ignored_assets: tuple[DiscoveredAsset, ...]

    @property
    def is_clean(self) -> bool:
        return not self.issues

    @property
    def scenario_by_id(self) -> dict[str, IndexedScenario]:
        return {scenario.asset_id: scenario for scenario in self.scenarios}

    @property
    def test_definition_by_id(self) -> dict[str, IndexedTestDefinition]:
        return {item.asset_id: item for item in self.test_definitions}

    def tests_for_scenario(self, scenario_id: str) -> tuple[IndexedTestDefinition, ...]:
        scenario = self.scenario_by_id.get(scenario_id)
        if scenario is None:
            return ()
        return scenario.manual_tests + scenario.automation_tests

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_clean": self.is_clean,
            "counts": {
                "scenarios": len(self.scenarios),
                "test_definitions": len(self.test_definitions),
                "manual_tests": sum(
                    1
                    for item in self.test_definitions
                    if item.asset_kind is AssetKind.MANUAL_TEST
                ),
                "automation_tests": sum(
                    1
                    for item in self.test_definitions
                    if item.asset_kind is AssetKind.AUTOMATION_TEST
                ),
                "issues": len(self.issues),
                "ignored_assets": len(self.ignored_assets),
            },
            "scenarios": [scenario.to_dict() for scenario in self.scenarios],
            "test_definitions": [
                item.to_dict() for item in self.test_definitions
            ],
            "issues": [issue.to_dict() for issue in self.issues],
            "ignored_assets": [
                {
                    "asset_id": asset.asset_id,
                    "asset_kind": asset.asset_kind.value,
                    "relative_path": asset.relative_path,
                }
                for asset in self.ignored_assets
            ],
        }
