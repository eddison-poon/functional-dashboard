"""Integration and regression tests for Phase 2C reporting services.

These tests exercise the complete reporting flow from canonical
repositories through selection, aggregation, readiness assessment, and
dashboard snapshot serialization.

The suite intentionally uses real repositories and real services rather
than mocks.
"""

import json
import sys
import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.enums import Environment  # noqa: E402
from canonical.execution import Execution  # noqa: E402
from canonical.scenario import Scenario  # noqa: E402
from canonical.test_definition import (  # noqa: E402
    TestDefinition,
    TestStep,
)
from repositories.execution_repository import (  # noqa: E402
    ExecutionRepository,
)
from repositories.scenario_repository import (  # noqa: E402
    ScenarioRepository,
)
from repositories.test_definition_repository import (  # noqa: E402
    TestDefinitionRepository,
)
from services.coverage_summary import (  # noqa: E402
    CoverageSummaryService,
)
from services.dashboard_snapshot import (  # noqa: E402
    DashboardHealth,
    DashboardSnapshot,
    DashboardSnapshotService,
)
from services.environment_summary import (  # noqa: E402
    EnvironmentReadinessService,
    EnvironmentReadinessStatus,
)
from services.execution_selection import (  # noqa: E402
    ExecutionSelectionService,
)
from services.execution_summary import (  # noqa: E402
    ExecutionSummaryService,
)


UTC = timezone.utc

GENERATED_AT = datetime(
    2026,
    7,
    24,
    9,
    0,
    tzinfo=UTC,
)

BASE_TIME = datetime(
    2026,
    7,
    24,
    8,
    0,
    tzinfo=UTC,
)


def create_scenario(
    scenario_id: str,
    *,
    feature_id: str,
    active: bool = True,
) -> Scenario:
    """Create a valid canonical Scenario."""
    return Scenario(
        scenario_id=scenario_id,
        feature_id=feature_id,
        requirement_ids=[],
        name=f"Scenario {scenario_id}",
        scenario_type="POSITIVE",
        priority="HIGH",
        description=(
            f"Business behaviour represented by {scenario_id}."
        ),
        tags=["functional"],
        preconditions=[
            "The application and required test data are available."
        ],
        expected_outcome="The expected business result is achieved.",
        owner="QA Team",
        active=active,
    )


def create_manual_test(
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
        description="Manual functional test.",
        preconditions=[
            "The application is available."
        ],
        steps=[
            TestStep(
                step_number=1,
                action="Perform the required user action.",
                expected_result=(
                    "The expected business result is displayed."
                ),
            )
        ],
        owner="Manual QA",
        tags=["manual"],
    )


def create_automation_test(
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
        description="Automated functional test.",
        preconditions=[
            "The application is available."
        ],
        framework=framework,
        repository=repository,
        script_path=(
            f"tests/{test_definition_id.lower()}.py"
        ),
        pipeline_name=pipeline_name,
        owner="Automation QA",
        tags=["automation"],
    )


def create_execution(
    execution_id: str,
    *,
    test_definition_id: str,
    environment: Environment | str,
    execution_cycle: str,
    status: str,
    build_version: str = "1.0.0",
    started_at: datetime | None = BASE_TIME,
    completed_at: datetime | None = (
        BASE_TIME + timedelta(minutes=5)
    ),
    rerun_of_execution_id: str | None = None,
    defect_ids: tuple[str, ...] = (),
) -> Execution:
    """Create a valid canonical Execution."""
    if status == "NOT_EXECUTED":
        started_at = None
        completed_at = None

    elif status == "IN_PROGRESS":
        if started_at is None:
            started_at = BASE_TIME

        completed_at = None

    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status=status,
        execution_cycle=execution_cycle,
        started_at=started_at,
        completed_at=completed_at,
        executed_by=(
            None
            if status == "NOT_EXECUTED"
            else "QA User"
        ),
        build_version=build_version,
        source_system="TEST_DATA",
        defect_ids=defect_ids,
        evidence_ids=(),
        remarks=None,
        rerun_of_execution_id=rerun_of_execution_id,
    )


