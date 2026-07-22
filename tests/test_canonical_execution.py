
"""Unit tests for the canonical Execution model."""

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
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
from canonical.execution import (  # noqa: E402
    Execution,
    ExecutionValidationError,
)


STARTED_AT = datetime(
    2026,
    7,
    23,
    9,
    0,
    tzinfo=timezone.utc,
)

COMPLETED_AT = datetime(
    2026,
    7,
    23,
    9,
    15,
    tzinfo=timezone.utc,
)


def valid_execution(**overrides: object) -> Execution:
    """Create a valid completed Execution."""
    payload: dict[str, object] = {
        "execution_id": "EXEC-SIT-0001",
        "test_definition_id": "MCP-JIRA-M-001",
        "environment": "SIT",
        "status": "PASSED",
        "execution_cycle": "RELEASE-2-REGRESSION",
        "started_at": STARTED_AT,
        "completed_at": COMPLETED_AT,
        "executed_by": "QA Tester",
        "build_version": "2.4.0",
        "source_system": "MANUAL_ENTRY",
        "external_reference": "XRAY-EXEC-1001",
        "defect_ids": [],
        "evidence_ids": ["EVD-0001"],
        "remarks": "Execution completed successfully.",
    }

    payload.update(overrides)
    return Execution(**payload)


class ExecutionCreationTests(unittest.TestCase):
    """Tests covering valid Execution creation."""

    def test_create_valid_execution(self) -> None:
        execution = valid_execution()

        self.assertEqual(
            execution.environment,
            Environment.SIT,
        )
        self.assertEqual(
            execution.status,
            ExecutionStatus.PASSED,
        )
        self.assertEqual(
            execution.source_system,
            SourceSystem.MANUAL_ENTRY,
        )

    def test_controlled_values_are_case_insensitive(self) -> None:
        execution = valid_execution(
            environment="sit",
            status="passed",
            source_system="manual_entry",
        )

        self.assertEqual(
            execution.environment,
            Environment.SIT,
        )
        self.assertEqual(
            execution.status,
            ExecutionStatus.PASSED,
        )

    def test_required_text_is_trimmed(self) -> None:
        execution = valid_execution(
            execution_id=" EXEC-SIT-0001 ",
            test_definition_id=" MCP-JIRA-M-001 ",
        )

        self.assertEqual(
            execution.execution_id,
            "EXEC-SIT-0001",
        )
        self.assertEqual(
            execution.test_definition_id,
            "MCP-JIRA-M-001",
        )

    def test_optional_text_is_trimmed(self) -> None:
        execution = valid_execution(
            execution_cycle=" RELEASE-2 ",
            executed_by=" QA Tester ",
            build_version=" 2.4.0 ",
            remarks=" Passed successfully ",
        )

        self.assertEqual(
            execution.execution_cycle,
            "RELEASE-2",
        )
        self.assertEqual(
            execution.executed_by,
            "QA Tester",
        )
        self.assertEqual(
            execution.build_version,
            "2.4.0",
        )
        self.assertEqual(
            execution.remarks,
            "Passed successfully",
        )

    def test_blank_optional_text_becomes_none(self) -> None:
        execution = valid_execution(
            external_reference=" ",
            rerun_of_execution_id=" ",
        )

        self.assertIsNone(execution.external_reference)
        self.assertIsNone(execution.rerun_of_execution_id)

    def test_execution_is_immutable(self) -> None:
        execution = valid_execution()

        with self.assertRaises(FrozenInstanceError):
            execution.status = ExecutionStatus.FAILED  # type: ignore[misc]


class ExecutionStatusRuleTests(unittest.TestCase):
    """Tests covering status-specific validation rules."""

    def test_not_executed_without_timestamps_is_valid(self) -> None:
        execution = valid_execution(
            status="NOT_EXECUTED",
            started_at=None,
            completed_at=None,
        )

        self.assertEqual(
            execution.status,
            ExecutionStatus.NOT_EXECUTED,
        )
        self.assertFalse(execution.is_executed)
        self.assertFalse(execution.is_terminal)

    def test_not_executed_rejects_started_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="NOT_EXECUTED",
                started_at=STARTED_AT,
                completed_at=None,
            )

    def test_not_executed_rejects_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="NOT_EXECUTED",
                started_at=None,
                completed_at=COMPLETED_AT,
            )

    def test_in_progress_requires_started_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="IN_PROGRESS",
                started_at=None,
                completed_at=None,
            )

    def test_in_progress_rejects_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="IN_PROGRESS",
                started_at=STARTED_AT,
                completed_at=COMPLETED_AT,
            )

    def test_valid_in_progress_execution(self) -> None:
        execution = valid_execution(
            status="IN_PROGRESS",
            started_at=STARTED_AT,
            completed_at=None,
        )

        self.assertTrue(execution.is_executed)
        self.assertFalse(execution.is_terminal)

    def test_passed_requires_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="PASSED",
                completed_at=None,
            )

    def test_failed_requires_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="FAILED",
                completed_at=None,
            )

    def test_blocked_requires_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="BLOCKED",
                completed_at=None,
            )

    def test_skipped_requires_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="SKIPPED",
                completed_at=None,
            )

    def test_aborted_requires_completed_at(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                status="ABORTED",
                completed_at=None,
            )


