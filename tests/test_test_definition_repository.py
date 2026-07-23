
"""Unit tests for the canonical Test Definition repository."""

import sys
import unittest
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
    TestStep,
)
from repositories.base import (  # noqa: E402
    DuplicateItemError,
    ItemNotFoundError,
    RepositoryValidationError,
)
from repositories.test_definition_repository import (  # noqa: E402
    TestDefinitionRepository,
)


def manual_test_definition(
    test_definition_id: str = "TEST-MANUAL-001",
    *,
    scenario_id: str = "SCN-001",
    name: str = "Create page manually",
    status: TestDefinitionStatus | str = "ACTIVE",
    version: str = "1.0",
    description: str | None = (
        "Verify that an authenticated user can create a page."
    ),
    preconditions: tuple[str, ...] | list[str] = (
        "The user is authenticated.",
    ),
    steps: tuple[TestStep, ...] | list[TestStep] | None = None,
    owner: str | None = "Manual QA",
    tags: tuple[str, ...] | list[str] = (
        "functional",
        "manual",
    ),
) -> TestDefinition:
    """Create a valid Manual Test Definition."""

    if steps is None:
        steps = [
            TestStep(
                step_number=1,
                action="Open the create-page screen.",
                expected_result="The create-page screen is displayed.",
            ),
            TestStep(
                step_number=2,
                action="Enter a title and page content.",
                expected_result="The entered values are accepted.",
                test_data="Title: Functional Testing Dashboard",
            ),
            TestStep(
                step_number=3,
                action="Select Save.",
                expected_result="The page is created successfully.",
            ),
        ]

    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type=TestType.MANUAL,
        name=name,
        status=status,
        version=version,
        description=description,
        preconditions=preconditions,
        steps=steps,
        owner=owner,
        tags=tags,
    )


def automation_test_definition(
    test_definition_id: str = "TEST-AUTO-001",
    *,
    scenario_id: str = "SCN-001",
    name: str = "Create page using automation",
    status: TestDefinitionStatus | str = "ACTIVE",
    version: str = "1.0",
    description: str | None = (
        "Automated validation of successful page creation."
    ),
    preconditions: tuple[str, ...] | list[str] = (
        "The application is available.",
    ),
    framework: AutomationFramework | str = "PLAYWRIGHT",
    repository: str | None = "functional-dashboard-tests",
    script_path: str = "tests/pages/test_create_page.py",
    pipeline_name: str | None = "functional-regression",
    owner: str | None = "Automation QA",
    tags: tuple[str, ...] | list[str] = (
        "functional",
        "automation",
    ),
) -> TestDefinition:
    """Create a valid Automation Test Definition."""

    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type=TestType.AUTOMATION,
        name=name,
        status=status,
        version=version,
        description=description,
        preconditions=preconditions,
        framework=framework,
        repository=repository,
        script_path=script_path,
        pipeline_name=pipeline_name,
        owner=owner,
        tags=tags,
    )


class TestDefinitionRepositoryCrudTests(unittest.TestCase):
    """Tests covering basic repository behaviour."""

    def setUp(self) -> None:
        self.repository = TestDefinitionRepository()

    def test_repository_starts_empty(self) -> None:
        self.assertEqual(self.repository.count(), 0)
        self.assertEqual(self.repository.list_all(), ())

    def test_add_and_get_test_definition(self) -> None:
        item = manual_test_definition()

        self.repository.add(item)

        self.assertEqual(
            self.repository.get("TEST-MANUAL-001"),
            item,
        )

    def test_duplicate_test_definition_is_rejected(self) -> None:
        self.repository.add(manual_test_definition())

        with self.assertRaises(DuplicateItemError):
            self.repository.add(
                manual_test_definition(
                    name="Updated manual test"
                )
            )

    def test_get_missing_test_definition_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.get("TEST-MISSING")

    def test_replace_test_definition(self) -> None:
        original = manual_test_definition()
        replacement = manual_test_definition(
            name="Updated manual definition",
            version="1.1",
        )

        self.repository.add(original)
        previous = self.repository.replace(replacement)

        self.assertEqual(previous, original)
        self.assertEqual(
            self.repository.get("TEST-MANUAL-001"),
            replacement,
        )

    def test_remove_test_definition(self) -> None:
        item = manual_test_definition()
        self.repository.add(item)

        removed = self.repository.remove(
            "TEST-MANUAL-001"
        )

        self.assertEqual(removed, item)
        self.assertEqual(self.repository.count(), 0)

    def test_list_all_is_sorted_by_test_definition_id(
        self,
    ) -> None:
        self.repository.add_many(
            [
                manual_test_definition(
                    "TEST-MANUAL-003",
                    name="Third test",
                ),
                manual_test_definition(
                    "TEST-MANUAL-001",
                    name="First test",
                ),
                manual_test_definition(
                    "TEST-MANUAL-002",
                    name="Second test",
                ),
            ]
        )

        result = self.repository.list_all()

        self.assertEqual(
            tuple(
                item.test_definition_id
                for item in result
            ),
            (
                "TEST-MANUAL-001",
                "TEST-MANUAL-002",
                "TEST-MANUAL-003",
            ),
        )

    def test_incorrect_object_type_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add(  # type: ignore[arg-type]
                {
                    "test_definition_id": (
                        "TEST-MANUAL-001"
                    )
                }
            )


