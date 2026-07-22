
"""Unit tests for the canonical controlled vocabularies."""

import json
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))


from canonical.enums import (  # noqa: E402
    Environment,
    EvidenceType,
    ExecutionStatus,
    InvalidEnumValueError,
    Priority,
    RequirementStatus,
    RequirementType,
    ScenarioType,
    Severity,
    SourceSystem,
    TestDefinitionStatus,
    TestType,
)


class CanonicalEnumTests(unittest.TestCase):
    """Tests shared behaviour provided by CanonicalEnum."""

    def test_parse_exact_value(self) -> None:
        result = ExecutionStatus.parse("PASSED")

        self.assertEqual(result, ExecutionStatus.PASSED)

    def test_parse_is_case_insensitive(self) -> None:
        result = ExecutionStatus.parse("passed")

        self.assertEqual(result, ExecutionStatus.PASSED)

    def test_parse_ignores_surrounding_whitespace(self) -> None:
        result = ExecutionStatus.parse("  failed  ")

        self.assertEqual(result, ExecutionStatus.FAILED)

    def test_parse_accepts_existing_enum_member(self) -> None:
        result = ExecutionStatus.parse(ExecutionStatus.BLOCKED)

        self.assertIs(result, ExecutionStatus.BLOCKED)

    def test_invalid_value_is_rejected(self) -> None:
        with self.assertRaises(InvalidEnumValueError) as context:
            ExecutionStatus.parse("SUCCESSFUL")

        message = str(context.exception)

        self.assertIn("SUCCESSFUL", message)
        self.assertIn("ExecutionStatus", message)
        self.assertIn("PASSED", message)

    def test_none_is_rejected(self) -> None:
        with self.assertRaises(InvalidEnumValueError):
            ExecutionStatus.parse(None)

    def test_empty_string_is_rejected(self) -> None:
        with self.assertRaises(InvalidEnumValueError):
            ExecutionStatus.parse("   ")

    def test_contains_returns_true_for_valid_value(self) -> None:
        self.assertTrue(ExecutionStatus.contains("passed"))

    def test_contains_returns_false_for_invalid_value(self) -> None:
        self.assertFalse(ExecutionStatus.contains("unknown"))

    def test_values_returns_canonical_values(self) -> None:
        self.assertEqual(
            ExecutionStatus.values(),
            (
                "PASSED",
                "FAILED",
                "BLOCKED",
                "NOT_EXECUTED",
                "SKIPPED",
                "ABORTED",
                "IN_PROGRESS",
            ),
        )

    def test_enum_serializes_to_json_string(self) -> None:
        payload = {
            "status": ExecutionStatus.PASSED,
            "environment": Environment.SIT,
        }

        serialized = json.dumps(payload)

        self.assertEqual(
            serialized,
            '{"status": "PASSED", "environment": "SIT"}',
        )


class VocabularyDefinitionTests(unittest.TestCase):
    """Verify the approved values for each Version 1 vocabulary."""

    def test_requirement_status_values(self) -> None:
        self.assertEqual(
            RequirementStatus.values(),
            (
                "DRAFT",
                "READY",
                "IN_PROGRESS",
                "BLOCKED",
                "DONE",
                "CANCELLED",
            ),
        )

    def test_requirement_type_values(self) -> None:
    self.assertEqual(
        RequirementType.values(),
        (
            "EPIC",
            "STORY",
            "TASK",
            "BUG",
            "CHANGE_REQUEST",
            "TECHNICAL_REQUIREMENT",
            "BUSINESS_REQUIREMENT",
            "OTHER",
        ),
    )

    def test_test_definition_status_values(self) -> None:
        self.assertEqual(
            TestDefinitionStatus.values(),
            (
                "DRAFT",
                "ACTIVE",
                "RETIRED",
                "DEPRECATED",
            ),
        )

    def test_test_type_values(self) -> None:
        self.assertEqual(
            TestType.values(),
            (
                "MANUAL",
                "AUTOMATION",
            ),
        )

    def test_environment_values(self) -> None:
        self.assertEqual(
            Environment.values(),
            (
                "DEV",
                "SIT",
                "UAT",
                "PRE_PRODUCTION",
                "PRODUCTION_VERIFICATION",
            ),
        )

    def test_priority_values(self) -> None:
        self.assertEqual(
            Priority.values(),
            (
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW",
            ),
        )

    def test_severity_values(self) -> None:
        self.assertEqual(
            Severity.values(),
            (
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW",
            ),
        )

    def test_scenario_type_values(self) -> None:
        self.assertEqual(
            ScenarioType.values(),
            (
                "POSITIVE",
                "NEGATIVE",
                "BOUNDARY",
                "PERMISSION",
                "INTEGRATION",
                "ERROR_HANDLING",
                "REGRESSION",
                "SMOKE",
            ),
        )

    def test_evidence_type_values(self) -> None:
        self.assertEqual(
            EvidenceType.values(),
            (
                "SCREENSHOT",
                "LOG",
                "VIDEO",
                "REPORT",
                "TRACE",
                "API_RESPONSE",
                "ATTACHMENT",
            ),
        )

    def test_source_system_values(self) -> None:
        self.assertEqual(
            SourceSystem.values(),
            (
                "JIRA",
                "XRAY",
                "ZEPHYR",
                "TESTRAIL",
                "CSV",
                "GITHUB_ACTIONS",
                "JENKINS",
                "PLAYWRIGHT",
                "SELENIUM",
                "PYTEST",
                "MANUAL_ENTRY",
            ),
        )


if __name__ == "__main__":
    unittest.main()
