"""Unit tests for Manual and Automation coverage reporting."""

import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.enums import (  # noqa: E402
    AutomationFramework,
)
from canonical.scenario import Scenario  # noqa: E402
from canonical.test_definition import (  # noqa: E402
    TestDefinition,
    TestStep,
)
from repositories.base import (  # noqa: E402
    RepositoryValidationError,
)
from repositories.scenario_repository import (  # noqa: E402
    ScenarioRepository,
)
from repositories.test_definition_repository import (  # noqa: E402
    TestDefinitionRepository,
)
from services.coverage_summary import (  # noqa: E402
    CoverageSummaryService,
    FrameworkCoverage,
    TestCoverageSummary,
)


def scenario(
    scenario_id: str,
    *,
    feature_id: str = "FEATURE-A",
    active: bool = True,
) -> Scenario:
    """Create a valid canonical Scenario."""
    return Scenario(
        scenario_id=scenario_id,
        feature_id=feature_id,
        requirement_ids=[f"REQ-{scenario_id}"],
        name=f"Scenario {scenario_id}",
        scenario_type="POSITIVE",
        priority="HIGH",
        description="Functional business behaviour.",
        expected_outcome="Expected result is achieved.",
        active=active,
    )


def manual_test(
    test_definition_id: str,
    *,
    scenario_id: str,
    status: str = "ACTIVE",
) -> TestDefinition:
    """Create a valid Manual Test Definition."""
    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="MANUAL",
        name=f"Manual test {test_definition_id}",
        status=status,
        version="1.0",
        steps=[
            TestStep(
                step_number=1,
                action="Perform the test action.",
                expected_result="The expected result occurs.",
            )
        ],
    )


def automation_test(
    test_definition_id: str,
    *,
    scenario_id: str,
    status: str = "ACTIVE",
    framework: str = "PLAYWRIGHT",
    repository: str | None = "functional-tests",
    pipeline_name: str | None = "functional-regression",
) -> TestDefinition:
    """Create a valid Automation Test Definition."""
    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="AUTOMATION",
        name=f"Automation test {test_definition_id}",
        status=status,
        version="1.0",
        framework=framework,
        repository=repository,
        script_path=(
            f"tests/{test_definition_id.lower()}.py"
        ),
        pipeline_name=pipeline_name,
    )


class FrameworkCoverageTests(unittest.TestCase):
    """Tests covering framework coverage values."""

    def test_to_dict(self) -> None:
        coverage = FrameworkCoverage(
            framework=AutomationFramework.PLAYWRIGHT,
            test_definition_count=3,
        )

        self.assertEqual(
            coverage.to_dict(),
            {
                "framework": "PLAYWRIGHT",
                "test_definition_count": 3,
            },
        )

    def test_invalid_framework_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            FrameworkCoverage(  # type: ignore[arg-type]
                framework="PLAYWRIGHT",
                test_definition_count=1,
            )

    def test_negative_count_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            FrameworkCoverage(
                framework=AutomationFramework.PLAYWRIGHT,
                test_definition_count=-1,
            )