class TestDefinitionRepositoryFixtureTests(
    unittest.TestCase
):
    """Shared fixture for repository query tests."""

    def setUp(self) -> None:
        self.repository = TestDefinitionRepository()

        self.manual_active = manual_test_definition(
            "TEST-MANUAL-001",
            scenario_id="SCN-001",
            name="Create Confluence page manually",
            status="ACTIVE",
            version="1.0",
            description=(
                "Verify successful Confluence page creation."
            ),
            owner="Manual QA",
            tags=["functional", "content"],
        )

        self.manual_draft = manual_test_definition(
            "TEST-MANUAL-002",
            scenario_id="SCN-002",
            name="Validate blank page title",
            status="DRAFT",
            version="1.1",
            description=(
                "Verify the validation shown for a blank title."
            ),
            steps=[
                TestStep(
                    step_number=1,
                    action="Open the create-page screen.",
                    expected_result=(
                        "The create-page screen is displayed."
                    ),
                ),
                TestStep(
                    step_number=2,
                    action="Leave the page title blank.",
                    expected_result=(
                        "The title remains empty."
                    ),
                ),
                TestStep(
                    step_number=3,
                    action="Select Save.",
                    expected_result=(
                        "A title validation message is displayed."
                    ),
                    test_data="Blank title",
                ),
            ],
            owner=None,
            tags=["manual", "validation"],
        )

        self.playwright_active = (
            automation_test_definition(
                "TEST-AUTO-001",
                scenario_id="SCN-001",
                name="Create Confluence page with Playwright",
                status="ACTIVE",
                version="2.0",
                description=(
                    "Automated browser validation for page creation."
                ),
                framework="PLAYWRIGHT",
                repository="functional-dashboard-tests",
                script_path=(
                    "tests/confluence/test_create_page.py"
                ),
                pipeline_name="functional-regression",
                owner="Automation QA",
                tags=["automation", "content"],
            )
        )

        self.pytest_deprecated = (
            automation_test_definition(
                "TEST-AUTO-002",
                scenario_id="SCN-003",
                name="Search Jira issues using API",
                status="DEPRECATED",
                version="1.2.3",
                description=(
                    "Automated Jira API search validation."
                ),
                framework="PYTEST",
                repository="mcp-functional-tests",
                script_path="tests/jira/test_search.py",
                pipeline_name=None,
                owner="Automation QA",
                tags=["automation", "integration", "search"],
            )
        )

        self.selenium_retired = (
            automation_test_definition(
                "TEST-AUTO-003",
                scenario_id="SCN-004",
                name="Handle GitHub login failure",
                status="RETIRED",
                version="3.0",
                description=(
                    "Legacy browser test for authentication errors."
                ),
                preconditions=[
                    "Invalid credentials are configured."
                ],
                framework="SELENIUM",
                repository="legacy-ui-tests",
                script_path=(
                    "tests/github/test_login_failure.py"
                ),
                pipeline_name="legacy-regression",
                owner="Legacy QA",
                tags=[
                    "automation",
                    "authentication",
                    "negative",
                ],
            )
        )

        self.playwright_no_pipeline = (
            automation_test_definition(
                "TEST-AUTO-004",
                scenario_id="SCN-005",
                name="Smoke test Jira search",
                status="ACTIVE",
                version="1.0",
                description=(
                    "Basic automated Jira search smoke test."
                ),
                framework="PLAYWRIGHT",
                repository="functional-dashboard-tests",
                script_path="tests/jira/test_smoke_search.py",
                pipeline_name=None,
                owner=None,
                tags=["automation", "smoke", "search"],
            )
        )

        self.repository.add_many(
            [
                self.manual_active,
                self.manual_draft,
                self.playwright_active,
                self.pytest_deprecated,
                self.selenium_retired,
                self.playwright_no_pipeline,
            ]
        )


