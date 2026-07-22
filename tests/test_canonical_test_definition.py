
"""Unit tests for the canonical Test Definition model."""

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))


from canonical.enums import (  # noqa: E402
    AutomationFramework,
    TestDefinitionStatus,
    TestType,
)
from canonical.test_definition import (  # noqa: E402
    TestDefinition,
    TestDefinitionValidationError,
    TestStep,
)


def valid_manual_definition(**overrides: object) -> TestDefinition:
    """Create a valid Manual Test Definition."""

    payload: dict[str, object] = {
        "test_definition_id": "MCP-JIRA-M-001",
        "scenario_id": "SCN-JIRA-0001",
        "test_type": "MANUAL",
        "name": "Create Jira ticket using mandatory fields",
        "status": "ACTIVE",
        "version": "1.0",
        "description": "Validate Jira ticket creation.",
        "preconditions": [
            "The Jira MCP service is available",
        ],
        "steps": [
            {
                "step_number": 1,
                "action": "Submit a valid request",
                "expected_result": "The request is accepted",
                "test_data": "Project=AHP",
            },
            {
                "step_number": 2,
                "action": "Open the created ticket",
                "expected_result": "Submitted values are displayed",
            },
        ],
        "owner": "QA Team",
        "tags": ["Manual", " Regression "],
    }

    payload.update(overrides)

    return TestDefinition(**payload)


def valid_automation_definition(
    **overrides: object,
) -> TestDefinition:
    """Create a valid Automation Test Definition."""

    payload: dict[str, object] = {
        "test_definition_id": "MCP-JIRA-A-001",
        "scenario_id": "SCN-JIRA-0001",
        "test_type": "AUTOMATION",
        "name": "Automated Jira ticket creation validation",
        "status": "ACTIVE",
        "version": "1.3",
        "framework": "PYTEST",
        "repository": "agenthub-functional-tests",
        "script_path": "tests/jira/test_create_ticket.py",
        "pipeline_name": "jira-mcp-regression",
        "owner": "QA Automation Team",
        "tags": ["Automation", "Regression"],
    }

    payload.update(overrides)

    return TestDefinition(**payload)


class TestStepTests(unittest.TestCase):
    """Tests covering manual Test Step behaviour."""

    def test_create_valid_step(self) -> None:
        step = TestStep(
            step_number=1,
            action="Submit a request",
            expected_result="The request is accepted",
            test_data="Project=AHP",
        )

        self.assertEqual(step.step_number, 1)
        self.assertEqual(step.action, "Submit a request")

    def test_step_text_is_trimmed(self) -> None:
        step = TestStep(
            step_number=1,
            action="  Submit a request  ",
            expected_result="  Request is accepted  ",
            test_data="  Project=AHP  ",
        )

        self.assertEqual(step.action, "Submit a request")
        self.assertEqual(
            step.expected_result,
            "Request is accepted",
        )
        self.assertEqual(step.test_data, "Project=AHP")

    def test_blank_test_data_becomes_none(self) -> None:
        step = TestStep(
            step_number=1,
            action="Submit a request",
            expected_result="Request is accepted",
            test_data=" ",
        )

        self.assertIsNone(step.test_data)

    def test_zero_step_number_is_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            TestStep(
                step_number=0,
                action="Submit a request",
                expected_result="Request is accepted",
            )

    def test_boolean_step_number_is_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            TestStep(
                step_number=True,
                action="Submit a request",
                expected_result="Request is accepted",
            )

    def test_empty_action_is_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            TestStep(
                step_number=1,
                action=" ",
                expected_result="Request is accepted",
            )

    def test_step_is_immutable(self) -> None:
        step = TestStep(
            step_number=1,
            action="Submit a request",
            expected_result="Request is accepted",
        )

        with self.assertRaises(FrozenInstanceError):
            step.action = "Changed"  # type: ignore[misc]


