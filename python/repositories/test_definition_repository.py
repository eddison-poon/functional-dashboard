"""Repository for canonical TestDefinition objects.

Purpose
-------
Provides deterministic storage, lookup, filtering, and text-search
operations for canonical manual and automated Test Definitions.

The repository contains no connector, persistence, metrics, execution,
or dashboard-rendering logic. It operates only on validated canonical
TestDefinition instances held in memory.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from canonical.enums import (
    AutomationFramework,
    TestDefinitionStatus,
    TestType,
)
from canonical.test_definition import TestDefinition

from .base import (
    InMemoryRepository,
    RepositoryValidationError,
)


ControlledValue = TypeVar("ControlledValue")


class TestDefinitionRepository(
    InMemoryRepository[TestDefinition]
):
    """In-memory repository for canonical Test Definitions."""

    def __init__(self) -> None:
        """Create an empty Test Definition repository."""
        super().__init__(
            item_type=TestDefinition,
            id_getter=lambda item: item.test_definition_id,
            entity_name="TestDefinition",
        )

    def find_by_scenario_id(
        self,
        scenario_id: str,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions linked to one Scenario.

        Scenario identifiers are matched exactly and case-sensitively
        after surrounding whitespace is removed.
        """
        normalized_scenario_id = self._normalize_identifier(
            scenario_id,
            "scenario_id",
        )

        return self._matching(
            lambda item: (
                item.scenario_id == normalized_scenario_id
            )
        )

    def find_by_test_type(
        self,
        test_type: TestType | str,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions using the requested test type."""
        parsed_test_type = self._parse_controlled_value(
            TestType,
            test_type,
            "test_type",
        )

        return self._matching(
            lambda item: item.test_type is parsed_test_type
        )

    def find_manual(
        self,
    ) -> tuple[TestDefinition, ...]:
        """Return all Manual Test Definitions."""
        return self.find_by_test_type(TestType.MANUAL)

    def find_automation(
        self,
    ) -> tuple[TestDefinition, ...]:
        """Return all Automation Test Definitions."""
        return self.find_by_test_type(TestType.AUTOMATION)

    def find_by_status(
        self,
        status: TestDefinitionStatus | str,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions with the requested lifecycle status."""
        parsed_status = self._parse_controlled_value(
            TestDefinitionStatus,
            status,
            "status",
        )

        return self._matching(
            lambda item: item.status is parsed_status
        )

    def find_by_framework(
        self,
        framework: AutomationFramework | str,
    ) -> tuple[TestDefinition, ...]:
        """Return Automation Test Definitions using a framework.

        Manual Test Definitions have no framework and therefore cannot
        appear in the result.
        """
        parsed_framework = self._parse_controlled_value(
            AutomationFramework,
            framework,
            "framework",
        )

        return self._matching(
            lambda item: item.framework is parsed_framework
        )

    def find_by_version(
        self,
        version: str,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions with an exact version value."""
        normalized_version = self._normalize_identifier(
            version,
            "version",
        )

        return self._matching(
            lambda item: item.version == normalized_version
        )

    def find_by_owner(
        self,
        owner: str,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions assigned to an owner.

        Owner matching is case-insensitive after surrounding whitespace
        is removed.
        """
        normalized_owner = self._normalize_query_text(
            owner,
            "owner",
        )

        return self._matching(
            lambda item: (
                item.owner is not None
                and item.owner.casefold() == normalized_owner
            )
        )

    def find_by_tag(
        self,
        tag: str,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions containing the requested tag.

        Tags are normalized to lowercase by the canonical model.
        """
        normalized_tag = self._normalize_query_text(
            tag,
            "tag",
        )

        return self._matching(
            lambda item: normalized_tag in item.tags
        )

    def find_by_repository(
        self,
        repository: str,
    ) -> tuple[TestDefinition, ...]:
        """Return Automation Test Definitions linked to a repository.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_repository = self._normalize_query_text(
            repository,
            "repository",
        )

        return self._matching(
            lambda item: (
                item.repository is not None
                and item.repository.casefold()
                == normalized_repository
            )
        )

    def find_by_pipeline_name(
        self,
        pipeline_name: str,
    ) -> tuple[TestDefinition, ...]:
        """Return Automation Test Definitions linked to a pipeline.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_pipeline_name = self._normalize_query_text(
            pipeline_name,
            "pipeline_name",
        )

        return self._matching(
            lambda item: (
                item.pipeline_name is not None
                and item.pipeline_name.casefold()
                == normalized_pipeline_name
            )
        )

    def find_without_owner(
        self,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions that do not have an assigned owner."""
        return self._matching(
            lambda item: item.owner is None
        )

    def find_automation_without_pipeline(
        self,
    ) -> tuple[TestDefinition, ...]:
        """Return Automation Test Definitions without a pipeline name.

        This query supports automation backlog and CI/CD readiness
        reporting.
        """
        return self._matching(
            lambda item: (
                item.test_type is TestType.AUTOMATION
                and item.pipeline_name is None
            )
        )

    def search_text(
        self,
        query: str,
    ) -> tuple[TestDefinition, ...]:
        """Search across commonly used Test Definition text fields.

        The search is case-insensitive and performs substring matching
        across:

        - Test Definition ID
        - Scenario ID
        - name
        - version
        - description
        - preconditions
        - manual step actions
        - manual step expected results
        - manual step test data
        - automation repository
        - automation script path
        - pipeline name
        - owner
        - tags
        """
        normalized_query = self._normalize_query_text(
            query,
            "query",
        )

        def matches(item: TestDefinition) -> bool:
            searchable_values: list[str | None] = [
                item.test_definition_id,
                item.scenario_id,
                item.name,
                item.version,
                item.description,
                item.repository,
                item.script_path,
                item.pipeline_name,
                item.owner,
                *item.preconditions,
                *item.tags,
            ]

            for step in item.steps:
                searchable_values.extend(
                    [
                        step.action,
                        step.expected_result,
                        step.test_data,
                    ]
                )

            return any(
                value is not None
                and normalized_query in value.casefold()
                for value in searchable_values
            )

        return self._matching(matches)

    def _matching(
        self,
        predicate: Callable[[TestDefinition], bool],
    ) -> tuple[TestDefinition, ...]:
        """Return sorted Test Definitions satisfying a predicate.

        The inherited list_all() method returns records sorted by
        test_definition_id, so filtered results remain deterministic.
        """
        return tuple(
            item
            for item in self.list_all()
            if predicate(item)
        )

    @staticmethod
    def _normalize_query_text(
        value: object,
        field_name: str,
    ) -> str:
        """Validate and normalize case-insensitive query text."""
        if not isinstance(value, str):
            raise RepositoryValidationError(
                f"{field_name} must be a string."
            )

        normalized_value = value.strip().casefold()

        if not normalized_value:
            raise RepositoryValidationError(
                f"{field_name} must not be empty."
            )

        return normalized_value

    @staticmethod
    def _normalize_identifier(
        value: object,
        field_name: str,
    ) -> str:
        """Validate and trim a case-sensitive identifier or version."""
        if not isinstance(value, str):
            raise RepositoryValidationError(
                f"{field_name} must be a string."
            )

        normalized_value = value.strip()

        if not normalized_value:
            raise RepositoryValidationError(
                f"{field_name} must not be empty."
            )

        return normalized_value

    @staticmethod
    def _parse_controlled_value(
        enum_type: type[ControlledValue],
        value: object,
        field_name: str,
    ) -> ControlledValue:
        """Parse a canonical enum and convert failures to repository errors."""
        try:
            parse = getattr(enum_type, "parse")
            return parse(value)
        except (TypeError, ValueError, AttributeError) as exc:
            raise RepositoryValidationError(
                f"Invalid {field_name}: {value!r}."
            ) from exc
