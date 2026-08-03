"""Build a relationship-aware repository index from Phase 3.1 discovery."""

from __future__ import annotations

from collections import defaultdict

from dashboard_engine.discovery import (
    AssetKind,
    DiscoveredAsset,
    DiscoveryReport,
)

from .metadata import extract_parent_scenario_id
from .models import (
    IndexedScenario,
    IndexedTestDefinition,
    RepositoryIndex,
    RepositoryIndexIssue,
)


class RepositoryIndexBuilder:
    """Build Scenario-to-Test Definition relationships from discovered assets."""

    def build(self, discovery_report: DiscoveryReport) -> RepositoryIndex:
        issues: list[RepositoryIndexIssue] = []
        ignored_assets: list[DiscoveredAsset] = []

        scenario_assets: dict[str, DiscoveredAsset] = {}
        candidate_tests: list[DiscoveredAsset] = []

        for asset in discovery_report.assets:
            if asset.asset_kind is AssetKind.BUSINESS_SCENARIO:
                if not asset.asset_id:
                    issues.append(
                        self._issue(
                            asset,
                            "SCENARIO_WITHOUT_ID",
                            "Business Scenario cannot be indexed without an asset ID.",
                        )
                    )
                    ignored_assets.append(asset)
                    continue

                if asset.asset_id in scenario_assets:
                    issues.append(
                        self._issue(
                            asset,
                            "DUPLICATE_SCENARIO_ID",
                            f"Business Scenario ID {asset.asset_id!r} appears more than once.",
                        )
                    )
                    ignored_assets.append(asset)
                    continue

                scenario_assets[asset.asset_id] = asset

            elif asset.asset_kind in {
                AssetKind.MANUAL_TEST,
                AssetKind.AUTOMATION_TEST,
            }:
                candidate_tests.append(asset)

            else:
                ignored_assets.append(asset)
                issues.append(
                    self._issue(
                        asset,
                        "UNSUPPORTED_ASSET_KIND",
                        "Asset kind is not supported by the Phase 3.2 index.",
                    )
                )

        indexed_tests: list[IndexedTestDefinition] = []
        tests_by_scenario: dict[str, list[IndexedTestDefinition]] = defaultdict(list)
        seen_test_ids: set[str] = set()

        for asset in candidate_tests:
            if not asset.asset_id:
                issues.append(
                    self._issue(
                        asset,
                        "TEST_DEFINITION_WITHOUT_ID",
                        "Test Definition cannot be indexed without an asset ID.",
                    )
                )
                ignored_assets.append(asset)
                continue

            if asset.asset_id in seen_test_ids:
                issues.append(
                    self._issue(
                        asset,
                        "DUPLICATE_TEST_DEFINITION_ID",
                        f"Test Definition ID {asset.asset_id!r} appears more than once.",
                    )
                )
                ignored_assets.append(asset)
                continue

            parent_scenario_id = extract_parent_scenario_id(asset.metadata)
            if not parent_scenario_id:
                issues.append(
                    self._issue(
                        asset,
                        "MISSING_PARENT_SCENARIO_ID",
                        "Test Definition does not reference a parent Business Scenario ID.",
                    )
                )
                ignored_assets.append(asset)
                continue

            if parent_scenario_id not in scenario_assets:
                issues.append(
                    self._issue(
                        asset,
                        "ORPHAN_TEST_DEFINITION",
                        (
                            f"Parent Business Scenario {parent_scenario_id!r} "
                            "was not found in the discovery report."
                        ),
                    )
                )
                ignored_assets.append(asset)
                continue

            indexed = IndexedTestDefinition(
                asset_id=asset.asset_id,
                parent_scenario_id=parent_scenario_id,
                title=asset.title,
                asset_kind=asset.asset_kind,
                review_state=asset.review_state,
                relative_path=asset.relative_path,
                source_asset=asset,
            )
            seen_test_ids.add(asset.asset_id)
            indexed_tests.append(indexed)
            tests_by_scenario[parent_scenario_id].append(indexed)

        scenarios: list[IndexedScenario] = []
        for scenario_id, asset in sorted(scenario_assets.items()):
            linked = sorted(
                tests_by_scenario.get(scenario_id, []),
                key=lambda item: (item.asset_kind.value, item.asset_id),
            )
            manual_tests = tuple(
                item
                for item in linked
                if item.asset_kind is AssetKind.MANUAL_TEST
            )
            automation_tests = tuple(
                item
                for item in linked
                if item.asset_kind is AssetKind.AUTOMATION_TEST
            )

            scenarios.append(
                IndexedScenario(
                    asset_id=scenario_id,
                    title=asset.title,
                    review_state=asset.review_state,
                    relative_path=asset.relative_path,
                    manual_tests=manual_tests,
                    automation_tests=automation_tests,
                    source_asset=asset,
                )
            )

        indexed_tests.sort(key=lambda item: (item.parent_scenario_id, item.asset_id))

        return RepositoryIndex(
            scenarios=tuple(scenarios),
            test_definitions=tuple(indexed_tests),
            issues=tuple(issues),
            ignored_assets=tuple(ignored_assets),
        )

    @staticmethod
    def _issue(
        asset: DiscoveredAsset,
        code: str,
        message: str,
    ) -> RepositoryIndexIssue:
        return RepositoryIndexIssue(
            code=code,
            message=message,
            asset_id=asset.asset_id,
            relative_path=asset.relative_path,
        )
