
"""Unit tests for the test execution summary service."""

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.enums import Environment  # noqa: E402
from canonical.execution import Execution  # noqa: E402
from repositories.base import (  # noqa: E402
    RepositoryValidationError,
)
from repositories.execution_repository import (  # noqa: E402
    ExecutionRepository,
)
from services.execution_selection import (  # noqa: E402
    ExecutionSelectionService,
)
from services.execution_summary import (  # noqa: E402
    ExecutionSummary,
    ExecutionSummaryService,
)


UTC = timezone.utc

BASE_TIME = datetime(
    2026,
    7,
    20,
    9,
    0,
    tzinfo=UTC,
)


def execution(
    execution_id: str,
    *,
    test_definition_id: str,
    environment: Environment | str = "SIT",
    status: str = "PASSED",
    execution_cycle: str | None = "SIT Cycle 1",
    started_at: datetime | None = BASE_TIME,
    completed_at: datetime | None = (
        BASE_TIME + timedelta(minutes=5)
    ),
    rerun_of_execution_id: str | None = None,
) -> Execution:
    """Create a valid Execution for one status."""
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
        build_version="1.0.0",
        rerun_of_execution_id=rerun_of_execution_id,
    )


class ExecutionSummaryModelTests(unittest.TestCase):
    """Tests covering ExecutionSummary properties."""

    def valid_summary(self) -> ExecutionSummary:
        """Return a valid example summary."""
        return ExecutionSummary(
            environment=Environment.SIT,
            execution_cycle="SIT Cycle 1",
            total=7,
            executed=6,
            terminal=5,
            passed=2,
            failed=1,
            blocked=1,
            skipped=1,
            aborted=0,
            in_progress=1,
            not_executed=1,
            execution_percentage=85.71,
            completion_percentage=71.43,
            pass_rate=40.0,
            failure_rate=20.0,
            blocked_rate=20.0,
        )

    def test_outstanding(self) -> None:
        summary = self.valid_summary()

        self.assertEqual(summary.outstanding, 2)

    def test_unsuccessful_terminal(self) -> None:
        summary = self.valid_summary()

        self.assertEqual(
            summary.unsuccessful_terminal,
            3,
        )

    def test_non_empty_summary(self) -> None:
        summary = self.valid_summary()

        self.assertFalse(summary.is_empty)

    def test_incomplete_summary(self) -> None:
        summary = self.valid_summary()

        self.assertFalse(summary.is_complete)

    def test_complete_summary(self) -> None:
        summary = ExecutionSummary(
            environment=Environment.SIT,
            execution_cycle="SIT Cycle 1",
            total=2,
            executed=2,
            terminal=2,
            passed=2,
            failed=0,
            blocked=0,
            skipped=0,
            aborted=0,
            in_progress=0,
            not_executed=0,
            execution_percentage=100.0,
            completion_percentage=100.0,
            pass_rate=100.0,
            failure_rate=0.0,
            blocked_rate=0.0,
        )

        self.assertTrue(summary.is_complete)

    def test_empty_summary_is_not_complete(self) -> None:
        summary = ExecutionSummary(
            environment=None,
            execution_cycle=None,
            total=0,
            executed=0,
            terminal=0,
            passed=0,
            failed=0,
            blocked=0,
            skipped=0,
            aborted=0,
            in_progress=0,
            not_executed=0,
            execution_percentage=0.0,
            completion_percentage=0.0,
            pass_rate=0.0,
            failure_rate=0.0,
            blocked_rate=0.0,
        )

        self.assertTrue(summary.is_empty)
        self.assertFalse(summary.is_complete)

    def test_to_dict(self) -> None:
        summary = self.valid_summary()

        result = summary.to_dict()

        self.assertEqual(result["environment"], "SIT")
        self.assertEqual(
            result["execution_cycle"],
            "SIT Cycle 1",
        )
        self.assertEqual(result["total"], 7)
        self.assertEqual(result["outstanding"], 2)
        self.assertEqual(
            result["unsuccessful_terminal"],
            3,
        )
        self.assertFalse(result["is_complete"])

    def test_status_counts_must_equal_total(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ExecutionSummary(
                environment=None,
                execution_cycle=None,
                total=2,
                executed=1,
                terminal=1,
                passed=1,
                failed=0,
                blocked=0,
                skipped=0,
                aborted=0,
                in_progress=0,
                not_executed=0,
                execution_percentage=50.0,
                completion_percentage=50.0,
                pass_rate=100.0,
                failure_rate=0.0,
                blocked_rate=0.0,
            )

    def test_terminal_count_must_be_consistent(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ExecutionSummary(
                environment=None,
                execution_cycle=None,
                total=1,
                executed=1,
                terminal=0,
                passed=1,
                failed=0,
                blocked=0,
                skipped=0,
                aborted=0,
                in_progress=0,
                not_executed=0,
                execution_percentage=100.0,
                completion_percentage=0.0,
                pass_rate=0.0,
                failure_rate=0.0,
                blocked_rate=0.0,
            )

    def test_executed_count_must_be_consistent(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ExecutionSummary(
                environment=None,
                execution_cycle=None,
                total=1,
                executed=0,
                terminal=1,
                passed=1,
                failed=0,
                blocked=0,
                skipped=0,
                aborted=0,
                in_progress=0,
                not_executed=0,
                execution_percentage=0.0,
                completion_percentage=100.0,
                pass_rate=100.0,
                failure_rate=0.0,
                blocked_rate=0.0,
            )

    def test_negative_count_is_rejected(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ExecutionSummary(
                environment=None,
                execution_cycle=None,
                total=-1,
                executed=0,
                terminal=0,
                passed=0,
                failed=0,
                blocked=0,
                skipped=0,
                aborted=0,
                in_progress=0,
                not_executed=0,
                execution_percentage=0.0,
                completion_percentage=0.0,
                pass_rate=0.0,
                failure_rate=0.0,
                blocked_rate=0.0,
            )

    def test_percentage_above_100_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ExecutionSummary(
                environment=None,
                execution_cycle=None,
                total=1,
                executed=1,
                terminal=1,
                passed=1,
                failed=0,
                blocked=0,
                skipped=0,
                aborted=0,
                in_progress=0,
                not_executed=0,
                execution_percentage=101.0,
                completion_percentage=100.0,
                pass_rate=100.0,
                failure_rate=0.0,
                blocked_rate=0.0,
            )


class ExecutionSummaryServiceValidationTests(
    unittest.TestCase
):
    """Tests covering service dependency validation."""

    def test_selection_service_is_required(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            ExecutionSummaryService(  # type: ignore[arg-type]
                execution_selection_service={}
            )


class ExecutionSummaryFixtureTests(unittest.TestCase):
    """Shared test execution summary fixture."""

    def setUp(self) -> None:
        self.repository = ExecutionRepository()
        self.selection = ExecutionSelectionService(
            self.repository
        )
        self.service = ExecutionSummaryService(
            self.selection
        )

        records = [
            execution(
                "EXEC-001",
                test_definition_id="TEST-001",
                status="PASSED",
            ),
            execution(
                "EXEC-002",
                test_definition_id="TEST-002",
                status="PASSED",
            ),
            execution(
                "EXEC-003",
                test_definition_id="TEST-003",
                status="FAILED",
            ),
            execution(
                "EXEC-004",
                test_definition_id="TEST-004",
                status="BLOCKED",
            ),
            execution(
                "EXEC-005",
                test_definition_id="TEST-005",
                status="SKIPPED",
            ),
            execution(
                "EXEC-006",
                test_definition_id="TEST-006",
                status="ABORTED",
            ),
            execution(
                "EXEC-007",
                test_definition_id="TEST-007",
                status="IN_PROGRESS",
            ),
            execution(
                "EXEC-008",
                test_definition_id="TEST-008",
                status="NOT_EXECUTED",
            ),
        ]

        self.repository.add_many(records)


class ExecutionSummaryCalculationTests(
    ExecutionSummaryFixtureTests
):
    """Tests covering summary calculations."""

    def test_status_counts(self) -> None:
        summary = self.service.summarize(
            environment="SIT",
            execution_cycle="SIT Cycle 1",
        )

        self.assertEqual(summary.total, 8)
        self.assertEqual(summary.executed, 7)
        self.assertEqual(summary.terminal, 6)
        self.assertEqual(summary.passed, 2)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.blocked, 1)
        self.assertEqual(summary.skipped, 1)
        self.assertEqual(summary.aborted, 1)
        self.assertEqual(summary.in_progress, 1)
        self.assertEqual(summary.not_executed, 1)

    def test_execution_percentage(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.execution_percentage,
            87.5,
        )

    def test_completion_percentage(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.completion_percentage,
            75.0,
        )

    def test_pass_rate_uses_terminal_results(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.pass_rate, 33.33)

    def test_failure_rate_uses_terminal_results(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.failure_rate, 16.67)

    def test_blocked_rate_uses_terminal_results(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.blocked_rate, 16.67)

    def test_outstanding_count(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.outstanding, 2)

    def test_unsuccessful_terminal_count(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(
            summary.unsuccessful_terminal,
            4,
        )


class ExecutionSummarySelectionTests(
    unittest.TestCase
):
    """Tests proving reruns do not inflate summary metrics."""

    def test_latest_rerun_replaces_original_result(
        self,
    ) -> None:
        repository = ExecutionRepository()
        selection = ExecutionSelectionService(repository)
        service = ExecutionSummaryService(selection)

        original = execution(
            "EXEC-001",
            test_definition_id="TEST-001",
            status="FAILED",
            completed_at=(
                BASE_TIME + timedelta(minutes=5)
            ),
        )

        rerun = execution(
            "EXEC-002",
            test_definition_id="TEST-001",
            status="PASSED",
            started_at=(
                BASE_TIME + timedelta(hours=1)
            ),
            completed_at=(
                BASE_TIME
                + timedelta(hours=1, minutes=5)
            ),
            rerun_of_execution_id="EXEC-001",
        )

        repository.add_many(
            [
                original,
                rerun,
            ]
        )

        summary = service.summarize()

        self.assertEqual(summary.total, 1)
        self.assertEqual(summary.passed, 1)
        self.assertEqual(summary.failed, 0)
        self.assertEqual(summary.pass_rate, 100.0)

    def test_completed_result_precedes_active_rerun(
        self,
    ) -> None:
        repository = ExecutionRepository()
        selection = ExecutionSelectionService(repository)
        service = ExecutionSummaryService(selection)

        completed = execution(
            "EXEC-001",
            test_definition_id="TEST-001",
            status="FAILED",
        )

        active_rerun = execution(
            "EXEC-002",
            test_definition_id="TEST-001",
            status="IN_PROGRESS",
            started_at=(
                BASE_TIME + timedelta(hours=1)
            ),
            rerun_of_execution_id="EXEC-001",
        )

        repository.add_many(
            [
                completed,
                active_rerun,
            ]
        )

        summary = service.summarize()

        self.assertEqual(summary.total, 1)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(summary.in_progress, 0)


class ExecutionSummaryFilterTests(
    ExecutionSummaryFixtureTests
):
    """Tests covering report scope filters."""

    def setUp(self) -> None:
        super().setUp()

        self.uat_result = execution(
            "EXEC-UAT-001",
            test_definition_id="TEST-009",
            environment="UAT",
            execution_cycle="UAT Cycle 1",
            status="PASSED",
        )

        self.second_cycle = execution(
            "EXEC-SIT-009",
            test_definition_id="TEST-009",
            environment="SIT",
            execution_cycle="SIT Cycle 2",
            status="FAILED",
        )

        self.repository.add_many(
            [
                self.uat_result,
                self.second_cycle,
            ]
        )

    def test_filter_by_environment(self) -> None:
        summary = self.service.summarize(
            environment="UAT"
        )

        self.assertEqual(
            summary.environment,
            Environment.UAT,
        )
        self.assertEqual(summary.total, 1)
        self.assertEqual(summary.passed, 1)

    def test_filter_by_cycle(self) -> None:
        summary = self.service.summarize(
            execution_cycle="SIT Cycle 2"
        )

        self.assertEqual(
            summary.execution_cycle,
            "SIT Cycle 2",
        )
        self.assertEqual(summary.total, 1)
        self.assertEqual(summary.failed, 1)

    def test_filter_by_environment_and_cycle(
        self,
    ) -> None:
        summary = self.service.summarize(
            environment="SIT",
            execution_cycle="SIT Cycle 1",
        )

        self.assertEqual(summary.total, 8)
        self.assertFalse(
            summary.includes_multiple_environments
        )
        self.assertFalse(
            summary.includes_multiple_cycles
        )

    def test_combined_summary_identifies_multiple_environments(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertTrue(
            summary.includes_multiple_environments
        )

    def test_combined_summary_identifies_multiple_cycles(
        self,
    ) -> None:
        summary = self.service.summarize()

        self.assertTrue(
            summary.includes_multiple_cycles
        )

    def test_no_matching_records_returns_empty_summary(
        self,
    ) -> None:
        summary = self.service.summarize(
            environment="UAT",
            execution_cycle="Missing Cycle",
        )

        self.assertEqual(summary.total, 0)
        self.assertTrue(summary.is_empty)
        self.assertEqual(
            summary.environment,
            Environment.UAT,
        )
        self.assertEqual(
            summary.execution_cycle,
            "Missing Cycle",
        )


class ExecutionSummaryGroupingTests(
    ExecutionSummaryFixtureTests
):
    """Tests covering grouped summary output."""

    def setUp(self) -> None:
        super().setUp()

        self.repository.add_many(
            [
                execution(
                    "EXEC-UAT-001",
                    test_definition_id="TEST-009",
                    environment="UAT",
                    execution_cycle="UAT Cycle 1",
                    status="PASSED",
                ),
                execution(
                    "EXEC-SIT-C2",
                    test_definition_id="TEST-009",
                    environment="SIT",
                    execution_cycle="SIT Cycle 2",
                    status="FAILED",
                ),
                execution(
                    "EXEC-SIT-NULL",
                    test_definition_id="TEST-010",
                    environment="SIT",
                    execution_cycle=None,
                    status="NOT_EXECUTED",
                ),
            ]
        )

    def test_summarize_by_environment(self) -> None:
        summaries = (
            self.service.summarize_by_environment()
        )

        self.assertEqual(
            tuple(
                summary.environment
                for summary in summaries
            ),
            (
                Environment.SIT,
                Environment.UAT,
            ),
        )

        sit_summary = summaries[0]

        self.assertEqual(sit_summary.total, 10)
        self.assertTrue(
            sit_summary.includes_multiple_cycles
        )

    def test_summarize_by_environment_with_cycle_filter(
        self,
    ) -> None:
        summaries = (
            self.service.summarize_by_environment(
                execution_cycle="SIT Cycle 1"
            )
        )

        self.assertEqual(len(summaries), 1)
        self.assertEqual(
            summaries[0].environment,
            Environment.SIT,
        )
        self.assertEqual(
            summaries[0].execution_cycle,
            "SIT Cycle 1",
        )

    def test_summarize_by_cycle(self) -> None:
        summaries = self.service.summarize_by_cycle(
            environment="SIT"
        )

        cycles = tuple(
            summary.execution_cycle
            for summary in summaries
        )

        self.assertEqual(
            cycles,
            (
                None,
                "SIT Cycle 1",
                "SIT Cycle 2",
            ),
        )

    def test_environment_cycle_matrix(self) -> None:
        summaries = (
            self.service
            .summarize_environment_cycle_matrix()
        )

        scopes = tuple(
            (
                summary.environment,
                summary.execution_cycle,
            )
            for summary in summaries
        )

        self.assertEqual(
            scopes,
            (
                (Environment.SIT, None),
                (
                    Environment.SIT,
                    "SIT Cycle 1",
                ),
                (
                    Environment.SIT,
                    "SIT Cycle 2",
                ),
                (
                    Environment.UAT,
                    "UAT Cycle 1",
                ),
            ),
        )

    def test_matrix_summaries_do_not_mix_scopes(
        self,
    ) -> None:
        summaries = (
            self.service
            .summarize_environment_cycle_matrix()
        )

        for summary in summaries:
            self.assertFalse(
                summary.includes_multiple_environments
            )
            self.assertFalse(
                summary.includes_multiple_cycles
            )


class ExecutionSummaryEmptyRepositoryTests(
    unittest.TestCase
):
    """Tests covering empty reporting data."""

    def setUp(self) -> None:
        repository = ExecutionRepository()

        self.service = ExecutionSummaryService(
            ExecutionSelectionService(repository)
        )

    def test_empty_repository_summary(self) -> None:
        summary = self.service.summarize()

        self.assertEqual(summary.total, 0)
        self.assertEqual(summary.executed, 0)
        self.assertEqual(summary.terminal, 0)
        self.assertEqual(
            summary.execution_percentage,
            0.0,
        )
        self.assertEqual(
            summary.completion_percentage,
            0.0,
        )
        self.assertEqual(summary.pass_rate, 0.0)

    def test_empty_environment_grouping(self) -> None:
        self.assertEqual(
            self.service.summarize_by_environment(),
            (),
        )

    def test_empty_cycle_grouping(self) -> None:
        self.assertEqual(
            self.service.summarize_by_cycle(),
            (),
        )

    def test_empty_matrix(self) -> None:
        self.assertEqual(
            self.service
            .summarize_environment_cycle_matrix(),
            (),
        )


if __name__ == "__main__":
    unittest.main()
