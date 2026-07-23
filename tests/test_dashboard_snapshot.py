"""Unit tests for the combined dashboard reporting snapshot."""

import sys
import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.execution import Execution  # noqa: E402
from canonical.scenario import Scenario  # noqa: E402
from canonical.test_definition import (  # noqa: E402
    TestDefinition,
    TestStep,
)
from repositories.base import (  # noqa: E402
    RepositoryValidationError,
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
    DashboardSnapshotService,
    ValidationSnapshot,
)
from services.environment_summary import (  # noqa: E402
    EnvironmentReadinessService,
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


def scenario(
    scenario_id: str,
    *,
    active: bool = True,
) -> Scenario:
    """Create a valid canonical Scenario."""
    return Scenario(
        scenario_id=scenario_id,
        feature_id="FEATURE-A",
        requirement_ids=[f"REQ-{scenario_id}"],
        name=f"Scenario {scenario_id}",
        scenario_type="POSITIVE",
        priority="HIGH",
        description="Functional business behaviour.",
        expected_outcome="Expected outcome occurs.",
        active=active,
    )


def manual_test(
    test_definition_id: str,
    *,
    scenario_id: str,
) -> TestDefinition:
    """Create a valid Manual Test Definition."""
    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="MANUAL",
        name=f"Manual {test_definition_id}",
        status="ACTIVE",
        version="1.0",
        steps=[
            TestStep(
                step_number=1,
                action="Perform the test.",
                expected_result="The test succeeds.",
            )
        ],
    )


def automation_test(
    test_definition_id: str,
    *,
    scenario_id: str,
    repository: str | None = "functional-tests",
    pipeline_name: str | None = "functional-regression",
) -> TestDefinition:
    """Create a valid Automation Test Definition."""
    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="AUTOMATION",
        name=f"Automation {test_definition_id}",
        status="ACTIVE",
        version="1.0",
        framework="PLAYWRIGHT",
        repository=repository,
        script_path=(
            f"tests/{test_definition_id.lower()}.py"
        ),
        pipeline_name=pipeline_name,
    )


def execution(
    execution_id: str,
    *,
    test_definition_id: str,
    environment: str = "SIT",
    execution_cycle: str = "Cycle 1",
    status: str = "PASSED",
    build_version: str = "1.0.0",
) -> Execution:
    """Create a valid canonical Execution."""
    started_at = BASE_TIME
    completed_at = BASE_TIME + timedelta(minutes=5)

    if status == "NOT_EXECUTED":
        started_at = None
        completed_at = None

    elif status == "IN_PROGRESS":
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
    )


@dataclass(frozen=True)
class FakeValidationReport:
    """Structural test double for repository validation."""

    error_count: int
    warning_count: int

    @property
    def is_valid(self) -> bool:
        """Return whether no errors exist."""
        return self.error_count == 0

    def to_dict(self) -> dict[str, object]:
        """Return representative serialized validation data."""
        return {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "is_valid": self.is_valid,
            "findings": [],
        }


