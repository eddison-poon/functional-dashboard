"""Unit tests for the canonical Scenario repository."""

import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.enums import Priority, ScenarioType  # noqa: E402
from canonical.scenario import Scenario  # noqa: E402
from repositories.base import (  # noqa: E402
    DuplicateItemError,
    ItemNotFoundError,
    RepositoryValidationError,
)
from repositories.scenario_repository import (  # noqa: E402
    ScenarioRepository,
)


def scenario(
    scenario_id: str = "SCN-001",
    *,
    feature_id: str = "FEATURE-CONFLUENCE",
    requirement_ids: tuple[str, ...] | list[str] = (
        "REQ-001",
    ),
    name: str = "Create Confluence page",
    scenario_type: ScenarioType | str = "POSITIVE",
    priority: Priority | str = "HIGH",
    description: str | None = (
        "A user creates a Confluence page successfully."
    ),
    tags: tuple[str, ...] | list[str] = (
        "functional",
        "content",
    ),
    preconditions: tuple[str, ...] | list[str] = (
        "The user is authenticated.",
    ),
    expected_outcome: str | None = (
        "The page is created successfully."
    ),
    owner: str | None = "QA Team",
    active: bool = True,
) -> Scenario:
    """Create a valid Scenario for repository tests."""
    return Scenario(
        scenario_id=scenario_id,
        feature_id=feature_id,
        requirement_ids=requirement_ids,
        name=name,
        scenario_type=scenario_type,
        priority=priority,
        description=description,
        tags=tags,
        preconditions=preconditions,
        expected_outcome=expected_outcome,
        owner=owner,
        active=active,
    )


class ScenarioRepositoryCrudTests(unittest.TestCase):
    """Tests covering Scenario repository CRUD behaviour."""

    def setUp(self) -> None:
        self.repository = ScenarioRepository()

    def test_repository_starts_empty(self) -> None:
        self.assertEqual(self.repository.count(), 0)
        self.assertEqual(self.repository.list_all(), ())

    def test_add_and_get_scenario(self) -> None:
        item = scenario()

        self.repository.add(item)

        self.assertEqual(
            self.repository.get("SCN-001"),
            item,
        )

    def test_duplicate_scenario_is_rejected(self) -> None:
        self.repository.add(scenario())

        with self.assertRaises(DuplicateItemError):
            self.repository.add(
                scenario(name="Updated scenario")
            )

    def test_get_missing_scenario_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.get("SCN-999")

    def test_replace_scenario(self) -> None:
        original = scenario()
        replacement = scenario(
            name="Updated scenario name"
        )

        self.repository.add(original)
        previous = self.repository.replace(replacement)

        self.assertEqual(previous, original)
        self.assertEqual(
            self.repository.get("SCN-001"),
            replacement,
        )

    def test_remove_scenario(self) -> None:
        item = scenario()
        self.repository.add(item)

        removed = self.repository.remove("SCN-001")

        self.assertEqual(removed, item)
        self.assertEqual(self.repository.count(), 0)

    def test_list_all_is_sorted_by_scenario_id(self) -> None:
        self.repository.add_many(
            [
                scenario("SCN-003", name="Third"),
                scenario("SCN-001", name="First"),
                scenario("SCN-002", name="Second"),
            ]
        )

        result = self.repository.list_all()

        self.assertEqual(
            tuple(item.scenario_id for item in result),
            (
                "SCN-001",
                "SCN-002",
                "SCN-003",
            ),
        )

    def test_incorrect_object_type_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add(  # type: ignore[arg-type]
                {"scenario_id": "SCN-001"}
            )