@dataclass(frozen=True)
class IntegrationValidationReport:
    """Validation-report test double matching the dashboard protocol."""

    error_count: int = 0
    warning_count: int = 0

    @property
    def is_valid(self) -> bool:
        """Return whether the report contains no errors."""
        return self.error_count == 0

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible validation data."""
        return {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "is_valid": self.is_valid,
            "findings": [],
        }


class ReportingIntegrationFixture(unittest.TestCase):
    """Shared repository and service wiring."""

    def setUp(self) -> None:
        self.scenario_repository = ScenarioRepository()
        self.test_definition_repository = (
            TestDefinitionRepository()
        )
        self.execution_repository = ExecutionRepository()

        self.execution_selection_service = (
            ExecutionSelectionService(
                self.execution_repository
            )
        )

        self.execution_summary_service = (
            ExecutionSummaryService(
                self.execution_selection_service
            )
        )

        self.coverage_summary_service = (
            CoverageSummaryService(
                scenario_repository=(
                    self.scenario_repository
                ),
                test_definition_repository=(
                    self.test_definition_repository
                ),
            )
        )

        self.environment_readiness_service = (
            EnvironmentReadinessService(
                execution_selection_service=(
                    self.execution_selection_service
                ),
                execution_summary_service=(
                    self.execution_summary_service
                ),
            )
        )

        self.dashboard_snapshot_service = (
            DashboardSnapshotService(
                execution_summary_service=(
                    self.execution_summary_service
                ),
                coverage_summary_service=(
                    self.coverage_summary_service
                ),
                environment_readiness_service=(
                    self.environment_readiness_service
                ),
            )
        )

    def build_snapshot(
        self,
        *,
        cycle: str = "Release 1",
        environments: tuple[str, ...] = (
            "SIT",
            "UAT",
        ),
        validation_report: (
            IntegrationValidationReport | None
        ) = None,
    ) -> DashboardSnapshot:
        """Build a snapshot using the wired real services."""
        return self.dashboard_snapshot_service.build(
            generated_at=GENERATED_AT,
            execution_cycle=cycle,
            environments=environments,
            validation_report=validation_report,
        )


class GreenReportingIntegrationTests(
    ReportingIntegrationFixture
):
    """Verify a complete healthy reporting flow."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add_many(
            [
                create_scenario(
                    "SCN-LOGIN",
                    feature_id="FEATURE-AUTH",
                ),
                create_scenario(
                    "SCN-LOGOUT",
                    feature_id="FEATURE-AUTH",
                ),
            ]
        )

        self.test_definition_repository.add_many(
            [
                create_manual_test(
                    "TEST-MANUAL-LOGIN",
                    scenario_id="SCN-LOGIN",
                ),
                create_automation_test(
                    "TEST-AUTO-LOGIN",
                    scenario_id="SCN-LOGIN",
                ),
                create_manual_test(
                    "TEST-MANUAL-LOGOUT",
                    scenario_id="SCN-LOGOUT",
                ),
                create_automation_test(
                    "TEST-AUTO-LOGOUT",
                    scenario_id="SCN-LOGOUT",
                ),
            ]
        )

        executions: list[Execution] = []

        for environment in ("SIT", "UAT"):
            executions.extend(
                [
                    create_execution(
                        f"EXEC-{environment}-MANUAL-LOGIN",
                        test_definition_id=(
                            "TEST-MANUAL-LOGIN"
                        ),
                        environment=environment,
                        execution_cycle="Release 1",
                        status="PASSED",
                    ),
                    create_execution(
                        f"EXEC-{environment}-AUTO-LOGIN",
                        test_definition_id="TEST-AUTO-LOGIN",
                        environment=environment,
                        execution_cycle="Release 1",
                        status="PASSED",
                    ),
                    create_execution(
                        f"EXEC-{environment}-MANUAL-LOGOUT",
                        test_definition_id=(
                            "TEST-MANUAL-LOGOUT"
                        ),
                        environment=environment,
                        execution_cycle="Release 1",
                        status="PASSED",
                    ),
                    create_execution(
                        f"EXEC-{environment}-AUTO-LOGOUT",
                        test_definition_id="TEST-AUTO-LOGOUT",
                        environment=environment,
                        execution_cycle="Release 1",
                        status="PASSED",
                    ),
                ]
            )

        self.execution_repository.add_many(
            executions
        )

    def test_full_reporting_flow_is_green(self) -> None:
        snapshot = self.build_snapshot()

        self.assertEqual(
            snapshot.health,
            DashboardHealth.GREEN,
        )
        self.assertEqual(
            snapshot.execution_summary.total,
            8,
        )
        self.assertEqual(
            snapshot.execution_summary.passed,
            8,
        )
        self.assertEqual(
            snapshot.execution_summary
            .completion_percentage,
            100.0,
        )

    def test_all_requested_environments_are_ready(
        self,
    ) -> None:
        snapshot = self.build_snapshot()

        self.assertEqual(
            snapshot.environment_count,
            2,
        )
        self.assertEqual(
            snapshot.ready_environment_count,
            2,
        )
        self.assertEqual(
            snapshot.partially_ready_environment_count,
            0,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            0,
        )

        self.assertTrue(
            all(
                summary.readiness
                is EnvironmentReadinessStatus.READY
                for summary
                in snapshot.environment_summaries
            )
        )

    def test_manual_and_automation_coverage_is_complete(
        self,
    ) -> None:
        snapshot = self.build_snapshot()
        coverage = snapshot.coverage_summary

        self.assertEqual(
            coverage.total_scenarios,
            2,
        )
        self.assertEqual(
            coverage.covered_scenarios,
            2,
        )
        self.assertEqual(
            coverage.manual_covered_scenarios,
            2,
        )
        self.assertEqual(
            coverage.automation_covered_scenarios,
            2,
        )
        self.assertEqual(
            coverage.dual_covered_scenarios,
            2,
        )
        self.assertTrue(
            coverage.has_full_scenario_coverage
        )
        self.assertTrue(
            coverage.has_full_manual_coverage
        )
        self.assertTrue(
            coverage.has_full_automation_coverage
        )

    def test_snapshot_payload_is_json_serializable(
        self,
    ) -> None:
        snapshot = self.build_snapshot()

        payload = snapshot.to_dict()
        serialized = json.dumps(payload)

        self.assertIsInstance(serialized, str)
        self.assertIn(
            '"health": "GREEN"',
            serialized,
        )
        self.assertIn(
            '"execution_cycle": "Release 1"',
            serialized,
        )

    def test_snapshot_generation_is_deterministic(
        self,
    ) -> None:
        first = self.build_snapshot().to_dict()
        second = self.build_snapshot().to_dict()

        self.assertEqual(first, second)

    def test_environment_order_is_deterministic(
        self,
    ) -> None:
        snapshot = self.dashboard_snapshot_service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Release 1",
            environments=(
                "UAT",
                "SIT",
                "UAT",
            ),
        )

        self.assertEqual(
            tuple(
                summary.environment
                for summary
                in snapshot.environment_summaries
            ),
            (
                Environment.SIT,
                Environment.UAT,
            ),
        )