class ValidationSnapshotTests(unittest.TestCase):
    """Tests covering validation snapshot conversion."""

    def test_empty_validation_snapshot(self) -> None:
        result = ValidationSnapshot.empty()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.error_count, 0)
        self.assertEqual(result.warning_count, 0)
        self.assertIsNone(result.report)

    def test_from_validation_report(self) -> None:
        result = ValidationSnapshot.from_report(
            FakeValidationReport(
                error_count=1,
                warning_count=2,
            )
        )

        self.assertFalse(result.is_valid)
        self.assertEqual(result.error_count, 1)
        self.assertEqual(result.warning_count, 2)
        self.assertIsInstance(result.report, dict)

    def test_is_valid_must_match_error_count(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ValidationSnapshot(
                error_count=1,
                warning_count=0,
                is_valid=True,
            )

    def test_negative_count_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ValidationSnapshot(
                error_count=-1,
                warning_count=0,
                is_valid=False,
            )


class DashboardSnapshotFixtureTests(unittest.TestCase):
    """Shared dashboard-snapshot fixture."""

    def setUp(self) -> None:
        self.scenarios = ScenarioRepository()
        self.test_definitions = (
            TestDefinitionRepository()
        )
        self.executions = ExecutionRepository()

        self.selection = ExecutionSelectionService(
            self.executions
        )
        self.execution_summaries = (
            ExecutionSummaryService(
                self.selection
            )
        )
        self.coverage_summaries = (
            CoverageSummaryService(
                self.scenarios,
                self.test_definitions,
            )
        )
        self.environment_readiness = (
            EnvironmentReadinessService(
                self.selection,
                self.execution_summaries,
            )
        )

        self.service = DashboardSnapshotService(
            execution_summary_service=(
                self.execution_summaries
            ),
            coverage_summary_service=(
                self.coverage_summaries
            ),
            environment_readiness_service=(
                self.environment_readiness
            ),
        )

    def add_fully_covered_scenario(
        self,
        *,
        scenario_id: str = "SCN-001",
        manual_id: str = "TEST-MANUAL-001",
        automation_id: str = "TEST-AUTO-001",
    ) -> None:
        """Add one Scenario with Manual and Automation coverage."""
        self.scenarios.add(
            scenario(scenario_id)
        )
        self.test_definitions.add_many(
            [
                manual_test(
                    manual_id,
                    scenario_id=scenario_id,
                ),
                automation_test(
                    automation_id,
                    scenario_id=scenario_id,
                ),
            ]
        )


class DashboardSnapshotValidationTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering service input validation."""

    def test_generated_at_must_be_datetime(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.build(  # type: ignore[arg-type]
                generated_at="2026-07-24"
            )

    def test_generated_at_must_be_timezone_aware(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.build(
                generated_at=datetime(
                    2026,
                    7,
                    24,
                    9,
                    0,
                )
            )

    def test_blank_cycle_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.build(
                generated_at=GENERATED_AT,
                execution_cycle=" ",
            )


class DashboardGreenHealthTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering Green dashboard health."""

    def test_complete_passing_scope_is_green(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Cycle 1",
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.GREEN,
        )
        self.assertEqual(
            snapshot.execution_summary.total,
            2,
        )
        self.assertEqual(
            snapshot.ready_environment_count,
            1,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            0,
        )
        self.assertEqual(
            snapshot.executive_summary.health,
            DashboardHealth.GREEN,
        )


class DashboardAmberHealthTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering Amber dashboard health."""

    def test_incomplete_execution_is_amber(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                    status="PASSED",
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                    status="IN_PROGRESS",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.partially_ready_environment_count,
            1,
        )

    def test_coverage_gap_is_amber(self) -> None:
        self.scenarios.add_many(
            [
                scenario("SCN-001"),
                scenario("SCN-002"),
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
                ),
            ]
        )

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.coverage_summary
            .uncovered_scenarios,
            1,
        )

    def test_validation_warning_is_amber(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
            validation_report=FakeValidationReport(
                error_count=0,
                warning_count=1,
            ),
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )


class DashboardRedHealthTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering Red dashboard health."""

    def test_failed_execution_is_red(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                    status="FAILED",
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertTrue(
            any(
                "failed" in risk.lower()
                for risk
                in snapshot.executive_summary.risks
            )
        )

    def test_requested_environment_without_data_is_red(
        self,
    ) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=[
                "SIT",
                "UAT",
            ],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            1,
        )

    def test_validation_error_is_red(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
            validation_report=FakeValidationReport(
                error_count=1,
                warning_count=0,
            ),
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.validation.error_count,
            1,
        )


class DashboardSnapshotSerializationTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering snapshot JSON serialization."""

    def test_to_dict(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Cycle 1",
            environments=["SIT"],
        )

        result = snapshot.to_dict()

        self.assertEqual(
            result["schema_version"],
            "1.0",
        )
        self.assertEqual(
            result["generated_at"],
            GENERATED_AT.isoformat(),
        )
        self.assertEqual(result["health"], "GREEN")
        self.assertEqual(
            result["execution_cycle"],
            "Cycle 1",
        )
        self.assertEqual(
            result["environment_count"],
            1,
        )
        self.assertIn(
            "executive_summary",
            result,
        )
        self.assertIn(
            "execution_summary",
            result,
        )
        self.assertIn(
            "coverage_summary",
            result,
        )
        self.assertIn(
            "environment_summaries",
            result,
        )
        self.assertIn(
            "validation",
            result,
        )


class DashboardEmptyDataTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering empty reporting data."""

    def test_empty_requested_environment_is_red(
        self,
    ) -> None:
        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.execution_summary.total,
            0,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            1,
        )

    def test_no_requested_environment_is_amber(
        self,
    ) -> None:
        snapshot = self.service.build(
            generated_at=GENERATED_AT,
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.environment_count,
            0,
        )
        self.assertEqual(
            snapshot.executive_summary
            .readiness_assessment,
            "No environment readiness data is available.",
        )


if __name__ == "__main__":
    unittest.main() """Unit tests for the combined dashboard reporting snapshot."""

