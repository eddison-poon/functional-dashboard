"""Unit tests for the Execution selection service."""

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
    ExecutionGroupKey,
    ExecutionSelectionService,
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


def not_executed_execution(
    execution_id: str,
    *,
    test_definition_id: str = "TEST-001",
    environment: Environment | str = "SIT",
    execution_cycle: str | None = "SIT Cycle 1",
) -> Execution:
    """Create a valid planned Execution."""
    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status="NOT_EXECUTED",
        execution_cycle=execution_cycle,
        build_version="1.0.0",
    )


def in_progress_execution(
    execution_id: str,
    *,
    test_definition_id: str = "TEST-001",
    environment: Environment | str = "SIT",
    execution_cycle: str | None = "SIT Cycle 1",
    started_at: datetime = BASE_TIME,
) -> Execution:
    """Create a valid in-progress Execution."""
    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status="IN_PROGRESS",
        execution_cycle=execution_cycle,
        started_at=started_at,
        executed_by="QA User",
        build_version="1.0.0",
    )


def terminal_execution(
    execution_id: str,
    *,
    test_definition_id: str = "TEST-001",
    environment: Environment | str = "SIT",
    execution_cycle: str | None = "SIT Cycle 1",
    status: str = "PASSED",
    started_at: datetime | None = BASE_TIME,
    completed_at: datetime = (
        BASE_TIME + timedelta(minutes=5)
    ),
    rerun_of_execution_id: str | None = None,
) -> Execution:
    """Create a valid terminal Execution."""
    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status=status,
        execution_cycle=execution_cycle,
        started_at=started_at,
        completed_at=completed_at,
        executed_by="QA User",
        build_version="1.0.0",
        rerun_of_execution_id=rerun_of_execution_id,
    )


class ExecutionGroupKeyTests(unittest.TestCase):
    """Tests covering execution grouping keys."""

    def test_group_key_to_dict(self) -> None:
        key = ExecutionGroupKey(
            test_definition_id="TEST-001",
            environment=Environment.SIT,
            execution_cycle="SIT Cycle 1",
        )

        self.assertEqual(
            key.to_dict(),
            {
                "test_definition_id": "TEST-001",
                "environment": "SIT",
                "execution_cycle": "SIT Cycle 1",
            },
        )

    def test_group_key_supports_null_cycle(self) -> None:
        key = ExecutionGroupKey(
            test_definition_id="TEST-001",
            environment=Environment.SIT,
            execution_cycle=None,
        )

        self.assertIsNone(
            key.to_dict()["execution_cycle"]
        )