class TestDefinitionRelationshipFilterTests(
    TestDefinitionRepositoryFixtureTests
):
    """Tests covering Scenario relationship filtering."""

    def test_find_by_scenario_id(self) -> None:
        result = self.repository.find_by_scenario_id(
            "SCN-001"
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.manual_active,
            ),
        )

    def test_find_by_scenario_id_trims_input(self) -> None:
        result = self.repository.find_by_scenario_id(
            " SCN-003 "
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_find_by_scenario_id_is_case_sensitive(
        self,
    ) -> None:
        result = self.repository.find_by_scenario_id(
            "scn-001"
        )

        self.assertEqual(result, ())

    def test_blank_scenario_id_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_scenario_id(" ")

    def test_non_string_scenario_id_is_rejected(
        self,
    ) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_scenario_id(  # type: ignore[arg-type]
                123
            )


class TestDefinitionTypeFilterTests(
    TestDefinitionRepositoryFixtureTests
):
    """Tests covering Manual and Automation filtering."""

    def test_find_by_manual_test_type(self) -> None:
        result = self.repository.find_by_test_type(
            TestType.MANUAL
        )

        self.assertEqual(
            result,
            (
                self.manual_active,
                self.manual_draft,
            ),
        )

    def test_find_by_automation_test_type(self) -> None:
        result = self.repository.find_by_test_type(
            " automation "
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.pytest_deprecated,
                self.selenium_retired,
                self.playwright_no_pipeline,
            ),
        )

    def test_find_manual_convenience_method(self) -> None:
        self.assertEqual(
            self.repository.find_manual(),
            (
                self.manual_active,
                self.manual_draft,
            ),
        )

    def test_find_automation_convenience_method(
        self,
    ) -> None:
        self.assertEqual(
            self.repository.find_automation(),
            (
                self.playwright_active,
                self.pytest_deprecated,
                self.selenium_retired,
                self.playwright_no_pipeline,
            ),
        )

    def test_invalid_test_type_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_test_type("HYBRID")


class TestDefinitionStatusFilterTests(
    TestDefinitionRepositoryFixtureTests
):
    """Tests covering lifecycle status filtering."""

    def test_find_active_status(self) -> None:
        result = self.repository.find_by_status(
            TestDefinitionStatus.ACTIVE
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.playwright_no_pipeline,
                self.manual_active,
            ),
        )

    def test_find_draft_status(self) -> None:
        result = self.repository.find_by_status(
            " draft "
        )

        self.assertEqual(
            result,
            (self.manual_draft,),
        )

    def test_find_deprecated_status(self) -> None:
        result = self.repository.find_by_status(
            "DEPRECATED"
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_find_retired_status(self) -> None:
        result = self.repository.find_by_status(
            "RETIRED"
        )

        self.assertEqual(
            result,
            (self.selenium_retired,),
        )

    def test_invalid_status_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_status("IN_REVIEW")


class TestDefinitionAutomationFilterTests(
    TestDefinitionRepositoryFixtureTests
):
    """Tests covering Automation-specific filters."""

    def test_find_by_framework(self) -> None:
        result = self.repository.find_by_framework(
            AutomationFramework.PLAYWRIGHT
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.playwright_no_pipeline,
            ),
        )

    def test_find_by_framework_accepts_string(self) -> None:
        result = self.repository.find_by_framework(
            " pytest "
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_manual_definitions_are_not_returned_by_framework(
        self,
    ) -> None:
        result = self.repository.find_by_framework(
            "PLAYWRIGHT"
        )

        self.assertNotIn(
            self.manual_active,
            result,
        )

    def test_invalid_framework_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_framework("APPIUM")

    def test_find_by_repository(self) -> None:
        result = self.repository.find_by_repository(
            "functional-dashboard-tests"
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.playwright_no_pipeline,
            ),
        )

    def test_find_by_repository_is_case_insensitive(
        self,
    ) -> None:
        result = self.repository.find_by_repository(
            " FUNCTIONAL-DASHBOARD-TESTS "
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.playwright_no_pipeline,
            ),
        )

    def test_find_by_pipeline_name(self) -> None:
        result = self.repository.find_by_pipeline_name(
            "functional-regression"
        )

        self.assertEqual(
            result,
            (self.playwright_active,),
        )

    def test_find_by_pipeline_name_is_case_insensitive(
        self,
    ) -> None:
        result = self.repository.find_by_pipeline_name(
            " LEGACY-REGRESSION "
        )

        self.assertEqual(
            result,
            (self.selenium_retired,),
        )

    def test_find_automation_without_pipeline(self) -> None:
        result = (
            self.repository
            .find_automation_without_pipeline()
        )

        self.assertEqual(
            result,
            (
                self.pytest_deprecated,
                self.playwright_no_pipeline,
            ),
        )

    def test_manual_test_without_pipeline_is_not_returned(
        self,
    ) -> None:
        result = (
            self.repository
            .find_automation_without_pipeline()
        )

        self.assertNotIn(
            self.manual_active,
            result,
        )

    def test_blank_repository_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_repository(" ")

    def test_blank_pipeline_name_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_pipeline_name(" ")