import sys
import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.execution import Execution  # noqa: E402
from canonical.scenario import Scenario  # noqa: E402
from canonical.test_definition import (  # noqa: E402
    TestDefinition,
    TestStep,
)
from repositories.base import (  # noqa: E402
    RepositoryValidationError,
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
    DashboardSnapshotService,
    ValidationSnapshot,
)
from services.environment_summary import (  # noqa: E402
    EnvironmentReadinessService,
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


def scenario(
    scenario_id: str,
    *,
    active: bool = True,
) -> Scenario:
    """Create a valid canonical Scenario."""
    return Scenario(
        scenario_id=scenario_id,
        feature_id="FEATURE-A",
        requirement_ids=[f"REQ-{scenario_id}"],
        name=f"Scenario {scenario_id}",
        scenario_type="POSITIVE",
        priority="HIGH",
        description="Functional business behaviour.",
        expected_outcome="Expected outcome occurs.",
        active=active,
    )


def manual_test(
    test_definition_id: str,
    *,
    scenario_id: str,
) -> TestDefinition:
    """Create a valid Manual Test Definition."""
    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="MANUAL",
        name=f"Manual {test_definition_id}",
        status="ACTIVE",
        version="1.0",
        steps=[
            TestStep(
                step_number=1,
                action="Perform the test.",
                expected_result="The test succeeds.",
            )
        ],
    )


def automation_test(
    test_definition_id: str,
    *,
    scenario_id: str,
    repository: str | None = "functional-tests",
    pipeline_name: str | None = "functional-regression",
) -> TestDefinition:
    """Create a valid Automation Test Definition."""
    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="AUTOMATION",
        name=f"Automation {test_definition_id}",
        status="ACTIVE",
        version="1.0",
        framework="PLAYWRIGHT",
        repository=repository,
        script_path=(
            f"tests/{test_definition_id.lower()}.py"
        ),
        pipeline_name=pipeline_name,
    )


def execution(
    execution_id: str,
    *,
    test_definition_id: str,
    environment: str = "SIT",
    execution_cycle: str = "Cycle 1",
    status: str = "PASSED",
    build_version: str = "1.0.0",
) -> Execution:
    """Create a valid canonical Execution."""
    started_at = BASE_TIME
    completed_at = BASE_TIME + timedelta(minutes=5)

    if status == "NOT_EXECUTED":
        started_at = None
        completed_at = None

    elif status == "IN_PROGRESS":
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
    )


@dataclass(frozen=True)
class FakeValidationReport:
    """Structural test double for repository validation."""

    error_count: int
    warning_count: int

    @property
    def is_valid(self) -> bool:
        """Return whether no errors exist."""
        return self.error_count == 0

    def to_dict(self) -> dict[str, object]:
        """Return representative serialized validation data."""
        return {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "is_valid": self.is_valid,
            "findings": [],
        }


