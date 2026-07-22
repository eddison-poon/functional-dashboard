"""Unit tests for the canonical Requirement model."""

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
    Priority,
    RequirementStatus,
    RequirementType,
    SourceSystem,
)
from canonical.requirement import (  # noqa: E402
    Requirement,
    RequirementValidationError,
)


def create_valid_requirement(**overrides: object) -> Requirement:
    """Create a valid Requirement with optional field overrides."""

    payload: dict[str, object] = {
        "requirement_id": "AHP-1042",
        "title": "Support Jira ticket creation",
        "source_system": "JIRA",
        "requirement_type": "STORY",
        "status": "IN_PROGRESS",
        "priority": "HIGH",
        "description": "Allow agents to create Jira tickets.",
        "source_project": "AHP",
        "source_url": (
            "https://company.atlassian.net/browse/AHP-1042"
        ),
        "component": "AI Platform - AgentHub",
        "labels": ["MCP", " jira-tool ", "Regression"],
        "release": "R2026.08",
        "sprint": "Sprint 12",
        "owner": "Product Owner",
        "active": True,
    }

    payload.update(overrides)

    return Requirement(**payload)


class RequirementCreationTests(unittest.TestCase):
    """Tests covering successful Requirement creation."""

    def test_create_valid_requirement(self) -> None:
        requirement = create_valid_requirement()

        self.assertEqual(requirement.requirement_id, "AHP-1042")
        self.assertEqual(
            requirement.source_system,
            SourceSystem.JIRA,
        )
        self.assertEqual(
            requirement.requirement_type,
            RequirementType.STORY,
        )
        self.assertEqual(
            requirement.status,
            RequirementStatus.IN_PROGRESS,
        )
        self.assertEqual(
            requirement.priority,
            Priority.HIGH,
        )

    def test_required_text_is_trimmed(self) -> None:
        requirement = create_valid_requirement(
            requirement_id="  AHP-1042  ",
            title="  Support Jira ticket creation  ",
        )

        self.assertEqual(requirement.requirement_id, "AHP-1042")
        self.assertEqual(
            requirement.title,
            "Support Jira ticket creation",
        )

    def test_controlled_values_are_case_insensitive(self) -> None:
        requirement = create_valid_requirement(
            source_system="jira",
            requirement_type="story",
            status="in_progress",
            priority="high",
        )

        self.assertEqual(
            requirement.source_system,
            SourceSystem.JIRA,
        )
        self.assertEqual(
            requirement.requirement_type,
            RequirementType.STORY,
        )
        self.assertEqual(
            requirement.status,
            RequirementStatus.IN_PROGRESS,
        )
        self.assertEqual(
            requirement.priority,
            Priority.HIGH,
        )

    def test_optional_blank_strings_become_none(self) -> None:
        requirement = create_valid_requirement(
            description="  ",
            source_project="",
            source_url=None,
            component=" ",
            release="",
            sprint=None,
            owner="   ",
        )

        self.assertIsNone(requirement.description)
        self.assertIsNone(requirement.source_project)
        self.assertIsNone(requirement.source_url)
        self.assertIsNone(requirement.component)
        self.assertIsNone(requirement.release)
        self.assertIsNone(requirement.sprint)
        self.assertIsNone(requirement.owner)

    def test_labels_are_normalized_and_deduplicated(self) -> None:
        requirement = create_valid_requirement(
            labels=[
                "Regression",
                " mcp ",
                "regression",
                "",
                "MCP",
                " jira-tool ",
            ]
        )

        self.assertEqual(
            requirement.labels,
            ("regression", "mcp", "jira-tool"),
        )

    def test_labels_default_to_empty_tuple(self) -> None:
        requirement = Requirement(
            requirement_id="AHP-1042",
            title="Support Jira ticket creation",
            source_system="JIRA",
            requirement_type="STORY",
            status="READY",
            priority="MEDIUM",
        )

        self.assertEqual(requirement.labels, ())

    def test_requirement_is_immutable(self) -> None:
        requirement = create_valid_requirement()

        with self.assertRaises(FrozenInstanceError):
            requirement.title = "Changed title"  # type: ignore[misc]


class RequirementValidationTests(unittest.TestCase):
    """Tests covering Requirement validation failures."""

    def test_empty_requirement_id_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(requirement_id="   ")

    def test_non_string_requirement_id_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(requirement_id=1042)

    def test_empty_title_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(title="")

    def test_overlong_title_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(title="x" * 301)

    def test_invalid_source_url_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(
                source_url="company.atlassian.net/browse/AHP-1042"
            )

    def test_ftp_source_url_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(
                source_url="ftp://company.example/AHP-1042"
            )

    def test_labels_as_single_string_are_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(labels="regression")

    def test_non_string_label_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(
                labels=["regression", 123]
            )

    def test_invalid_boolean_string_is_rejected(self) -> None:
        with self.assertRaises(RequirementValidationError):
            create_valid_requirement(active="true")

    def test_invalid_requirement_status_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_valid_requirement(status="UNDER_REVIEW")

    def test_invalid_requirement_type_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_valid_requirement(
                requirement_type="USER_STORY"
            )


class RequirementSerializationTests(unittest.TestCase):
    """Tests covering dictionary and JSON conversion."""

    def test_to_dict_returns_json_compatible_values(self) -> None:
        requirement = create_valid_requirement()

        result = requirement.to_dict()

        self.assertEqual(result["source_system"], "JIRA")
        self.assertEqual(result["requirement_type"], "STORY")
        self.assertEqual(result["status"], "IN_PROGRESS")
        self.assertEqual(result["priority"], "HIGH")
        self.assertEqual(
            result["labels"],
            ["mcp", "jira-tool", "regression"],
        )

    def test_to_dict_can_be_serialized_with_standard_json(self) -> None:
        requirement = create_valid_requirement()

        serialized = json.dumps(requirement.to_dict())

        self.assertIn('"requirement_id": "AHP-1042"', serialized)
        self.assertIn('"status": "IN_PROGRESS"', serialized)

    def test_from_dict_builds_requirement(self) -> None:
        payload = create_valid_requirement().to_dict()

        reconstructed = Requirement.from_dict(payload)

        self.assertEqual(
            reconstructed,
            create_valid_requirement(),
        )

    def test_from_dict_rejects_non_mapping_input(self) -> None:
        with self.assertRaises(RequirementValidationError):
            Requirement.from_dict(  # type: ignore[arg-type]
                ["not", "a", "mapping"]
            )

    def test_from_dict_rejects_unknown_fields(self) -> None:
        payload = create_valid_requirement().to_dict()
        payload["unknown_field"] = "unexpected"

        with self.assertRaises(RequirementValidationError):
            Requirement.from_dict(payload)

    def test_from_dict_rejects_missing_required_field(self) -> None:
        payload = create_valid_requirement().to_dict()
        del payload["title"]

        with self.assertRaises(RequirementValidationError):
            Requirement.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