class ScenarioRepositoryFixtureTests(unittest.TestCase):
    """Base fixture for Scenario repository query tests."""

    def setUp(self) -> None:
        self.repository = ScenarioRepository()

        self.scenario_1 = scenario(
            "SCN-001",
            feature_id="FEATURE-CONFLUENCE",
            requirement_ids=["REQ-001", "REQ-010"],
            name="Create Confluence page",
            scenario_type="POSITIVE",
            priority="HIGH",
            description=(
                "A user creates a new Confluence page."
            ),
            tags=["functional", "content"],
            preconditions=[
                "The user is authenticated.",
                "The space exists.",
            ],
            expected_outcome=(
                "The page is created and visible."
            ),
            owner="QA Team",
            active=True,
        )

        self.scenario_2 = scenario(
            "SCN-002",
            feature_id="FEATURE-CONFLUENCE",
            requirement_ids=["REQ-001"],
            name="Reject blank page title",
            scenario_type="NEGATIVE",
            priority="HIGH",
            description=(
                "The application rejects a blank title."
            ),
            tags=["functional", "validation"],
            preconditions=[
                "The user is authenticated.",
            ],
            expected_outcome=(
                "A validation message is displayed."
            ),
            owner="QA Team",
            active=True,
        )

        self.scenario_3 = scenario(
            "SCN-003",
            feature_id="FEATURE-JIRA",
            requirement_ids=["REQ-002", "REQ-010"],
            name="Search Jira issues",
            scenario_type="INTEGRATION",
            priority="CRITICAL",
            description=(
                "The agent searches Jira through the MCP gateway."
            ),
            tags=["integration", "search"],
            preconditions=[
                "Jira is available.",
                "The user has search permission.",
            ],
            expected_outcome=(
                "Matching Jira issues are returned."
            ),
            owner="Automation Team",
            active=True,
        )

        self.scenario_4 = scenario(
            "SCN-004",
            feature_id="FEATURE-GITHUB",
            requirement_ids=["REQ-003"],
            name="Handle GitHub authentication error",
            scenario_type="ERROR_HANDLING",
            priority="MEDIUM",
            description=(
                "The application handles invalid GitHub credentials."
            ),
            tags=["negative", "authentication"],
            preconditions=[
                "Invalid credentials are configured.",
            ],
            expected_outcome=(
                "A controlled authentication error is shown."
            ),
            owner=None,
            active=False,
        )

        self.scenario_5 = scenario(
            "SCN-005",
            feature_id="FEATURE-JIRA",
            requirement_ids=["REQ-002"],
            name="Smoke test Jira search",
            scenario_type="SMOKE",
            priority="LOW",
            description=(
                "Basic Jira search is verified after deployment."
            ),
            tags=["smoke", "search"],
            preconditions=[
                "The deployment is complete.",
            ],
            expected_outcome=(
                "A basic issue search succeeds."
            ),
            owner="Release QA",
            active=True,
        )

        self.repository.add_many(
            [
                self.scenario_1,
                self.scenario_2,
                self.scenario_3,
                self.scenario_4,
                self.scenario_5,
            ]
        )


class ScenarioRepositoryRelationshipFilterTests(
    ScenarioRepositoryFixtureTests
):
    """Tests covering feature and requirement filters."""

    def test_find_by_feature_id(self) -> None:
        result = self.repository.find_by_feature_id(
            "FEATURE-CONFLUENCE"
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
            ),
        )

    def test_find_by_feature_id_is_case_insensitive(self) -> None:
        result = self.repository.find_by_feature_id(
            " feature-jira "
        )

        self.assertEqual(
            result,
            (
                self.scenario_3,
                self.scenario_5,
            ),
        )

    def test_find_by_requirement_id(self) -> None:
        result = self.repository.find_by_requirement_id(
            "REQ-001"
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
            ),
        )

    def test_find_by_requirement_id_trims_input(self) -> None:
        result = self.repository.find_by_requirement_id(
            " REQ-010 "
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_3,
            ),
        )

    def test_find_by_requirement_id_is_case_sensitive(self) -> None:
        result = self.repository.find_by_requirement_id(
            "req-001"
        )

        self.assertEqual(result, ())

    def test_find_by_any_requirement_id(self) -> None:
        result = self.repository.find_by_any_requirement_id(
            ["REQ-002", "REQ-003"]
        )

        self.assertEqual(
            result,
            (
                self.scenario_3,
                self.scenario_4,
                self.scenario_5,
            ),
        )

    def test_find_by_all_requirement_ids(self) -> None:
        result = self.repository.find_by_all_requirement_ids(
            ["REQ-001", "REQ-010"]
        )

        self.assertEqual(
            result,
            (self.scenario_1,),
        )

    def test_requirement_collection_deduplicates_input(self) -> None:
        result = self.repository.find_by_any_requirement_id(
            ["REQ-002", "REQ-002"]
        )

        self.assertEqual(
            result,
            (
                self.scenario_3,
                self.scenario_5,
            ),
        )

    def test_empty_requirement_collection_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_any_requirement_id([])

    def test_single_string_requirement_collection_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_any_requirement_id(
                "REQ-001"  # type: ignore[arg-type]
            )

    def test_invalid_requirement_collection_item_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_any_requirement_id(
                [
                    "REQ-001",
                    123,  # type: ignore[list-item]
                ]
            )


