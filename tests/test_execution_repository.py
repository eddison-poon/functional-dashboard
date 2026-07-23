"""Unit tests for the canonical Execution repository."""

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.enums import (  # noqa: E402
    Environment,
    ExecutionStatus,
    SourceSystem,
)
from canonical.execution import Execution  # noqa: E402
from repositories.base import (  # noqa: E402
    DuplicateItemError,
    ItemNotFoundError,
    RepositoryValidationError,
)
from repositories.execution_repository import (  # noqa: E402
    ExecutionRepository,
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
    execution_id: str = "EXEC-001",
    *,
    test_definition_id: str = "TEST-MANUAL-001",
    environment: Environment | str = "SIT",
    execution_cycle: str | None = "SIT Cycle 1",
    build_version: str | None = "2.1.0",
    source_system: SourceSystem | str = (
        SourceSystem.MANUAL_ENTRY
    ),
    external_reference: str | None = None,
    remarks: str | None = "Execution is planned.",
    rerun_of_execution_id: str | None = None,
) -> Execution:
    """Create a valid NOT_EXECUTED Execution."""

    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status=ExecutionStatus.NOT_EXECUTED,
        execution_cycle=execution_cycle,
        build_version=build_version,
        source_system=source_system,
        external_reference=external_reference,
        remarks=remarks,
        rerun_of_execution_id=rerun_of_execution_id,
    )


def in_progress_execution(
    execution_id: str = "EXEC-002",
    *,
    test_definition_id: str = "TEST-MANUAL-002",
    environment: Environment | str = "SIT",
    execution_cycle: str | None = "SIT Cycle 1",
    started_at: datetime = BASE_TIME,
    executed_by: str | None = "Manual QA",
    build_version: str | None = "2.1.0",
    source_system: SourceSystem | str = (
        SourceSystem.MANUAL_ENTRY
    ),
    external_reference: str | None = "JIRA-EXEC-002",
    defect_ids: tuple[str, ...] | list[str] = (),
    evidence_ids: tuple[str, ...] | list[str] = (),
    remarks: str | None = "Execution is in progress.",
    rerun_of_execution_id: str | None = None,
) -> Execution:
    """Create a valid IN_PROGRESS Execution."""

    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status=ExecutionStatus.IN_PROGRESS,
        execution_cycle=execution_cycle,
        started_at=started_at,
        executed_by=executed_by,
        build_version=build_version,
        source_system=source_system,
        external_reference=external_reference,
        defect_ids=defect_ids,
        evidence_ids=evidence_ids,
        remarks=remarks,
        rerun_of_execution_id=rerun_of_execution_id,
    )


def terminal_execution(
    execution_id: str = "EXEC-003",
    *,
    test_definition_id: str = "TEST-AUTO-001",
    environment: Environment | str = "SIT",
    status: ExecutionStatus | str = "PASSED",
    execution_cycle: str | None = "SIT Cycle 1",
    started_at: datetime | None = BASE_TIME,
    completed_at: datetime = BASE_TIME + timedelta(minutes=5),
    executed_by: str | None = "Automation Service",
    build_version: str | None = "2.1.0",
    source_system: SourceSystem | str = (
        SourceSystem.MANUAL_ENTRY
    ),
    external_reference: str | None = "PIPELINE-1001",
    defect_ids: tuple[str, ...] | list[str] = (),
    evidence_ids: tuple[str, ...] | list[str] = (
        "EVIDENCE-001",
    ),
    remarks: str | None = "Execution completed.",
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
        executed_by=executed_by,
        build_version=build_version,
        source_system=source_system,
        external_reference=external_reference,
        defect_ids=defect_ids,
        evidence_ids=evidence_ids,
        remarks=remarks,
        rerun_of_execution_id=rerun_of_execution_id,
    )


