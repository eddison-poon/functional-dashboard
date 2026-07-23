
"""Unit tests for the canonical Requirement repository."""

import sys
import unittest
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
from canonical.requirement import Requirement  # noqa: E402
from repositories.base import (  # noqa: E402
    DuplicateItemError,
    ItemNotFoundError,
    RepositoryValidationError,
)
from repositories.requirement_repository import (  # noqa: E402
    RequirementRepository,
)


def requirement(
    requirement_id: str = "REQ-001",
    *,
    title: str = "Create Confluence page",
    source_system: SourceSystem | str = "JIRA",
    requirement_type: RequirementType | str = "STORY",
    status: RequirementStatus | str = "READY",
    priority: Priority | str = "HIGH",
    description: str | None = (
        "Users can create a page in Confluence."
    ),
    source_project: str | None = "AGENT-HUB",
    source_url: str | None = None,
    component: str | None = "Confluence",
    labels: tuple[str, ...] | list[str] = (
        "functional",
        "content",
    ),
    release: str | None = "Release 1",
    sprint: str | None = "Sprint 10",
    owner: str | None = "QA Team",
    active: bool = True,
) -> Requirement:
    """Create a valid Requirement for repository tests."""
    return Requirement(
        requirement_id=requirement_id,
        title=title,
        source_system=source_system,
        requirement_type=requirement_type,
        status=status,
        priority=priority,
        description=description,
        source_project=source_project,
        source_url=source_url,
        component=component,
        labels=labels,
        release=release,
        sprint=sprint,
        owner=owner,
        active=active,
    )


class RequirementRepositoryCrudTests(unittest.TestCase):
    """Tests covering Requirement repository CRUD behaviour."""

    def setUp(self) -> None:
        self.repository = RequirementRepository()

    def test_repository_starts_empty(self) -> None:
        self.assertEqual(self.repository.count(), 0)
        self.assertEqual(self.repository.list_all(), ())

    def test_add_and_get_requirement(self) -> None:
        item = requirement()

        self.repository.add(item)

        self.assertEqual(
            self.repository.get("REQ-001"),
            item,
        )

    def test_duplicate_requirement_is_rejected(self) -> None:
        self.repository.add(requirement())

        with self.assertRaises(DuplicateItemError):
            self.repository.add(
                requirement(title="Updated title")
            )

    def test_get_missing_requirement_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.get("REQ-999")

    def test_replace_requirement(self) -> None:
        original = requirement()
        replacement = requirement(
            title="Updated requirement title"
        )

        self.repository.add(original)
        previous = self.repository.replace(replacement)

        self.assertEqual(previous, original)
        self.assertEqual(
            self.repository.get("REQ-001"),
            replacement,
        )

    def test_remove_requirement(self) -> None:
        item = requirement()
        self.repository.add(item)

        removed = self.repository.remove("REQ-001")

        self.assertEqual(removed, item)
        self.assertEqual(self.repository.count(), 0)

    def test_list_all_is_sorted_by_requirement_id(self) -> None:
        self.repository.add_many(
            [
                requirement(
                    "REQ-003",
                    title="Third",
                ),
                requirement(
                    "REQ-001",
                    title="First",
                ),
                requirement(
                    "REQ-002",
                    title="Second",
                ),
            ]
        )

        result = self.repository.list_all()

        self.assertEqual(
            tuple(
                item.requirement_id
                for item in result
            ),
            (
                "REQ-001",
                "REQ-002",
                "REQ-003",
            ),
        )

    def test_incorrect_object_type_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add(  # type: ignore[arg-type]
                {"requirement_id": "REQ-001"}
            )


class RequirementRepositoryFixtureTests(unittest.TestCase):
    """Base fixture for Requirement query tests."""

    def setUp(self) -> None:
        self.repository = RequirementRepository()

        self.requirement_1 = requirement(
            "REQ-001",
            title="Create Confluence page",
            source_system="JIRA",
            requirement_type="STORY",
            status="READY",
            priority="HIGH",
            description=(
                "A user can create new Confluence content."
            ),
            source_project="AGENT-HUB",
            component="Confluence",
            labels=["functional", "content"],
            release="Release 1",
            sprint="Sprint 10",
            owner="QA Team",
            active=True,
        )

        self.requirement_2 = requirement(
            "REQ-002",
            title="Search Jira issues",
            source_system="XRAY",
            requirement_type="TECHNICAL_REQUIREMENT",
            status="IN_PROGRESS",
            priority="CRITICAL",
            description=(
                "The agent searches Jira issues by query."
            ),
            source_project="AGENT-HUB",
            component="Jira",
            labels=["functional", "search"],
            release="Release 1",
            sprint="Sprint 11",
            owner="Automation Team",
            active=True,
        )

        self.requirement_3 = requirement(
            "REQ-003",
            title="Retired legacy integration",
            source_system="CSV",
            requirement_type="OTHER",
            status="DONE",
            priority="LOW",
            description="Legacy connector no longer used.",
            source_project="LEGACY",
            component="Confluence",
            labels=["legacy", "integration"],
            release="Release 0",
            sprint=None,
            owner="QA Team",
            active=False,
        )

        self.requirement_4 = requirement(
            "REQ-004",
            title="Handle GitHub authentication failure",
            source_system="JIRA",
            requirement_type="BUG",
            status="BLOCKED",
            priority="HIGH",
            description=(
                "Display a controlled error when authentication fails."
            ),
            source_project="DEV-TOOLS",
            component="GitHub",
            labels=["negative", "authentication"],
            release="Release 2",
            sprint="Sprint 11",
            owner=None,
            active=True,
        )

        self.repository.add_many(
            [
                self.requirement_1,
                self.requirement_2,
                self.requirement_3,
                self.requirement_4,
            ]
        )