class RerunRegressionTests(
    ReportingIntegrationFixture
):
    """Verify representative selection throughout the full flow."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add(
            create_scenario(
                "SCN-PAYMENT",
                feature_id="FEATURE-PAYMENT",
            )
        )

        self.test_definition_repository.add_many(
            [
                create_manual_test(
                    "TEST-MANUAL-PAYMENT",
                    scenario_id="SCN-PAYMENT",
                ),
                create_automation_test(
                    "TEST-AUTO-PAYMENT",
                    scenario_id="SCN-PAYMENT",
                ),
            ]
        )

        self.execution_repository.add_many(
            [
                create_execution(
                    "EXEC-MANUAL-PAYMENT",
                    test_definition_id=(
                        "TEST-MANUAL-PAYMENT"
                    ),
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                ),
                create_execution(
                    "EXEC-AUTO-PAYMENT-INITIAL",
                    test_definition_id="TEST-AUTO-PAYMENT",
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="FAILED",
                    completed_at=(
                        BASE_TIME + timedelta(minutes=5)
                    ),
                    defect_ids=("BUG-101",),
                ),
                create_execution(
                    "EXEC-AUTO-PAYMENT-RERUN",
                    test_definition_id="TEST-AUTO-PAYMENT",
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                    started_at=(
                        BASE_TIME + timedelta(hours=1)
                    ),
                    completed_at=(
                        BASE_TIME
                        + timedelta(
                            hours=1,
                            minutes=5,
                        )
                    ),
                    rerun_of_execution_id=(
                        "EXEC-AUTO-PAYMENT-INITIAL"
                    ),
                ),
            ]
        )

    def test_successful_rerun_removes_failure_from_snapshot(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        self.assertEqual(
            snapshot.execution_summary.total,
            2,
        )
        self.assertEqual(
            snapshot.execution_summary.passed,
            2,
        )
        self.assertEqual(
            snapshot.execution_summary.failed,
            0,
        )
        self.assertEqual(
            snapshot.health,
            DashboardHealth.GREEN,
        )

    def test_rerun_does_not_inflate_execution_total(
        self,
    ) -> None:
        selected = (
            self.execution_selection_service
            .select_current_executions(
                environment="SIT",
                execution_cycle="Release 1",
            )
        )

        self.assertEqual(len(selected), 2)

        selected_ids = {
            execution.execution_id
            for execution in selected
        }

        self.assertIn(
            "EXEC-AUTO-PAYMENT-RERUN",
            selected_ids,
        )
        self.assertNotIn(
            "EXEC-AUTO-PAYMENT-INITIAL",
            selected_ids,
        )


class AmberReportingIntegrationTests(
    ReportingIntegrationFixture
):
    """Verify non-critical readiness and coverage exceptions."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add_many(
            [
                create_scenario(
                    "SCN-SEARCH",
                    feature_id="FEATURE-SEARCH",
                ),
                create_scenario(
                    "SCN-EXPORT",
                    feature_id="FEATURE-EXPORT",
                ),
            ]
        )

        self.test_definition_repository.add_many(
            [
                create_manual_test(
                    "TEST-MANUAL-SEARCH",
                    scenario_id="SCN-SEARCH",
                ),
                create_automation_test(
                    "TEST-AUTO-SEARCH",
                    scenario_id="SCN-SEARCH",
                ),
            ]
        )

        self.execution_repository.add_many(
            [
                create_execution(
                    "EXEC-MANUAL-SEARCH",
                    test_definition_id=(
                        "TEST-MANUAL-SEARCH"
                    ),
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                ),
                create_execution(
                    "EXEC-AUTO-SEARCH",
                    test_definition_id="TEST-AUTO-SEARCH",
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="IN_PROGRESS",
                ),
            ]
        )

    def test_incomplete_execution_and_coverage_are_amber(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.partially_ready_environment_count,
            1,
        )
        self.assertEqual(
            snapshot.coverage_summary
            .uncovered_scenarios,
            1,
        )

    def test_amber_snapshot_contains_actionable_risks(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        risks = " ".join(
            snapshot.executive_summary.risks
        ).lower()

        actions = " ".join(
            snapshot.executive_summary
            .recommended_actions
        ).lower()

        self.assertIn("remain", risks)
        self.assertIn("no eligible test definition", risks)
        self.assertIn("outstanding execution", actions)
        self.assertIn("uncovered", actions)

    def test_validation_warning_keeps_snapshot_amber(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",),
            validation_report=(
                IntegrationValidationReport(
                    error_count=0,
                    warning_count=2,
                )
            ),
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.validation.warning_count,
            2,
        )


class RedReportingIntegrationTests(
    ReportingIntegrationFixture
):
    """Verify release-impacting reporting exceptions."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add(
            create_scenario(
                "SCN-ORDER",
                feature_id="FEATURE-ORDER",
            )
        )

        self.test_definition_repository.add_many(
            [
                create_manual_test(
                    "TEST-MANUAL-ORDER",
                    scenario_id="SCN-ORDER",
                ),
                create_automation_test(
                    "TEST-AUTO-ORDER",
                    scenario_id="SCN-ORDER",
                ),
            ]
        )

        self.execution_repository.add_many(
            [
                create_execution(
                    "EXEC-MANUAL-ORDER",
                    test_definition_id=(
                        "TEST-MANUAL-ORDER"
                    ),
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                ),
                create_execution(
                    "EXEC-AUTO-ORDER",
                    test_definition_id="TEST-AUTO-ORDER",
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="BLOCKED",
                ),
            ]
        )

    def test_blocked_execution_makes_dashboard_red(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.execution_summary.blocked,
            1,
        )
        self.assertEqual(
            snapshot.partially_ready_environment_count,
            1,
        )

    def test_missing_requested_environment_makes_dashboard_red(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=(
                "SIT",
                "UAT",
            )
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            1,
        )

        uat_summary = next(
            summary
            for summary in snapshot.environment_summaries
            if summary.environment is Environment.UAT
        )

        self.assertEqual(
            uat_summary.readiness,
            EnvironmentReadinessStatus.NOT_READY,
        )

    def test_validation_error_takes_red_precedence(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",),
            validation_report=(
                IntegrationValidationReport(
                    error_count=1,
                    warning_count=3,
                )
            ),
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertFalse(
            snapshot.validation.is_valid
        )
        self.assertEqual(
            snapshot.validation.error_count,
            1,
        )


class ExecutionCycleIsolationTests(
    ReportingIntegrationFixture
):
    """Verify reporting cycles never overwrite each other."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add(
            create_scenario(
                "SCN-PROFILE",
                feature_id="FEATURE-PROFILE",
            )
        )

        self.test_definition_repository.add(
            create_manual_test(
                "TEST-MANUAL-PROFILE",
                scenario_id="SCN-PROFILE",
            )
        )

        self.execution_repository.add_many(
            [
                create_execution(
                    "EXEC-PROFILE-CYCLE-1",
                    test_definition_id=(
                        "TEST-MANUAL-PROFILE"
                    ),
                    environment="SIT",
                    execution_cycle="Cycle 1",
                    status="FAILED",
                ),
                create_execution(
                    "EXEC-PROFILE-CYCLE-2",
                    test_definition_id=(
                        "TEST-MANUAL-PROFILE"
                    ),
                    environment="SIT",
                    execution_cycle="Cycle 2",
                    status="PASSED",
                    started_at=(
                        BASE_TIME + timedelta(days=1)
                    ),
                    completed_at=(
                        BASE_TIME
                        + timedelta(
                            days=1,
                            minutes=5,
                        )
                    ),
                ),
            ]
        )

    def test_cycle_one_retains_failure(self) -> None:
        snapshot = self.dashboard_snapshot_service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Cycle 1",
            environments=("SIT",),
        )

        self.assertEqual(
            snapshot.execution_summary.total,
            1,
        )
        self.assertEqual(
            snapshot.execution_summary.failed,
            1,
        )
        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )

    def test_cycle_two_uses_passing_result(self) -> None:
        snapshot = self.dashboard_snapshot_service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Cycle 2",
            environments=("SIT",),
        )

        self.assertEqual(
            snapshot.execution_summary.total,
            1,
        )
        self.assertEqual(
            snapshot.execution_summary.passed,
            1,
        )

    def test_combined_summary_preserves_both_cycles(
        self,
    ) -> None:
        summary = (
            self.execution_summary_service.summarize()
        )

        self.assertEqual(summary.total, 2)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.passed, 1)
        self.assertTrue(
            summary.includes_multiple_cycles
        )