class ExecutionRepositoryCrudTests(unittest.TestCase):
    """Tests covering base repository behaviour."""

    def setUp(self) -> None:
        self.repository = ExecutionRepository()

    def test_repository_starts_empty(self) -> None:
        self.assertEqual(self.repository.count(), 0)
        self.assertEqual(self.repository.list_all(), ())

    def test_add_and_get_execution(self) -> None:
        execution = not_executed_execution()

        self.repository.add(execution)

        self.assertEqual(
            self.repository.get("EXEC-001"),
            execution,
        )

    def test_duplicate_execution_is_rejected(self) -> None:
        self.repository.add(not_executed_execution())

        with self.assertRaises(DuplicateItemError):
            self.repository.add(
                not_executed_execution(
                    remarks="Duplicate execution."
                )
            )

    def test_get_missing_execution_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.get("EXEC-MISSING")

    def test_replace_execution(self) -> None:
        original = not_executed_execution()
        replacement = in_progress_execution(
            "EXEC-001",
            test_definition_id="TEST-MANUAL-001",
            remarks="Execution has now started.",
        )

        self.repository.add(original)

        previous = self.repository.replace(replacement)

        self.assertEqual(previous, original)
        self.assertEqual(
            self.repository.get("EXEC-001"),
            replacement,
        )

    def test_remove_execution(self) -> None:
        execution = not_executed_execution()
        self.repository.add(execution)

        removed = self.repository.remove("EXEC-001")

        self.assertEqual(removed, execution)
        self.assertEqual(self.repository.count(), 0)

    def test_list_all_is_sorted_by_execution_id(self) -> None:
        self.repository.add_many(
            [
                not_executed_execution("EXEC-003"),
                not_executed_execution("EXEC-001"),
                not_executed_execution("EXEC-002"),
            ]
        )

        result = self.repository.list_all()

        self.assertEqual(
            tuple(item.execution_id for item in result),
            (
                "EXEC-001",
                "EXEC-002",
                "EXEC-003",
            ),
        )

    def test_incorrect_object_type_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add(  # type: ignore[arg-type]
                {
                    "execution_id": "EXEC-001",
                }
            )


class ExecutionRepositoryFixtureTests(unittest.TestCase):
    """Shared Execution repository fixture."""

    def setUp(self) -> None:
        self.repository = ExecutionRepository()

        self.not_executed = not_executed_execution(
            "EXEC-001",
            test_definition_id="TEST-MANUAL-001",
            environment="SIT",
            execution_cycle="SIT Cycle 1",
            build_version="2.1.0",
            external_reference="JIRA-PLAN-001",
            remarks="Planned login validation.",
        )

        self.in_progress = in_progress_execution(
            "EXEC-002",
            test_definition_id="TEST-MANUAL-002",
            environment="SIT",
            execution_cycle="SIT Cycle 1",
            started_at=BASE_TIME + timedelta(hours=1),
            executed_by="Manual QA",
            build_version="2.1.0",
            external_reference="JIRA-EXEC-002",
            remarks="Checkout validation is underway.",
        )

        self.passed = terminal_execution(
            "EXEC-003",
            test_definition_id="TEST-AUTO-001",
            environment="SIT",
            status="PASSED",
            execution_cycle="SIT Cycle 1",
            started_at=BASE_TIME + timedelta(hours=2),
            completed_at=BASE_TIME + timedelta(
                hours=2,
                minutes=10,
            ),
            executed_by="Automation Service",
            build_version="2.1.0",
            external_reference="PIPELINE-1001",
            evidence_ids=[
                "EVIDENCE-001",
                "REPORT-001",
            ],
            remarks="Automated login validation passed.",
        )

        self.failed = terminal_execution(
            "EXEC-004",
            test_definition_id="TEST-AUTO-002",
            environment="UAT",
            status="FAILED",
            execution_cycle="UAT Cycle 1",
            started_at=BASE_TIME + timedelta(days=1),
            completed_at=BASE_TIME + timedelta(
                days=1,
                minutes=15,
            ),
            executed_by="Automation Service",
            build_version="2.2.0-RC1",
            external_reference="PIPELINE-1002",
            defect_ids=[
                "BUG-101",
                "BUG-102",
            ],
            evidence_ids=["EVIDENCE-002"],
            remarks="Payment validation failed.",
        )

        self.blocked = terminal_execution(
            "EXEC-005",
            test_definition_id="TEST-MANUAL-003",
            environment="UAT",
            status="BLOCKED",
            execution_cycle="UAT Cycle 1",
            started_at=BASE_TIME + timedelta(days=1, hours=1),
            completed_at=BASE_TIME + timedelta(
                days=1,
                hours=1,
                minutes=5,
            ),
            executed_by="Business Tester",
            build_version="2.2.0-RC1",
            external_reference="JIRA-EXEC-005",
            defect_ids=["BUG-201"],
            evidence_ids=(),
            remarks="Blocked by unavailable payment service.",
        )

        self.rerun_passed = terminal_execution(
            "EXEC-006",
            test_definition_id="TEST-AUTO-002",
            environment="UAT",
            status="PASSED",
            execution_cycle="UAT Cycle 1",
            started_at=BASE_TIME + timedelta(days=2),
            completed_at=BASE_TIME + timedelta(
                days=2,
                minutes=12,
            ),
            executed_by="Automation Service",
            build_version="2.2.0-RC2",
            external_reference="PIPELINE-1003",
            evidence_ids=["EVIDENCE-003"],
            remarks="Payment validation passed after the fix.",
            rerun_of_execution_id="EXEC-004",
        )

        self.repository.add_many(
            [
                self.not_executed,
                self.in_progress,
                self.passed,
                self.failed,
                self.blocked,
                self.rerun_passed,
            ]
        )


class ExecutionRelationshipFilterTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering entity and rerun relationships."""

    def test_find_by_test_definition_id(self) -> None:
        result = (
            self.repository.find_by_test_definition_id(
                "TEST-AUTO-002"
            )
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.rerun_passed,
            ),
        )

    def test_test_definition_id_is_trimmed(self) -> None:
        result = (
            self.repository.find_by_test_definition_id(
                " TEST-MANUAL-001 "
            )
        )

        self.assertEqual(
            result,
            (self.not_executed,),
        )

    def test_test_definition_id_is_case_sensitive(
        self,
    ) -> None:
        result = (
            self.repository.find_by_test_definition_id(
                "test-auto-002"
            )
        )

        self.assertEqual(result, ())

    def test_find_reruns(self) -> None:
        result = self.repository.find_reruns()

        self.assertEqual(
            result,
            (self.rerun_passed,),
        )

    def test_find_reruns_of_execution(self) -> None:
        result = self.repository.find_reruns_of(
            "EXEC-004"
        )

        self.assertEqual(
            result,
            (self.rerun_passed,),
        )

    def test_blank_test_definition_id_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_test_definition_id(
                " "
            )

    def test_blank_rerun_execution_id_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_reruns_of(" ")


class ExecutionControlledValueFilterTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering canonical enum filters."""

    def test_find_by_environment(self) -> None:
        result = self.repository.find_by_environment(
            Environment.SIT
        )

        self.assertEqual(
            result,
            (
                self.not_executed,
                self.in_progress,
                self.passed,
            ),
        )

    def test_find_by_environment_accepts_string(
        self,
    ) -> None:
        result = self.repository.find_by_environment(
            " uat "
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.blocked,
                self.rerun_passed,
            ),
        )

    def test_invalid_environment_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_environment(
                "LOCAL"
            )

    def test_find_by_status(self) -> None:
        result = self.repository.find_by_status(
            ExecutionStatus.PASSED
        )

        self.assertEqual(
            result,
            (
                self.passed,
                self.rerun_passed,
            ),
        )

    def test_find_by_status_accepts_string(self) -> None:
        result = self.repository.find_by_status(
            " failed "
        )

        self.assertEqual(
            result,
            (self.failed,),
        )

    def test_invalid_status_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_status(
                "PARTIALLY_PASSED"
            )

    def test_find_by_source_system(self) -> None:
        result = self.repository.find_by_source_system(
            SourceSystem.MANUAL_ENTRY
        )

        self.assertEqual(
            result,
            self.repository.list_all(),
        )

    def test_find_by_source_system_accepts_string(
        self,
    ) -> None:
        result = self.repository.find_by_source_system(
            " manual_entry "
        )

        self.assertEqual(
            result,
            self.repository.list_all(),
        )

    def test_invalid_source_system_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_source_system(
                "UNKNOWN_SYSTEM"
            )


class ExecutionGeneralFilterTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering general Execution filters."""

    def test_find_by_execution_cycle(self) -> None:
        result = self.repository.find_by_execution_cycle(
            "SIT Cycle 1"
        )

        self.assertEqual(
            result,
            (
                self.not_executed,
                self.in_progress,
                self.passed,
            ),
        )

    def test_execution_cycle_is_case_insensitive(
        self,
    ) -> None:
        result = self.repository.find_by_execution_cycle(
            " uat cycle 1 "
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.blocked,
                self.rerun_passed,
            ),
        )

    def test_find_by_executed_by(self) -> None:
        result = self.repository.find_by_executed_by(
            "Automation Service"
        )

        self.assertEqual(
            result,
            (
                self.passed,
                self.failed,
                self.rerun_passed,
            ),
        )

    def test_executed_by_is_case_insensitive(self) -> None:
        result = self.repository.find_by_executed_by(
            " business tester "
        )

        self.assertEqual(
            result,
            (self.blocked,),
        )

    def test_find_by_build_version(self) -> None:
        result = self.repository.find_by_build_version(
            "2.1.0"
        )

        self.assertEqual(
            result,
            (
                self.not_executed,
                self.in_progress,
                self.passed,
            ),
        )

    def test_build_version_is_case_insensitive(
        self,
    ) -> None:
        result = self.repository.find_by_build_version(
            " 2.2.0-rc1 "
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.blocked,
            ),
        )

    def test_find_by_external_reference(self) -> None:
        result = (
            self.repository.find_by_external_reference(
                "PIPELINE-1002"
            )
        )

        self.assertEqual(
            result,
            (self.failed,),
        )

    def test_external_reference_is_case_sensitive(
        self,
    ) -> None:
        result = (
            self.repository.find_by_external_reference(
                "pipeline-1002"
            )
        )

        self.assertEqual(result, ())

    def test_blank_general_filters_are_rejected(
        self,
    ) -> None:
        invalid_calls = [
            lambda: self.repository.find_by_execution_cycle(
                " "
            ),
            lambda: self.repository.find_by_executed_by(
                " "
            ),
            lambda: self.repository.find_by_build_version(
                " "
            ),
            lambda: (
                self.repository.find_by_external_reference(
                    " "
                )
            ),
        ]

        for invalid_call in invalid_calls:
            with self.subTest(call=invalid_call):
                with self.assertRaises(
                    RepositoryValidationError
                ):
                    invalid_call()


class ExecutionDefectAndEvidenceFilterTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering defects and execution evidence."""

    def test_find_by_defect_id(self) -> None:
        result = self.repository.find_by_defect_id(
            "BUG-101"
        )

        self.assertEqual(
            result,
            (self.failed,),
        )

    def test_defect_id_is_case_sensitive(self) -> None:
        result = self.repository.find_by_defect_id(
            "bug-101"
        )

        self.assertEqual(result, ())

    def test_find_with_defects(self) -> None:
        result = self.repository.find_with_defects()

        self.assertEqual(
            result,
            (
                self.failed,
                self.blocked,
            ),
        )

    def test_find_by_evidence_id(self) -> None:
        result = self.repository.find_by_evidence_id(
            "EVIDENCE-001"
        )

        self.assertEqual(
            result,
            (self.passed,),
        )

    def test_find_with_evidence(self) -> None:
        result = self.repository.find_with_evidence()

        self.assertEqual(
            result,
            (
                self.passed,
                self.failed,
                self.rerun_passed,
            ),
        )

    def test_find_without_evidence(self) -> None:
        result = self.repository.find_without_evidence()

        self.assertEqual(
            result,
            (
                self.not_executed,
                self.in_progress,
                self.blocked,
            ),
        )

    def test_blank_defect_id_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_defect_id(" ")

    def test_blank_evidence_id_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_evidence_id(" ")


class ExecutionStateFilterTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering derived Execution state queries."""

    def test_find_not_executed(self) -> None:
        result = self.repository.find_not_executed()

        self.assertEqual(
            result,
            (self.not_executed,),
        )

    def test_find_executed(self) -> None:
        result = self.repository.find_executed()

        self.assertEqual(
            result,
            (
                self.in_progress,
                self.passed,
                self.failed,
                self.blocked,
                self.rerun_passed,
            ),
        )

    def test_find_terminal(self) -> None:
        result = self.repository.find_terminal()

        self.assertEqual(
            result,
            (
                self.passed,
                self.failed,
                self.blocked,
                self.rerun_passed,
            ),
        )

    def test_find_successful(self) -> None:
        result = self.repository.find_successful()

        self.assertEqual(
            result,
            (
                self.passed,
                self.rerun_passed,
            ),
        )


class ExecutionDatetimeFilterTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering timestamp-range filtering."""

    def test_find_started_between_inclusive(self) -> None:
        result = self.repository.find_started_between(
            BASE_TIME + timedelta(hours=1),
            BASE_TIME + timedelta(hours=2),
        )

        self.assertEqual(
            result,
            (
                self.in_progress,
                self.passed,
            ),
        )

    def test_not_executed_item_is_excluded_from_started_range(
        self,
    ) -> None:
        result = self.repository.find_started_between(
            BASE_TIME - timedelta(days=1),
            BASE_TIME + timedelta(days=3),
        )

        self.assertNotIn(
            self.not_executed,
            result,
        )

    def test_find_completed_between_inclusive(self) -> None:
        result = self.repository.find_completed_between(
            BASE_TIME + timedelta(days=1),
            BASE_TIME + timedelta(
                days=1,
                hours=2,
            ),
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.blocked,
            ),
        )

    def test_non_datetime_range_value_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_started_between(
                "2026-07-20",  # type: ignore[arg-type]
                BASE_TIME,
            )

    def test_naive_datetime_is_rejected(self) -> None:
        naive_time = datetime(2026, 7, 20, 9, 0)

        with self.assertRaises(RepositoryValidationError):
            self.repository.find_completed_between(
                naive_time,
                BASE_TIME,
            )

    def test_reversed_datetime_range_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_started_between(
                BASE_TIME + timedelta(days=1),
                BASE_TIME,
            )


class ExecutionSearchTests(
    ExecutionRepositoryFixtureTests
):
    """Tests covering multi-field text search."""

    def test_search_by_execution_id(self) -> None:
        result = self.repository.search_text(
            "EXEC-004"
        )

        self.assertEqual(
            result,
            (self.failed,),
        )

    def test_search_by_test_definition_id(self) -> None:
        result = self.repository.search_text(
            "TEST-AUTO-002"
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.rerun_passed,
            ),
        )

    def test_search_by_execution_cycle(self) -> None:
        result = self.repository.search_text(
            "UAT Cycle 1"
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.blocked,
                self.rerun_passed,
            ),
        )

    def test_search_by_executor(self) -> None:
        result = self.repository.search_text(
            "business tester"
        )

        self.assertEqual(
            result,
            (self.blocked,),
        )

    def test_search_by_build_version(self) -> None:
        result = self.repository.search_text(
            "2.2.0-RC2"
        )

        self.assertEqual(
            result,
            (self.rerun_passed,),
        )

    def test_search_by_external_reference(self) -> None:
        result = self.repository.search_text(
            "PIPELINE-1001"
        )

        self.assertEqual(
            result,
            (self.passed,),
        )

    def test_search_by_defect_id(self) -> None:
        result = self.repository.search_text(
            "BUG-201"
        )

        self.assertEqual(
            result,
            (self.blocked,),
        )

    def test_search_by_evidence_id(self) -> None:
        result = self.repository.search_text(
            "REPORT-001"
        )

        self.assertEqual(
            result,
            (self.passed,),
        )

    def test_search_by_remarks(self) -> None:
        result = self.repository.search_text(
            "payment service"
        )

        self.assertEqual(
            result,
            (self.blocked,),
        )

    def test_search_by_rerun_execution_id(self) -> None:
        result = self.repository.search_text(
            "EXEC-004"
        )

        self.assertEqual(
            result,
            (
                self.failed,
                self.rerun_passed,
            ),
        )

    def test_search_is_case_insensitive(self) -> None:
        result = self.repository.search_text(
            "AUTOMATION SERVICE"
        )

        self.assertEqual(
            result,
            (
                self.passed,
                self.failed,
                self.rerun_passed,
            ),
        )

    def test_search_returns_empty_tuple_when_no_match(
        self,
    ) -> None:
        result = self.repository.search_text(
            "nonexistent-value"
        )

        self.assertEqual(result, ())

    def test_blank_search_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.search_text(" ")

    def test_non_string_search_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.search_text(  # type: ignore[arg-type]
                123
            )


if __name__ == "__main__":
    unittest.main()