class RequirementRepositoryControlledFilterTests(
    RequirementRepositoryFixtureTests
):
    """Tests covering enum-based Requirement filters."""

    def test_find_by_status(self) -> None:
        result = self.repository.find_by_status(
            RequirementStatus.READY
        )

        self.assertEqual(result, (self.requirement_1,))

    def test_find_by_status_accepts_case_insensitive_string(
        self,
    ) -> None:
        result = self.repository.find_by_status(
            " in_progress "
        )

        self.assertEqual(result, (self.requirement_2,))

    def test_find_by_priority(self) -> None:
        result = self.repository.find_by_priority("HIGH")

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_4,
            ),
        )

    def test_find_by_type(self) -> None:
        result = self.repository.find_by_type("BUG")

        self.assertEqual(result, (self.requirement_4,))

    def test_find_by_source_system(self) -> None:
        result = self.repository.find_by_source_system(
            SourceSystem.JIRA
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_4,
            ),
        )

    def test_invalid_status_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_status(
                "UNKNOWN"
            )

    def test_invalid_priority_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_priority(
                "URGENT"
            )


class RequirementRepositoryTextFilterTests(
    RequirementRepositoryFixtureTests
):
    """Tests covering Requirement text filters."""

    def test_find_by_source_project(self) -> None:
        result = self.repository.find_by_source_project(
            "agent-hub"
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_2,
            ),
        )

    def test_find_by_component(self) -> None:
        result = self.repository.find_by_component(
            " confluence "
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_3,
            ),
        )

    def test_find_by_owner(self) -> None:
        result = self.repository.find_by_owner(
            "qa team"
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_3,
            ),
        )

    def test_find_by_label(self) -> None:
        result = self.repository.find_by_label(
            " FUNCTIONAL "
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_2,
            ),
        )

    def test_find_by_release(self) -> None:
        result = self.repository.find_by_release(
            "release 1"
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_2,
            ),
        )

    def test_find_by_sprint(self) -> None:
        result = self.repository.find_by_sprint(
            "SPRINT 11"
        )

        self.assertEqual(
            result,
            (
                self.requirement_2,
                self.requirement_4,
            ),
        )

    def test_text_filter_returns_empty_tuple_when_no_match(
        self,
    ) -> None:
        result = self.repository.find_by_owner(
            "Unknown Owner"
        )

        self.assertEqual(result, ())

    def test_blank_text_filter_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_component(" ")

    def test_non_string_text_filter_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_owner(  # type: ignore[arg-type]
                123
            )


class RequirementRepositoryActiveFilterTests(
    RequirementRepositoryFixtureTests
):
    """Tests covering active-state filtering."""

    def test_find_active_requirements(self) -> None:
        result = self.repository.find_active()

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_2,
                self.requirement_4,
            ),
        )

    def test_find_inactive_requirements(self) -> None:
        result = self.repository.find_active(False)

        self.assertEqual(
            result,
            (self.requirement_3,),
        )

    def test_find_active_rejects_non_boolean(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_active(  # type: ignore[arg-type]
                1
            )


class RequirementRepositorySearchTests(
    RequirementRepositoryFixtureTests
):
    """Tests covering multi-field text search."""

    def test_search_by_requirement_id(self) -> None:
        result = self.repository.search_text("REQ-002")

        self.assertEqual(result, (self.requirement_2,))

    def test_search_by_title(self) -> None:
        result = self.repository.search_text(
            "authentication failure"
        )

        self.assertEqual(result, (self.requirement_4,))

    def test_search_by_description(self) -> None:
        result = self.repository.search_text(
            "create new confluence"
        )

        self.assertEqual(result, (self.requirement_1,))

    def test_search_by_component(self) -> None:
        result = self.repository.search_text(
            "github"
        )

        self.assertEqual(result, (self.requirement_4,))

    def test_search_by_label(self) -> None:
        result = self.repository.search_text(
            "integration"
        )

        self.assertEqual(result, (self.requirement_3,))

    def test_search_by_owner(self) -> None:
        result = self.repository.search_text(
            "automation team"
        )

        self.assertEqual(result, (self.requirement_2,))

    def test_search_by_release(self) -> None:
        result = self.repository.search_text(
            "release 1"
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_2,
            ),
        )

    def test_search_is_case_insensitive(self) -> None:
        result = self.repository.search_text(
            "CONFLUENCE"
        )

        self.assertEqual(
            result,
            (
                self.requirement_1,
                self.requirement_3,
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