class BuildVersionRegressionTests(
    ReportingIntegrationFixture
):
    """Verify mixed builds remain visible in reporting."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add(
            create_scenario(
                "SCN-ACCOUNT",
                feature_id="FEATURE-ACCOUNT",
            )
        )

        self.test_definition_repository.add_many(
            [
                create_manual_test(
                    "TEST-MANUAL-ACCOUNT",
                    scenario_id="SCN-ACCOUNT",
                ),
                create_automation_test(
                    "TEST-AUTO-ACCOUNT",
                    scenario_id="SCN-ACCOUNT",
                ),
            ]
        )

        self.execution_repository.add_many(
            [
                create_execution(
                    "EXEC-MANUAL-ACCOUNT",
                    test_definition_id=(
                        "TEST-MANUAL-ACCOUNT"
                    ),
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                    build_version="1.0.0",
                ),
                create_execution(
                    "EXEC-AUTO-ACCOUNT",
                    test_definition_id="TEST-AUTO-ACCOUNT",
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                    build_version="1.0.1",
                ),
            ]
        )

    def test_mixed_builds_make_snapshot_amber(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        environment = snapshot.environment_summaries[0]

        self.assertTrue(
            environment.has_mixed_build_versions
        )
        self.assertEqual(
            environment.build_versions,
            (
                "1.0.0",
                "1.0.1",
            ),
        )
        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )

    def test_mixed_build_action_is_reported(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        actions = " ".join(
            snapshot.executive_summary
            .recommended_actions
        ).lower()

        self.assertIn(
            "one intended build",
            actions,
        )


class ActiveOnlyCoverageRegressionTests(
    ReportingIntegrationFixture
):
    """Verify inactive data does not distort active coverage."""

    def setUp(self) -> None:
        super().setUp()

        self.scenario_repository.add_many(
            [
                create_scenario(
                    "SCN-ACTIVE",
                    feature_id="FEATURE-A",
                    active=True,
                ),
                create_scenario(
                    "SCN-INACTIVE",
                    feature_id="FEATURE-A",
                    active=False,
                ),
            ]
        )

        self.test_definition_repository.add_many(
            [
                create_manual_test(
                    "TEST-MANUAL-ACTIVE",
                    scenario_id="SCN-ACTIVE",
                ),
                create_automation_test(
                    "TEST-AUTO-ACTIVE",
                    scenario_id="SCN-ACTIVE",
                ),
                create_manual_test(
                    "TEST-MANUAL-INACTIVE",
                    scenario_id="SCN-INACTIVE",
                ),
            ]
        )

        self.execution_repository.add_many(
            [
                create_execution(
                    "EXEC-MANUAL-ACTIVE",
                    test_definition_id=(
                        "TEST-MANUAL-ACTIVE"
                    ),
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                ),
                create_execution(
                    "EXEC-AUTO-ACTIVE",
                    test_definition_id="TEST-AUTO-ACTIVE",
                    environment="SIT",
                    execution_cycle="Release 1",
                    status="PASSED",
                ),
            ]
        )

    def test_default_snapshot_uses_active_coverage(
        self,
    ) -> None:
        snapshot = self.build_snapshot(
            environments=("SIT",)
        )

        self.assertEqual(
            snapshot.coverage_summary.total_scenarios,
            1,
        )
        self.assertEqual(
            snapshot.coverage_summary.covered_scenarios,
            1,
        )
        self.assertTrue(
            snapshot.coverage_summary
            .has_full_automation_coverage
        )

    def test_governance_snapshot_can_include_inactive_data(
        self,
    ) -> None:
        snapshot = self.dashboard_snapshot_service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Release 1",
            environments=("SIT",),
            active_only=False,
        )

        self.assertEqual(
            snapshot.coverage_summary.total_scenarios,
            2,
        )
        self.assertEqual(
            snapshot.coverage_summary
            .manual_covered_scenarios,
            2,
        )
        self.assertEqual(
            snapshot.coverage_summary
            .automation_covered_scenarios,
            1,
        )
        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )


class ReportingBoundaryRegressionTests(
    ReportingIntegrationFixture
):
    """Verify snapshot output remains a reporting boundary."""

    def test_snapshot_does_not_write_files(self) -> None:
        before = {
            path.relative_to(REPOSITORY_ROOT)
            for path in REPOSITORY_ROOT.rglob("*")
            if path.is_file()
        }

        self.dashboard_snapshot_service.build(
            generated_at=GENERATED_AT,
            environments=("SIT",),
        )

        after = {
            path.relative_to(REPOSITORY_ROOT)
            for path in REPOSITORY_ROOT.rglob("*")
            if path.is_file()
        }

        self.assertEqual(before, after)

    def test_snapshot_payload_contains_expected_sections(
        self,
    ) -> None:
        payload = (
            self.dashboard_snapshot_service.build(
                generated_at=GENERATED_AT,
                environments=("SIT",),
            )
            .to_dict()
        )

        self.assertEqual(
            set(payload),
            {
                "schema_version",
                "generated_at",
                "health",
                "execution_cycle",
                "environment_count",
                "ready_environment_count",
                "partially_ready_environment_count",
                "not_ready_environment_count",
                "executive_summary",
                "execution_summary",
                "coverage_summary",
                "environment_summaries",
                "validation",
            },
        )


if __name__ == "__main__":
    unittest.main()
