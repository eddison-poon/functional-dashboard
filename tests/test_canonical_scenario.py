
"""Unit tests for the canonical Scenario model."""

import json
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))


from canonical.enums import Priority, ScenarioType  # noqa: E402
from canonical.scenario import (  # noqa: E402
    Scenario,
    ScenarioValidationError,
)


def create_valid_scenario(**overrides: object) -> Scenario:
    """Create a valid Scenario with optional field overrides."""

    payload: dict[str, object] = {
        "scenario_id": "SCN-JIRA-0001",
        "feature_id": "create-jira-ticket",
        "requirement_ids": ["AHP-1042"],
        "name": "Create a Jira ticket using mandatory fields",
        "scenario_type": "POSITIVE",
        "priority": "HIGH",
        "description": (
            "Verify that an authorized user can create a Jira ticket "
            "when all required information is supplied."
        ),
        "tags": ["Smoke", " Regression "],
        "preconditions": [
            "The Jira MCP service is available",
            "The user has permission to create issues",
        ],
        "expected_outcome": (
            "A Jira issue is created with the submitted "
            "mandatory values."
        ),
        "owner": "QA Team",
        "active": True,
    }

    payload.update(overrides)

    return Scenario(**payload)


class ScenarioCreationTests(unittest.TestCase):
    """Tests covering successful Scenario creation."""

    def test_create_valid_scenario(self) -> None:
        scenario = create_valid_scenario()

        self.assertEqual(
            scenario.scenario_id,
            "SCN-JIRA-0001",
        )
        self.assertEqual(
            scenario.feature_id,
            "create-jira-ticket",
        )
        self.assertEqual(
            scenario.requirement_ids,
            ("AHP-1042",),
        )
        self.assertEqual(
            scenario.scenario_type,
            ScenarioType.POSITIVE,
        )
        self.assertEqual(
            scenario.priority,
            Priority.HIGH,
        )

    def test_required_text_is_trimmed(self) -> None:
        scenario = create_valid_scenario(
            scenario_id="  SCN-JIRA-0001  ",
            feature_id="  create-jira-ticket  ",
            name="  Create a Jira ticket  ",
        )

        self.assertEqual(
            scenario.scenario_id,
            "SCN-JIRA-0001",
        )
        self.assertEqual(
            scenario.feature_id,
            "create-jira-ticket",
        )
        self.assertEqual(
            scenario.name,
            "Create a Jira ticket",
        )

    def test_controlled_values_are_case_insensitive(self) -> None:
        scenario = create_valid_scenario(
            scenario_type="positive",
            priority="high",
        )

        self.assertEqual(
            scenario.scenario_type,
            ScenarioType.POSITIVE,
        )
        self.assertEqual(
            scenario.priority,
            Priority.HIGH,
        )

    def test_requirement_ids_are_trimmed_and_deduplicated(
        self,
    ) -> None:
        scenario = create_valid_scenario(
            requirement_ids=[
                "AHP-1042",
                " AHP-1043 ",
                "AHP-1042",
            ]
        )

        self.assertEqual(
            scenario.requirement_ids,
            ("AHP-1042", "AHP-1043"),
        )

    def test_tags_are_normalized_and_deduplicated(self) -> None:
        scenario = create_valid_scenario(
            tags=[
                "Smoke",
                " regression ",
                "SMOKE",
                "",
                "Regression",
            ]
        )

        self.assertEqual(
            scenario.tags,
            ("smoke", "regression"),
        )

    def test_preconditions_are_trimmed_and_deduplicated(
        self,
    ) -> None:
        scenario = create_valid_scenario(
            preconditions=[
                " The Jira MCP service is available ",
                "The user has permission",
                "",
                "The Jira MCP service is available",
            ]
        )

        self.assertEqual(
            scenario.preconditions,
            (
                "The Jira MCP service is available",
                "The user has permission",
            ),
        )

    def test_blank_optional_text_becomes_none(self) -> None:
        scenario = create_valid_scenario(
            description="   ",
            expected_outcome="",
            owner=None,
        )

        self.assertIsNone(scenario.description)
        self.assertIsNone(scenario.expected_outcome)
        self.assertIsNone(scenario.owner)

    def test_optional_collections_default_to_empty_tuples(
        self,
    ) -> None:
        scenario = Scenario(
            scenario_id="SCN-JIRA-0001",
            feature_id="create-jira-ticket",
            requirement_ids=["AHP-1042"],
            name="Create a Jira ticket",
            scenario_type="POSITIVE",
            priority="HIGH",
        )

        self.assertEqual(scenario.tags, ())
        self.assertEqual(scenario.preconditions, ())

    def test_scenario_is_immutable(self) -> None:
        scenario = create_valid_scenario()

        with self.assertRaises(FrozenInstanceError):
            scenario.name = "Changed behaviour"  # type: ignore[misc]