class ExecutionSelectionServiceValidationTests(
    unittest.TestCase
):
    """Tests covering service input validation."""

    def test_repository_is_required(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            ExecutionSelectionService(  # type: ignore[arg-type]
                execution_repository={}
            )

    def test_invalid_environment_is_rejected(self) -> None:
        service = ExecutionSelectionService(
            ExecutionRepository()
        )

        with self.assertRaises(RepositoryValidationError):
            service.select_current_by_environment(
                "LOCAL"
            )

    def test_blank_cycle_is_rejected(self) -> None:
        service = ExecutionSelectionService(
            ExecutionRepository()
        )

        with self.assertRaises(RepositoryValidationError):
            service.select_current_by_cycle(" ")

    def test_non_string_cycle_is_rejected(self) -> None:
        service = ExecutionSelectionService(
            ExecutionRepository()
        )

        with self.assertRaises(RepositoryValidationError):
            service.select_current_by_cycle(  # type: ignore[arg-type]
                123
            )

    def test_blank_test_definition_id_is_rejected(
        self,
    ) -> None:
        service = ExecutionSelectionService(
            ExecutionRepository()
        )

        with self.assertRaises(RepositoryValidationError):
            service.group_execution_history_by_test_definition(
                " "
            )


class ExecutionSelectionFixtureTests(unittest.TestCase):
    """Shared execution-selection fixture."""

    def setUp(self) -> None:
        self.repository = ExecutionRepository()
        self.service = ExecutionSelectionService(
            self.repository
        )

        self.original_failure = terminal_execution(
            "EXEC-001",
            test_definition_id="TEST-001",
            environment="SIT",
            execution_cycle="SIT Cycle 1",
            status="FAILED",
            started_at=BASE_TIME,
            completed_at=(
                BASE_TIME + timedelta(minutes=5)
            ),
        )

        self.successful_rerun = terminal_execution(
            "EXEC-002",
            test_definition_id="TEST-001",
            environment="SIT",
            execution_cycle="SIT Cycle 1",
            status="PASSED",
            started_at=(
                BASE_TIME + timedelta(hours=1)
            ),
            completed_at=(
                BASE_TIME
                + timedelta(hours=1, minutes=4)
            ),
            rerun_of_execution_id="EXEC-001",
        )

        self.second_test = terminal_execution(
            "EXEC-003",
            test_definition_id="TEST-002",
            environment="SIT",
            execution_cycle="SIT Cycle 1",
            status="PASSED",
            started_at=(
                BASE_TIME + timedelta(hours=2)
            ),
            completed_at=(
                BASE_TIME
                + timedelta(hours=2, minutes=3)
            ),
        )

        self.uat_result = terminal_execution(
            "EXEC-004",
            test_definition_id="TEST-001",
            environment="UAT",
            execution_cycle="UAT Cycle 1",
            status="BLOCKED",
            started_at=(
                BASE_TIME + timedelta(days=1)
            ),
            completed_at=(
                BASE_TIME
                + timedelta(days=1, minutes=2)
            ),
        )

        self.second_cycle_result = terminal_execution(
            "EXEC-005",
            test_definition_id="TEST-001",
            environment="SIT",
            execution_cycle="SIT Cycle 2",
            status="FAILED",
            started_at=(
                BASE_TIME + timedelta(days=2)
            ),
            completed_at=(
                BASE_TIME
                + timedelta(days=2, minutes=6)
            ),
        )

        self.repository.add_many(
            [
                self.original_failure,
                self.successful_rerun,
                self.second_test,
                self.uat_result,
                self.second_cycle_result,
            ]
        )


class ExecutionRepresentativeSelectionTests(
    ExecutionSelectionFixtureTests
):
    """Tests covering representative Execution selection."""

    def test_latest_completed_execution_is_selected(
        self,
    ) -> None:
        result = self.service.select_current_by_cycle(
            "SIT Cycle 1",
            environment="SIT",
        )

        self.assertEqual(
            result,
            (
                self.successful_rerun,
                self.second_test,
            ),
        )

    def test_rerun_does_not_inflate_current_total(
        self,
    ) -> None:
        result = self.service.select_current_by_cycle(
            "SIT Cycle 1",
            environment="SIT",
        )

        self.assertEqual(len(result), 2)

    def test_latest_started_is_used_without_completed_records(
        self,
    ) -> None:
        repository = ExecutionRepository()
        service = ExecutionSelectionService(repository)

        earlier = in_progress_execution(
            "EXEC-010",
            started_at=BASE_TIME,
        )
        later = in_progress_execution(
            "EXEC-011",
            started_at=(
                BASE_TIME + timedelta(hours=1)
            ),
        )

        repository.add_many([earlier, later])

        result = service.select_current_executions()

        self.assertEqual(result, (later,))

    def test_execution_id_is_fallback_without_timestamps(
        self,
    ) -> None:
        repository = ExecutionRepository()
        service = ExecutionSelectionService(repository)

        lower_id = not_executed_execution(
            "EXEC-010"
        )
        higher_id = not_executed_execution(
            "EXEC-011"
        )

        repository.add_many(
            [
                higher_id,
                lower_id,
            ]
        )

        result = service.select_current_executions()

        self.assertEqual(result, (higher_id,))

    def test_completed_execution_precedes_in_progress_rerun(
        self,
    ) -> None:
        repository = ExecutionRepository()
        service = ExecutionSelectionService(repository)

        completed = terminal_execution(
            "EXEC-020",
            status="FAILED",
            started_at=BASE_TIME,
            completed_at=(
                BASE_TIME + timedelta(minutes=5)
            ),
        )
        active_rerun = in_progress_execution(
            "EXEC-021",
            started_at=(
                BASE_TIME + timedelta(hours=1)
            ),
        )

        repository.add_many(
            [
                completed,
                active_rerun,
            ]
        )

        result = service.select_current_executions()

        self.assertEqual(result, (completed,))

    def test_later_completed_result_is_selected(
        self,
    ) -> None:
        repository = ExecutionRepository()
        service = ExecutionSelectionService(repository)

        earlier = terminal_execution(
            "EXEC-030",
            status="FAILED",
            completed_at=(
                BASE_TIME + timedelta(minutes=10)
            ),
        )
        later = terminal_execution(
            "EXEC-031",
            status="PASSED",
            completed_at=(
                BASE_TIME + timedelta(hours=1)
            ),
        )

        repository.add_many([later, earlier])

        result = service.select_current_executions()

        self.assertEqual(result, (later,))


class ExecutionGroupingTests(
    ExecutionSelectionFixtureTests
):
    """Tests covering reporting group boundaries."""

    def test_environment_is_part_of_group_key(self) -> None:
        result = self.service.select_current_executions()

        selected_ids = tuple(
            execution.execution_id
            for execution in result
        )

        self.assertIn("EXEC-002", selected_ids)
        self.assertIn("EXEC-004", selected_ids)

    def test_execution_cycle_is_part_of_group_key(
        self,
    ) -> None:
        result = self.service.select_current_by_environment(
            "SIT"
        )

        selected_ids = tuple(
            execution.execution_id
            for execution in result
        )

        self.assertIn("EXEC-002", selected_ids)
        self.assertIn("EXEC-005", selected_ids)

    def test_test_definition_is_part_of_group_key(
        self,
    ) -> None:
        result = self.service.select_current_by_cycle(
            "SIT Cycle 1",
            environment="SIT",
        )

        selected_test_ids = tuple(
            execution.test_definition_id
            for execution in result
        )

        self.assertEqual(
            selected_test_ids,
            (
                "TEST-001",
                "TEST-002",
            ),
        )

    def test_null_cycle_forms_separate_group(self) -> None:
        null_cycle = terminal_execution(
            "EXEC-010",
            test_definition_id="TEST-001",
            environment="SIT",
            execution_cycle=None,
        )
        self.repository.add(null_cycle)

        result = self.service.select_current_by_environment(
            "SIT"
        )

        self.assertIn(null_cycle, result)
        self.assertIn(self.successful_rerun, result)


class ExecutionSelectionFilterTests(
    ExecutionSelectionFixtureTests
):
    """Tests covering environment and cycle filters."""

    def test_filter_by_environment(self) -> None:
        result = self.service.select_current_by_environment(
            "UAT"
        )

        self.assertEqual(
            result,
            (self.uat_result,),
        )

    def test_environment_filter_accepts_enum(self) -> None:
        result = self.service.select_current_by_environment(
            Environment.UAT
        )

        self.assertEqual(
            result,
            (self.uat_result,),
        )

    def test_environment_filter_accepts_trimmed_string(
        self,
    ) -> None:
        result = self.service.select_current_by_environment(
            " uat "
        )

        self.assertEqual(
            result,
            (self.uat_result,),
        )

    def test_filter_by_cycle(self) -> None:
        result = self.service.select_current_by_cycle(
            "SIT Cycle 2"
        )

        self.assertEqual(
            result,
            (self.second_cycle_result,),
        )

    def test_cycle_filter_is_case_insensitive(self) -> None:
        result = self.service.select_current_by_cycle(
            " sit cycle 2 "
        )

        self.assertEqual(
            result,
            (self.second_cycle_result,),
        )

    def test_filter_by_environment_and_cycle(self) -> None:
        result = self.service.select_current_by_cycle(
            "SIT Cycle 1",
            environment="SIT",
        )

        self.assertEqual(
            result,
            (
                self.successful_rerun,
                self.second_test,
            ),
        )

    def test_missing_filter_match_returns_empty_tuple(
        self,
    ) -> None:
        result = self.service.select_current_by_cycle(
            "Pre-Production Cycle 1"
        )

        self.assertEqual(result, ())

    def test_no_filters_include_all_groups(self) -> None:
        result = self.service.select_current_executions()

        self.assertEqual(
            tuple(
                execution.execution_id
                for execution in result
            ),
            (
                "EXEC-002",
                "EXEC-003",
                "EXEC-005",
                "EXEC-004",
            ),
        )


class ExecutionHistoryGroupingTests(
    ExecutionSelectionFixtureTests
):
    """Tests covering full execution-history grouping."""

    def test_history_preserves_all_attempts(self) -> None:
        grouped = self.service.group_execution_history(
            environment="SIT",
            execution_cycle="SIT Cycle 1",
        )

        key = ExecutionGroupKey(
            test_definition_id="TEST-001",
            environment=Environment.SIT,
            execution_cycle="SIT Cycle 1",
        )

        self.assertEqual(
            grouped[key],
            (
                self.original_failure,
                self.successful_rerun,
            ),
        )

    def test_history_is_ordered_oldest_to_newest(
        self,
    ) -> None:
        repository = ExecutionRepository()
        service = ExecutionSelectionService(repository)

        newest = terminal_execution(
            "EXEC-003",
            completed_at=(
                BASE_TIME + timedelta(hours=2)
            ),
        )
        oldest = terminal_execution(
            "EXEC-001",
            completed_at=BASE_TIME,
        )
        middle = terminal_execution(
            "EXEC-002",
            completed_at=(
                BASE_TIME + timedelta(hours=1)
            ),
        )

        repository.add_many(
            [
                newest,
                oldest,
                middle,
            ]
        )

        grouped = service.group_execution_history()
        history = next(iter(grouped.values()))

        self.assertEqual(
            history,
            (
                oldest,
                middle,
                newest,
            ),
        )

    def test_history_filter_by_environment(self) -> None:
        grouped = self.service.group_execution_history(
            environment="UAT"
        )

        self.assertEqual(len(grouped), 1)

        key = next(iter(grouped))

        self.assertEqual(
            key.environment,
            Environment.UAT,
        )

    def test_history_filter_by_cycle(self) -> None:
        grouped = self.service.group_execution_history(
            execution_cycle="SIT Cycle 2"
        )

        self.assertEqual(len(grouped), 1)

        history = next(iter(grouped.values()))

        self.assertEqual(
            history,
            (self.second_cycle_result,),
        )

    def test_history_by_test_definition(self) -> None:
        grouped = (
            self.service
            .group_execution_history_by_test_definition(
                "TEST-001"
            )
        )

        self.assertEqual(len(grouped), 3)

        self.assertTrue(
            all(
                key.test_definition_id == "TEST-001"
                for key in grouped
            )
        )

    def test_test_definition_filter_is_case_sensitive(
        self,
    ) -> None:
        grouped = (
            self.service
            .group_execution_history_by_test_definition(
                "test-001"
            )
        )

        self.assertEqual(grouped, {})

    def test_empty_repository_returns_empty_results(
        self,
    ) -> None:
        service = ExecutionSelectionService(
            ExecutionRepository()
        )

        self.assertEqual(
            service.select_current_executions(),
            (),
        )
        self.assertEqual(
            service.group_execution_history(),
            {},
        )


if __name__ == "__main__":
    unittest.main()