class ScenarioRepositoryControlledFilterTests(
    ScenarioRepositoryFixtureTests
):
    """Tests covering enum-based Scenario filters."""

    def test_find_by_type(self) -> None:
        result = self.repository.find_by_type(
            ScenarioType.NEGATIVE
        )

        self.assertEqual(
            result,
            (self.scenario_2,),
        )

    def test_find_by_type_accepts_case_insensitive_string(
        self,
    ) -> None:
        result = self.repository.find_by_type(
            " error_handling "
        )

        self.assertEqual(
            result,
            (self.scenario_4,),
        )

    def test_find_by_priority(self) -> None:
        result = self.repository.find_by_priority(
            Priority.HIGH
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
            ),
        )

    def test_invalid_scenario_type_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_type(
                "UNKNOWN"
            )

    def test_invalid_priority_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_priority(
                "URGENT"
            )


class ScenarioRepositoryTextFilterTests(
    ScenarioRepositoryFixtureTests
):
    """Tests covering Scenario text filters."""

    def test_find_by_owner(self) -> None:
        result = self.repository.find_by_owner(
            "qa team"
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
            ),
        )

    def test_find_by_tag(self) -> None:
        result = self.repository.find_by_tag(
            " SEARCH "
        )

        self.assertEqual(
            result,
            (
                self.scenario_3,
                self.scenario_5,
            ),
        )

    def test_text_filter_returns_empty_tuple_when_no_match(
        self,
    ) -> None:
        result = self.repository.find_by_owner(
            "Unknown Owner"
        )

        self.assertEqual(result, ())

    def test_blank_owner_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_owner(" ")

    def test_blank_tag_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_tag(" ")

    def test_non_string_owner_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_owner(  # type: ignore[arg-type]
                123
            )


class ScenarioRepositoryActiveFilterTests(
    ScenarioRepositoryFixtureTests
):
    """Tests covering active-state filtering."""

    def test_find_active_scenarios(self) -> None:
        result = self.repository.find_active()

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
                self.scenario_3,
                self.scenario_5,
            ),
        )

    def test_find_inactive_scenarios(self) -> None:
        result = self.repository.find_active(False)

        self.assertEqual(
            result,
            (self.scenario_4,),
        )

    def test_find_active_rejects_non_boolean(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_active(  # type: ignore[arg-type]
                1
            )


class ScenarioRepositorySearchTests(
    ScenarioRepositoryFixtureTests
):
    """Tests covering multi-field text search."""

    def test_search_by_scenario_id(self) -> None:
        result = self.repository.search_text("SCN-003")

        self.assertEqual(
            result,
            (self.scenario_3,),
        )

    def test_search_by_feature_id(self) -> None:
        result = self.repository.search_text(
            "feature-confluence"
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
            ),
        )

    def test_search_by_requirement_id(self) -> None:
        result = self.repository.search_text(
            "REQ-010"
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_3,
            ),
        )

    def test_search_by_name(self) -> None:
        result = self.repository.search_text(
            "blank page title"
        )

        self.assertEqual(
            result,
            (self.scenario_2,),
        )

    def test_search_by_description(self) -> None:
        result = self.repository.search_text(
            "mcp gateway"
        )

        self.assertEqual(
            result,
            (self.scenario_3,),
        )

    def test_search_by_tag(self) -> None:
        result = self.repository.search_text(
            "authentication"
        )

        self.assertEqual(
            result,
            (self.scenario_4,),
        )

    def test_search_by_precondition(self) -> None:
        result = self.repository.search_text(
            "space exists"
        )

        self.assertEqual(
            result,
            (self.scenario_1,),
        )

    def test_search_by_expected_outcome(self) -> None:
        result = self.repository.search_text(
            "validation message"
        )

        self.assertEqual(
            result,
            (self.scenario_2,),
        )

    def test_search_by_owner(self) -> None:
        result = self.repository.search_text(
            "release qa"
        )

        self.assertEqual(
            result,
            (self.scenario_5,),
        )

    def test_search_is_case_insensitive(self) -> None:
        result = self.repository.search_text(
            "CONFLUENCE"
        )

        self.assertEqual(
            result,
            (
                self.scenario_1,
                self.scenario_2,
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


if __name__ == "__main__":
    unittest.main()