class ScenarioValidationTests(unittest.TestCase):
    """Tests covering Scenario validation failures."""

    def test_empty_scenario_id_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(scenario_id="   ")

    def test_non_string_scenario_id_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(scenario_id=1001)

    def test_empty_feature_id_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(feature_id="")

    def test_empty_name_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(name="   ")

    def test_empty_requirement_collection_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(requirement_ids=[])

    def test_none_requirement_collection_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(requirement_ids=None)

    def test_requirement_ids_as_string_are_rejected(
        self,
    ) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(
                requirement_ids="AHP-1042"
            )

    def test_blank_requirement_id_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(
                requirement_ids=["AHP-1042", "  "]
            )

    def test_non_string_requirement_id_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(
                requirement_ids=["AHP-1042", 1043]
            )

    def test_tags_as_string_are_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(tags="smoke")

    def test_non_string_tag_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(
                tags=["smoke", 100]
            )

    def test_preconditions_as_string_are_rejected(
        self,
    ) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(
                preconditions="Service is available"
            )

    def test_non_string_precondition_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(
                preconditions=["Service is available", 100]
            )

    def test_invalid_scenario_type_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_valid_scenario(
                scenario_type="FUNCTIONAL"
            )

    def test_invalid_priority_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_valid_scenario(priority="URGENT")

    def test_boolean_string_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(active="true")

    def test_overlong_name_is_rejected(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            create_valid_scenario(name="x" * 301)


class ScenarioSerializationTests(unittest.TestCase):
    """Tests covering dictionary and JSON conversion."""

    def test_to_dict_returns_json_compatible_values(self) -> None:
        scenario = create_valid_scenario()

        result = scenario.to_dict()

        self.assertEqual(
            result["scenario_type"],
            "POSITIVE",
        )
        self.assertEqual(result["priority"], "HIGH")
        self.assertEqual(
            result["requirement_ids"],
            ["AHP-1042"],
        )
        self.assertEqual(
            result["tags"],
            ["smoke", "regression"],
        )

    def test_to_dict_can_be_serialized_with_standard_json(
        self,
    ) -> None:
        scenario = create_valid_scenario()

        serialized = json.dumps(scenario.to_dict())

        self.assertIn(
            '"scenario_id": "SCN-JIRA-0001"',
            serialized,
        )
        self.assertIn(
            '"scenario_type": "POSITIVE"',
            serialized,
        )

    def test_from_dict_builds_scenario(self) -> None:
        original = create_valid_scenario()

        reconstructed = Scenario.from_dict(
            original.to_dict()
        )

        self.assertEqual(reconstructed, original)

    def test_from_dict_rejects_non_mapping_input(self) -> None:
        with self.assertRaises(ScenarioValidationError):
            Scenario.from_dict(  # type: ignore[arg-type]
                ["not", "a", "mapping"]
            )

    def test_from_dict_rejects_unknown_fields(self) -> None:
        payload = create_valid_scenario().to_dict()
        payload["unknown_field"] = "unexpected"

        with self.assertRaises(ScenarioValidationError):
            Scenario.from_dict(payload)

    def test_from_dict_rejects_missing_required_field(
        self,
    ) -> None:
        payload = create_valid_scenario().to_dict()
        del payload["feature_id"]

        with self.assertRaises(ScenarioValidationError):
            Scenario.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