class ExecutionTimestampTests(unittest.TestCase):
    """Tests covering Execution timestamps and duration."""

    def test_duration_seconds_is_calculated(self) -> None:
        execution = valid_execution()

        self.assertEqual(
            execution.duration_seconds,
            900.0,
        )

    def test_duration_is_none_without_started_at(self) -> None:
        execution = valid_execution(started_at=None)

        self.assertIsNone(execution.duration_seconds)

    def test_completed_at_before_started_at_is_rejected(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                started_at=COMPLETED_AT,
                completed_at=STARTED_AT,
            )

    def test_naive_started_at_is_rejected(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                started_at=datetime(2026, 7, 23, 9, 0),
            )

    def test_naive_completed_at_is_rejected(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                completed_at=datetime(2026, 7, 23, 9, 15),
            )


class ExecutionRelationshipTests(unittest.TestCase):
    """Tests covering defects, evidence, and reruns."""

    def test_defect_ids_are_trimmed_and_deduplicated(self) -> None:
        execution = valid_execution(
            status="FAILED",
            defect_ids=[
                " JIRA-100 ",
                "JIRA-101",
                "JIRA-100",
                "",
            ],
        )

        self.assertEqual(
            execution.defect_ids,
            ("JIRA-100", "JIRA-101"),
        )

    def test_evidence_ids_are_trimmed_and_deduplicated(self) -> None:
        execution = valid_execution(
            evidence_ids=[
                " EVD-001 ",
                "EVD-002",
                "EVD-001",
            ],
        )

        self.assertEqual(
            execution.evidence_ids,
            ("EVD-001", "EVD-002"),
        )

    def test_single_string_defect_ids_is_rejected(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(defect_ids="JIRA-100")

    def test_non_string_evidence_id_is_rejected(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(evidence_ids=["EVD-001", 123])

    def test_execution_can_reference_previous_execution(self) -> None:
        execution = valid_execution(
            execution_id="EXEC-SIT-0002",
            rerun_of_execution_id="EXEC-SIT-0001",
        )

        self.assertEqual(
            execution.rerun_of_execution_id,
            "EXEC-SIT-0001",
        )

    def test_execution_cannot_reference_itself_as_rerun(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            valid_execution(
                execution_id="EXEC-SIT-0001",
                rerun_of_execution_id="EXEC-SIT-0001",
            )


class ExecutionPropertyTests(unittest.TestCase):
    """Tests covering calculated Execution properties."""

    def test_passed_execution_is_successful(self) -> None:
        execution = valid_execution(status="PASSED")

        self.assertTrue(execution.is_successful)
        self.assertTrue(execution.is_terminal)
        self.assertTrue(execution.is_executed)

    def test_failed_execution_is_not_successful(self) -> None:
        execution = valid_execution(status="FAILED")

        self.assertFalse(execution.is_successful)
        self.assertTrue(execution.is_terminal)

    def test_blocked_execution_is_terminal(self) -> None:
        execution = valid_execution(status="BLOCKED")

        self.assertTrue(execution.is_terminal)
        self.assertFalse(execution.is_successful)


class ExecutionSerializationTests(unittest.TestCase):
    """Tests covering dictionary and JSON conversion."""

    def test_to_dict_is_json_compatible(self) -> None:
        execution = valid_execution()

        result = execution.to_dict()

        self.assertEqual(
            result["environment"],
            "SIT",
        )
        self.assertEqual(
            result["status"],
            "PASSED",
        )
        self.assertEqual(
            result["source_system"],
            "MANUAL_ENTRY",
        )
        self.assertEqual(
            result["started_at"],
            "2026-07-23T09:00:00+00:00",
        )
        self.assertEqual(
            result["completed_at"],
            "2026-07-23T09:15:00+00:00",
        )
        self.assertEqual(
            result["evidence_ids"],
            ["EVD-0001"],
        )

        serialized = json.dumps(result)

        self.assertIn(
            '"execution_id": "EXEC-SIT-0001"',
            serialized,
        )

    def test_from_dict_round_trip(self) -> None:
        original = valid_execution()

        reconstructed = Execution.from_dict(
            original.to_dict()
        )

        self.assertEqual(reconstructed, original)

    def test_from_dict_parses_iso_datetime(self) -> None:
        payload = valid_execution().to_dict()

        execution = Execution.from_dict(payload)

        self.assertEqual(
            execution.started_at,
            STARTED_AT,
        )
        self.assertEqual(
            execution.completed_at,
            COMPLETED_AT,
        )

    def test_from_dict_rejects_invalid_datetime(self) -> None:
        payload = valid_execution().to_dict()
        payload["completed_at"] = "not-a-datetime"

        with self.assertRaises(ExecutionValidationError):
            Execution.from_dict(payload)

    def test_from_dict_rejects_unknown_field(self) -> None:
        payload = valid_execution().to_dict()
        payload["unknown_field"] = "unexpected"

        with self.assertRaises(ExecutionValidationError):
            Execution.from_dict(payload)

    def test_from_dict_rejects_missing_required_field(self) -> None:
        payload = valid_execution().to_dict()
        del payload["test_definition_id"]

        with self.assertRaises(ExecutionValidationError):
            Execution.from_dict(payload)

    def test_from_dict_rejects_non_mapping(self) -> None:
        with self.assertRaises(ExecutionValidationError):
            Execution.from_dict(  # type: ignore[arg-type]
                ["not", "a", "mapping"]
            )


if __name__ == "__main__":
    unittest.main()