class TestDefinitionGeneralFilterTests(
    TestDefinitionRepositoryFixtureTests
):
    """Tests covering general Test Definition filters."""

    def test_find_by_version(self) -> None:
        result = self.repository.find_by_version("1.0")

        self.assertEqual(
            result,
            (
                self.playwright_no_pipeline,
                self.manual_active,
            ),
        )

    def test_find_by_version_trims_input(self) -> None:
        result = self.repository.find_by_version(
            " 1.2.3 "
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_find_by_owner(self) -> None:
        result = self.repository.find_by_owner(
            "Automation QA"
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.pytest_deprecated,
            ),
        )

    def test_find_by_owner_is_case_insensitive(
        self,
    ) -> None:
        result = self.repository.find_by_owner(
            " manual qa "
        )

        self.assertEqual(
            result,
            (self.manual_active,),
        )

    def test_find_by_tag(self) -> None:
        result = self.repository.find_by_tag(
            " search "
        )

        self.assertEqual(
            result,
            (
                self.pytest_deprecated,
                self.playwright_no_pipeline,
            ),
        )

    def test_find_without_owner(self) -> None:
        result = self.repository.find_without_owner()

        self.assertEqual(
            result,
            (
                self.playwright_no_pipeline,
                self.manual_draft,
            ),
        )

    def test_blank_owner_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_owner(" ")

    def test_blank_tag_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_tag(" ")

    def test_blank_version_is_rejected(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.find_by_version(" ")


class TestDefinitionSearchTests(
    TestDefinitionRepositoryFixtureTests
):
    """Tests covering multi-field text search."""

    def test_search_by_test_definition_id(self) -> None:
        result = self.repository.search_text(
            "TEST-AUTO-002"
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_search_by_scenario_id(self) -> None:
        result = self.repository.search_text(
            "SCN-001"
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.manual_active,
            ),
        )

    def test_search_by_name(self) -> None:
        result = self.repository.search_text(
            "blank page title"
        )

        self.assertEqual(
            result,
            (self.manual_draft,),
        )

    def test_search_by_description(self) -> None:
        result = self.repository.search_text(
            "Jira API search"
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_search_by_version(self) -> None:
        result = self.repository.search_text(
            "1.2.3"
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_search_by_precondition(self) -> None:
        result = self.repository.search_text(
            "invalid credentials"
        )

        self.assertEqual(
            result,
            (self.selenium_retired,),
        )

    def test_search_by_manual_step_action(self) -> None:
        result = self.repository.search_text(
            "leave the page title blank"
        )

        self.assertEqual(
            result,
            (self.manual_draft,),
        )

    def test_search_by_manual_expected_result(
        self,
    ) -> None:
        result = self.repository.search_text(
            "title validation message"
        )

        self.assertEqual(
            result,
            (self.manual_draft,),
        )

    def test_search_by_manual_test_data(self) -> None:
        result = self.repository.search_text(
            "blank title"
        )

        self.assertEqual(
            result,
            (self.manual_draft,),
        )

    def test_search_by_repository(self) -> None:
        result = self.repository.search_text(
            "mcp-functional-tests"
        )

        self.assertEqual(
            result,
            (self.pytest_deprecated,),
        )

    def test_search_by_script_path(self) -> None:
        result = self.repository.search_text(
            "test_smoke_search.py"
        )

        self.assertEqual(
            result,
            (self.playwright_no_pipeline,),
        )

    def test_search_by_pipeline_name(self) -> None:
        result = self.repository.search_text(
            "functional-regression"
        )

        self.assertEqual(
            result,
            (self.playwright_active,),
        )

    def test_search_by_owner(self) -> None:
        result = self.repository.search_text(
            "legacy qa"
        )

        self.assertEqual(
            result,
            (self.selenium_retired,),
        )

    def test_search_by_tag(self) -> None:
        result = self.repository.search_text(
            "authentication"
        )

        self.assertEqual(
            result,
            (self.selenium_retired,),
        )

    def test_search_is_case_insensitive(self) -> None:
        result = self.repository.search_text(
            "CONFLUENCE"
        )

        self.assertEqual(
            result,
            (
                self.playwright_active,
                self.manual_active,
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