class ManualTestDefinitionTests(unittest.TestCase):
    """Tests covering Manual Test Definitions."""

    def test_create_valid_manual_definition(self) -> None:
        definition = valid_manual_definition()

        self.assertEqual(definition.test_type, TestType.MANUAL)
        self.assertEqual(
            definition.status,
            TestDefinitionStatus.ACTIVE,
        )
        self.assertEqual(len(definition.steps), 2)
        self.assertIsInstance(definition.steps[0], TestStep)

    def test_manual_definition_requires_steps(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(steps=[])

    def test_manual_definition_rejects_framework(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(framework="PYTEST")

    def test_manual_definition_rejects_script_path(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(
                script_path="tests/test_ticket.py"
            )

    def test_duplicate_step_numbers_are_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(
                steps=[
                    {
                        "step_number": 1,
                        "action": "First action",
                        "expected_result": "First result",
                    },
                    {
                        "step_number": 1,
                        "action": "Second action",
                        "expected_result": "Second result",
                    },
                ]
            )

    def test_non_continuous_steps_are_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(
                steps=[
                    {
                        "step_number": 1,
                        "action": "First action",
                        "expected_result": "First result",
                    },
                    {
                        "step_number": 3,
                        "action": "Third action",
                        "expected_result": "Third result",
                    },
                ]
            )


class AutomationTestDefinitionTests(unittest.TestCase):
    """Tests covering Automation Test Definitions."""

    def test_create_valid_automation_definition(self) -> None:
        definition = valid_automation_definition()

        self.assertEqual(
            definition.test_type,
            TestType.AUTOMATION,
        )
        self.assertEqual(
            definition.framework,
            AutomationFramework.PYTEST,
        )
        self.assertEqual(definition.steps, ())

    def test_automation_requires_framework(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_automation_definition(framework=None)

    def test_automation_requires_script_path(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_automation_definition(script_path=None)

    def test_automation_rejects_manual_steps(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_automation_definition(
                steps=[
                    {
                        "step_number": 1,
                        "action": "Run the test",
                        "expected_result": "Test passes",
                    }
                ]
            )

    def test_automation_framework_is_case_insensitive(
        self,
    ) -> None:
        definition = valid_automation_definition(
            framework="pytest"
        )

        self.assertEqual(
            definition.framework,
            AutomationFramework.PYTEST,
        )


class CommonTestDefinitionTests(unittest.TestCase):
    """Tests covering shared Test Definition behaviour."""

    def test_required_text_is_trimmed(self) -> None:
        definition = valid_manual_definition(
            test_definition_id="  MCP-JIRA-M-001  ",
            scenario_id="  SCN-JIRA-0001  ",
            name="  Create Jira ticket  ",
        )

        self.assertEqual(
            definition.test_definition_id,
            "MCP-JIRA-M-001",
        )
        self.assertEqual(
            definition.scenario_id,
            "SCN-JIRA-0001",
        )
        self.assertEqual(
            definition.name,
            "Create Jira ticket",
        )

    def test_controlled_values_are_case_insensitive(self) -> None:
        definition = valid_manual_definition(
            test_type="manual",
            status="active",
        )

        self.assertEqual(definition.test_type, TestType.MANUAL)
        self.assertEqual(
            definition.status,
            TestDefinitionStatus.ACTIVE,
        )

    def test_tags_are_normalized_and_deduplicated(self) -> None:
        definition = valid_manual_definition(
            tags=[
                "Manual",
                " regression ",
                "MANUAL",
                "",
            ]
        )

        self.assertEqual(
            definition.tags,
            ("manual", "regression"),
        )

    def test_preconditions_are_normalized(self) -> None:
        definition = valid_manual_definition(
            preconditions=[
                " Service is available ",
                "",
                "Service is available",
            ]
        )

        self.assertEqual(
            definition.preconditions,
            ("Service is available",),
        )

    def test_invalid_version_is_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(version="version-one")

    def test_single_number_version_is_rejected(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            valid_manual_definition(version="1")

    def test_patch_version_is_accepted(self) -> None:
        definition = valid_manual_definition(version="2.1.3")

        self.assertEqual(definition.version, "2.1.3")

    def test_definition_is_immutable(self) -> None:
        definition = valid_manual_definition()

        with self.assertRaises(FrozenInstanceError):
            definition.name = "Changed"  # type: ignore[misc]


class TestDefinitionSerializationTests(unittest.TestCase):
    """Tests covering dictionary and JSON conversion."""

    def test_manual_to_dict_is_json_compatible(self) -> None:
        definition = valid_manual_definition()

        result = definition.to_dict()

        self.assertEqual(result["test_type"], "MANUAL")
        self.assertEqual(result["status"], "ACTIVE")
        self.assertEqual(result["steps"][0]["step_number"], 1)
        self.assertIsNone(result["framework"])

        serialized = json.dumps(result)

        self.assertIn(
            '"test_definition_id": "MCP-JIRA-M-001"',
            serialized,
        )

    def test_automation_to_dict_is_json_compatible(self) -> None:
        definition = valid_automation_definition()

        result = definition.to_dict()

        self.assertEqual(result["test_type"], "AUTOMATION")
        self.assertEqual(result["framework"], "PYTEST")
        self.assertEqual(result["steps"], [])

    def test_manual_from_dict_round_trip(self) -> None:
        original = valid_manual_definition()

        reconstructed = TestDefinition.from_dict(
            original.to_dict()
        )

        self.assertEqual(reconstructed, original)

    def test_automation_from_dict_round_trip(self) -> None:
        original = valid_automation_definition()

        reconstructed = TestDefinition.from_dict(
            original.to_dict()
        )

        self.assertEqual(reconstructed, original)

    def test_from_dict_rejects_unknown_field(self) -> None:
        payload = valid_manual_definition().to_dict()
        payload["unknown_field"] = "unexpected"

        with self.assertRaises(TestDefinitionValidationError):
            TestDefinition.from_dict(payload)

    def test_from_dict_rejects_missing_required_field(
        self,
    ) -> None:
        payload = valid_manual_definition().to_dict()
        del payload["scenario_id"]

        with self.assertRaises(TestDefinitionValidationError):
            TestDefinition.from_dict(payload)

    def test_from_dict_rejects_non_mapping(self) -> None:
        with self.assertRaises(TestDefinitionValidationError):
            TestDefinition.from_dict(  # type: ignore[arg-type]
                ["not", "a", "mapping"]
            )


if __name__ == "__main__":
    unittest.main()