class ValidationSnapshotTests(unittest.TestCase):
    """Tests covering validation snapshot conversion."""

    def test_empty_validation_snapshot(self) -> None:
        result = ValidationSnapshot.empty()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.error_count, 0)
        self.assertEqual(result.warning_count, 0)
        self.assertIsNone(result.report)

    def test_from_validation_report(self) -> None:
        result = ValidationSnapshot.from_report(
            FakeValidationReport(
                error_count=1,
                warning_count=2,
            )
        )

        self.assertFalse(result.is_valid)
        self.assertEqual(result.error_count, 1)
        self.assertEqual(result.warning_count, 2)
        self.assertIsInstance(result.report, dict)

    def test_is_valid_must_match_error_count(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ValidationSnapshot(
                error_count=1,
                warning_count=0,
                is_valid=True,
            )

    def test_negative_count_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ValidationSnapshot(
                error_count=-1,
                warning_count=0,
                is_valid=False,
            )


class DashboardSnapshotFixtureTests(unittest.TestCase):
    """Shared dashboard-snapshot fixture."""

    def setUp(self) -> None:
        self.scenarios = ScenarioRepository()
        self.test_definitions = (
            TestDefinitionRepository()
        )
        self.executions = ExecutionRepository()

        self.selection = ExecutionSelectionService(
            self.executions
        )
        self.execution_summaries = (
            ExecutionSummaryService(
                self.selection
            )
        )
        self.coverage_summaries = (
            CoverageSummaryService(
                self.scenarios,
                self.test_definitions,
            )
        )
        self.environment_readiness = (
            EnvironmentReadinessService(
                self.selection,
                self.execution_summaries,
            )
        )

        self.service = DashboardSnapshotService(
            execution_summary_service=(
                self.execution_summaries
            ),
            coverage_summary_service=(
                self.coverage_summaries
            ),
            environment_readiness_service=(
                self.environment_readiness
            ),
        )

    def add_fully_covered_scenario(
        self,
        *,
        scenario_id: str = "SCN-001",
        manual_id: str = "TEST-MANUAL-001",
        automation_id: str = "TEST-AUTO-001",
    ) -> None:
        """Add one Scenario with Manual and Automation coverage."""
        self.scenarios.add(
            scenario(scenario_id)
        )
        self.test_definitions.add_many(
            [
                manual_test(
                    manual_id,
                    scenario_id=scenario_id,
                ),
                automation_test(
                    automation_id,
                    scenario_id=scenario_id,
                ),
            ]
        )


class DashboardSnapshotValidationTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering service input validation."""

    def test_generated_at_must_be_datetime(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.build(  # type: ignore[arg-type]
                generated_at="2026-07-24"
            )

    def test_generated_at_must_be_timezone_aware(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.build(
                generated_at=datetime(
                    2026,
                    7,
                    24,
                    9,
                    0,
                )
            )

    def test_blank_cycle_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            self.service.build(
                generated_at=GENERATED_AT,
                execution_cycle=" ",
            )


class DashboardGreenHealthTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering Green dashboard health."""

    def test_complete_passing_scope_is_green(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Cycle 1",
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.GREEN,
        )
        self.assertEqual(
            snapshot.execution_summary.total,
            2,
        )
        self.assertEqual(
            snapshot.ready_environment_count,
            1,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            0,
        )
        self.assertEqual(
            snapshot.executive_summary.health,
            DashboardHealth.GREEN,
        )


class DashboardAmberHealthTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering Amber dashboard health."""

    def test_incomplete_execution_is_amber(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                    status="PASSED",
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                    status="IN_PROGRESS",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.partially_ready_environment_count,
            1,
        )

    def test_coverage_gap_is_amber(self) -> None:
        self.scenarios.add_many(
            [
                scenario("SCN-001"),
                scenario("SCN-002"),
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
                ),
            ]
        )

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.coverage_summary
            .uncovered_scenarios,
            1,
        )

    def test_validation_warning_is_amber(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
            validation_report=FakeValidationReport(
                error_count=0,
                warning_count=1,
            ),
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )


class DashboardRedHealthTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering Red dashboard health."""

    def test_failed_execution_is_red(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                    status="FAILED",
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertTrue(
            any(
                "failed" in risk.lower()
                for risk
                in snapshot.executive_summary.risks
            )
        )

    def test_requested_environment_without_data_is_red(
        self,
    ) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=[
                "SIT",
                "UAT",
            ],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            1,
        )

    def test_validation_error_is_red(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
            validation_report=FakeValidationReport(
                error_count=1,
                warning_count=0,
            ),
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.validation.error_count,
            1,
        )


class DashboardSnapshotSerializationTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering snapshot JSON serialization."""

    def test_to_dict(self) -> None:
        self.add_fully_covered_scenario()

        self.executions.add_many(
            [
                execution(
                    "EXEC-MANUAL-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-AUTO-001",
                    test_definition_id="TEST-AUTO-001",
                ),
            ]
        )

        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            execution_cycle="Cycle 1",
            environments=["SIT"],
        )

        result = snapshot.to_dict()

        self.assertEqual(
            result["schema_version"],
            "1.0",
        )
        self.assertEqual(
            result["generated_at"],
            GENERATED_AT.isoformat(),
        )
        self.assertEqual(result["health"], "GREEN")
        self.assertEqual(
            result["execution_cycle"],
            "Cycle 1",
        )
        self.assertEqual(
            result["environment_count"],
            1,
        )
        self.assertIn(
            "executive_summary",
            result,
        )
        self.assertIn(
            "execution_summary",
            result,
        )
        self.assertIn(
            "coverage_summary",
            result,
        )
        self.assertIn(
            "environment_summaries",
            result,
        )
        self.assertIn(
            "validation",
            result,
        )


class DashboardEmptyDataTests(
    DashboardSnapshotFixtureTests
):
    """Tests covering empty reporting data."""

    def test_empty_requested_environment_is_red(
        self,
    ) -> None:
        snapshot = self.service.build(
            generated_at=GENERATED_AT,
            environments=["SIT"],
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.RED,
        )
        self.assertEqual(
            snapshot.execution_summary.total,
            0,
        )
        self.assertEqual(
            snapshot.not_ready_environment_count,
            1,
        )

    def test_no_requested_environment_is_amber(
        self,
    ) -> None:
        snapshot = self.service.build(
            generated_at=GENERATED_AT,
        )

        self.assertEqual(
            snapshot.health,
            DashboardHealth.AMBER,
        )
        self.assertEqual(
            snapshot.environment_count,
            0,
        )
        self.assertEqual(
            snapshot.executive_summary
            .readiness_assessment,
            "No environment readiness data is available.",
        )


if __name__ == "__main__":
    unittest.main()