class TestCoverageSummaryModelTests(unittest.TestCase):
    """Tests covering the immutable summary model."""

    def valid_summary(self) -> TestCoverageSummary:
        """Return a consistent example summary."""
        return TestCoverageSummary(
            active_only=True,
            total_scenarios=4,
            covered_scenarios=3,
            uncovered_scenarios=1,
            manual_covered_scenarios=2,
            automation_covered_scenarios=2,
            dual_covered_scenarios=1,
            manual_only_scenarios=1,
            automation_only_scenarios=1,
            total_test_definitions=4,
            manual_test_definitions=2,
            automation_test_definitions=2,
            automation_with_repository=1,
            automation_without_repository=1,
            automation_with_pipeline=1,
            automation_without_pipeline=1,
            scenario_coverage_percentage=75.0,
            manual_coverage_percentage=50.0,
            automation_coverage_percentage=50.0,
            dual_coverage_percentage=25.0,
            automation_pipeline_readiness_percentage=50.0,
            automation_repository_readiness_percentage=50.0,
            framework_coverage=(
                FrameworkCoverage(
                    framework=(
                        AutomationFramework.PLAYWRIGHT
                    ),
                    test_definition_count=2,
                ),
            ),
            uncovered_scenario_ids=("SCN-004",),
            manual_only_scenario_ids=("SCN-002",),
            automation_only_scenario_ids=("SCN-003",),
        )

    def test_automation_backlog(self) -> None:
        summary = self.valid_summary()

        self.assertEqual(summary.automation_backlog, 1)

    def test_full_coverage_properties_are_false(
        self,
    ) -> None:
        summary = self.valid_summary()

        self.assertFalse(
            summary.has_full_scenario_coverage
        )
        self.assertFalse(
            summary.has_full_manual_coverage
        )
        self.assertFalse(
            summary.has_full_automation_coverage
        )

    def test_to_dict(self) -> None:
        result = self.valid_summary().to_dict()

        self.assertEqual(result["total_scenarios"], 4)
        self.assertEqual(result["automation_backlog"], 1)
        self.assertEqual(
            result["framework_coverage"],
            [
                {
                    "framework": "PLAYWRIGHT",
                    "test_definition_count": 2,
                }
            ],
        )
        self.assertEqual(
            result["uncovered_scenario_ids"],
            ["SCN-004"],
        )

    def test_inconsistent_scenario_total_is_rejected(
        self,
    ) -> None:
        summary = self.valid_summary()

        with self.assertRaises(
            RepositoryValidationError
        ):
            TestCoverageSummary(
                **{
                    **summary.__dict__,
                    "covered_scenarios": 4,
                }
            )

    def test_unsorted_identifier_collection_is_rejected(
        self,
    ) -> None:
        summary = self.valid_summary()

        values = {
            field_name: getattr(summary, field_name)
            for field_name in summary.__dataclass_fields__
        }
        values["uncovered_scenario_ids"] = (
            "SCN-004",
            "SCN-001",
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            TestCoverageSummary(**values)


class CoverageSummaryServiceValidationTests(
    unittest.TestCase
):
    """Tests covering service dependency validation."""

    def test_scenario_repository_is_required(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            CoverageSummaryService(  # type: ignore[arg-type]
                scenario_repository={},
                test_definition_repository=(
                    TestDefinitionRepository()
                ),
            )

    def test_test_definition_repository_is_required(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            CoverageSummaryService(  # type: ignore[arg-type]
                scenario_repository=ScenarioRepository(),
                test_definition_repository={},
            )

    def test_active_only_must_be_boolean(self) -> None:
        service = CoverageSummaryService(
            ScenarioRepository(),
            TestDefinitionRepository(),
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            service.summarize(  # type: ignore[arg-type]
                active_only="yes"
            )


class CoverageSummaryFixtureTests(unittest.TestCase):
    """Shared Manual and Automation coverage fixture."""

    def setUp(self) -> None:
        self.scenarios = ScenarioRepository()
        self.test_definitions = TestDefinitionRepository()

        self.service = CoverageSummaryService(
            scenario_repository=self.scenarios,
            test_definition_repository=(
                self.test_definitions
            ),
        )

        self.scenarios.add_many(
            [
                scenario(
                    "SCN-001",
                    feature_id="FEATURE-A",
                ),
                scenario(
                    "SCN-002",
                    feature_id="FEATURE-A",
                ),
                scenario(
                    "SCN-003",
                    feature_id="FEATURE-B",
                ),
                scenario(
                    "SCN-004",
                    feature_id="FEATURE-B",
                ),
            ]
        )

        self.test_definitions.add_many(
            [
                manual_test(
                    "TEST-MANUAL-001",
                    scenario_id="SCN-001",
                ),
                automation_test(
                    "TEST-AUTO-001",
                    scenario_id="SCN-001",
                    framework="PLAYWRIGHT",
                ),
                manual_test(
                    "TEST-MANUAL-002",
                    scenario_id="SCN-002",
                ),
                automation_test(
                    "TEST-AUTO-003",
                    scenario_id="SCN-003",
                    framework="PYTEST",
                    repository=None,
                    pipeline_name=None,
                ),
            ]
        )


class CoverageCalculationTests(
    CoverageSummaryFixtureTests
):
    """Tests covering primary Scenario coverage metrics."""

    def test_scenario_coverage_counts(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.total_scenarios, 4)
        self.assertEqual(summary.covered_scenarios, 3)
        self.assertEqual(summary.uncovered_scenarios, 1)

    def test_manual_and_automation_counts(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.manual_covered_scenarios,
            2,
        )
        self.assertEqual(
            summary.automation_covered_scenarios,
            2,
        )
        self.assertEqual(
            summary.dual_covered_scenarios,
            1,
        )
        self.assertEqual(
            summary.manual_only_scenarios,
            1,
        )
        self.assertEqual(
            summary.automation_only_scenarios,
            1,
        )

    def test_scenario_identifier_lists(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.uncovered_scenario_ids,
            ("SCN-004",),
        )
        self.assertEqual(
            summary.manual_only_scenario_ids,
            ("SCN-002",),
        )
        self.assertEqual(
            summary.automation_only_scenario_ids,
            ("SCN-003",),
        )

    def test_coverage_percentages(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.scenario_coverage_percentage,
            75.0,
        )
        self.assertEqual(
            summary.manual_coverage_percentage,
            50.0,
        )
        self.assertEqual(
            summary.automation_coverage_percentage,
            50.0,
        )
        self.assertEqual(
            summary.dual_coverage_percentage,
            25.0,
        )

    def test_test_definition_counts(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.total_test_definitions,
            4,
        )
        self.assertEqual(
            summary.manual_test_definitions,
            2,
        )
        self.assertEqual(
            summary.automation_test_definitions,
            2,
        )

    def test_automation_backlog(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.automation_backlog, 1)


class AutomationReadinessTests(
    CoverageSummaryFixtureTests
):
    """Tests covering Automation implementation readiness."""

    def test_repository_readiness(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.automation_with_repository,
            1,
        )
        self.assertEqual(
            summary.automation_without_repository,
            1,
        )
        self.assertEqual(
            summary
            .automation_repository_readiness_percentage,
            50.0,
        )

    def test_pipeline_readiness(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.automation_with_pipeline,
            1,
        )
        self.assertEqual(
            summary.automation_without_pipeline,
            1,
        )
        self.assertEqual(
            summary
            .automation_pipeline_readiness_percentage,
            50.0,
        )

    def test_framework_coverage_is_sorted(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.framework_coverage,
            (
                FrameworkCoverage(
                    framework=(
                        AutomationFramework.PLAYWRIGHT
                    ),
                    test_definition_count=1,
                ),
                FrameworkCoverage(
                    framework=AutomationFramework.PYTEST,
                    test_definition_count=1,
                ),
            ),
        )


class CoverageActiveOnlyTests(
    CoverageSummaryFixtureTests
):
    """Tests covering active-only reporting policy."""

    def setUp(self) -> None:
        super().setUp()

        self.scenarios.add(
            scenario(
                "SCN-INACTIVE",
                active=False,
            )
        )

        self.test_definitions.add_many(
            [
                manual_test(
                    "TEST-DRAFT",
                    scenario_id="SCN-004",
                    status="DRAFT",
                ),
                automation_test(
                    "TEST-INACTIVE-SCENARIO",
                    scenario_id="SCN-INACTIVE",
                    status="ACTIVE",
                ),
            ]
        )

    def test_default_excludes_inactive_scenario(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.total_scenarios, 4)
        self.assertNotIn(
            "SCN-INACTIVE",
            summary.uncovered_scenario_ids,
        )

    def test_default_excludes_non_active_test_definition(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertIn(
            "SCN-004",
            summary.uncovered_scenario_ids,
        )

    def test_active_only_false_includes_all_records(
        self,
    ) -> None:
        summary = self.service.summarize(
            active_only=False
        )

        self.assertEqual(summary.total_scenarios, 5)
        self.assertEqual(summary.covered_scenarios, 5)
        self.assertEqual(summary.uncovered_scenarios, 0)
        self.assertEqual(
            summary.total_test_definitions,
            6,
        )


class CoverageFeatureGroupingTests(
    CoverageSummaryFixtureTests
):
    """Tests covering feature-level summaries."""

    def test_summarize_by_feature(self) -> None:
        summaries = self.service.summarize_by_feature()

        self.assertEqual(
            tuple(summaries),
            (
                "FEATURE-A",
                "FEATURE-B",
            ),
        )

    def test_feature_a_has_full_coverage(self) -> None:
        summary = self.service.summarize_by_feature()[
            "FEATURE-A"
        ]

        self.assertEqual(summary.total_scenarios, 2)
        self.assertEqual(summary.covered_scenarios, 2)
        self.assertTrue(
            summary.has_full_scenario_coverage
        )

    def test_feature_b_has_one_uncovered_scenario(
        self,
    ) -> None:
        summary = self.service.summarize_by_feature()[
            "FEATURE-B"
        ]

        self.assertEqual(summary.total_scenarios, 2)
        self.assertEqual(summary.covered_scenarios, 1)
        self.assertEqual(
            summary.uncovered_scenario_ids,
            ("SCN-004",),
        )


class CoverageScenarioSubsetTests(
    CoverageSummaryFixtureTests
):
    """Tests covering requested Scenario subsets."""

    def test_summarize_requested_scenarios(self) -> None:
        summary = (
            self.service
            .summarize_for_scenario_ids(
                [
                    "SCN-001",
                    "SCN-004",
                ]
            )
        )

        self.assertEqual(summary.total_scenarios, 2)
        self.assertEqual(summary.covered_scenarios, 1)
        self.assertEqual(
            summary.uncovered_scenario_ids,
            ("SCN-004",),
        )

    def test_unknown_ids_are_not_included(self) -> None:
        summary = (
            self.service
            .summarize_for_scenario_ids(
                ["SCN-MISSING"]
            )
        )

        self.assertTrue(summary.is_empty)
        self.assertEqual(summary.total_scenarios, 0)

    def test_duplicate_ids_are_deduplicated(
        self,
    ) -> None:
        summary = (
            self.service
            .summarize_for_scenario_ids(
                [
                    "SCN-001",
                    "SCN-001",
                ]
            )
        )

        self.assertEqual(summary.total_scenarios, 1)

    def test_scenario_id_matching_is_case_sensitive(
        self,
    ) -> None:
        summary = (
            self.service
            .summarize_for_scenario_ids(
                ["scn-001"]
            )
        )

        self.assertTrue(summary.is_empty)

    def test_string_instead_of_collection_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.summarize_for_scenario_ids(
                "SCN-001"  # type: ignore[arg-type]
            )

    def test_empty_collection_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.summarize_for_scenario_ids(
                []
            )

    def test_blank_identifier_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.summarize_for_scenario_ids(
                [" "]
            )


class CoverageFullCoverageTests(unittest.TestCase):
    """Tests covering complete Manual and Automation coverage."""

    def test_full_dual_coverage(self) -> None:
        scenarios = ScenarioRepository()
        definitions = TestDefinitionRepository()

        scenarios.add(
            scenario("SCN-001")
        )
        definitions.add_many(
            [
                manual_test(
                    "TEST-MANUAL-001",
                    scenario_id="SCN-001",
                ),
                automation_test(
                    "TEST-AUTO-001",
                    scenario_id="SCN-001",
                ),
            ]
        )

        summary = CoverageSummaryService(
            scenarios,
            definitions,
        ).summarize()

        self.assertTrue(
            summary.has_full_scenario_coverage
        )
        self.assertTrue(
            summary.has_full_manual_coverage
        )
        self.assertTrue(
            summary.has_full_automation_coverage
        )
        self.assertEqual(
            summary.dual_coverage_percentage,
            100.0,
        )


class CoverageEmptyRepositoryTests(unittest.TestCase):
    """Tests covering empty coverage data."""

    def setUp(self) -> None:
        self.service = CoverageSummaryService(
            ScenarioRepository(),
            TestDefinitionRepository(),
        )

    def test_empty_summary(self) -> None:
        summary = self.service.summarize()

        self.assertTrue(summary.is_empty)
        self.assertEqual(summary.total_scenarios, 0)
        self.assertEqual(summary.covered_scenarios, 0)
        self.assertEqual(
            summary.scenario_coverage_percentage,
            0.0,
        )
        self.assertFalse(
            summary.has_full_scenario_coverage
        )

    def test_empty_feature_summary(self) -> None:
        self.assertEqual(
            self.service.summarize_by_feature(),
            {},
        )


if __name__ == "__main__":
    unittest.main()
