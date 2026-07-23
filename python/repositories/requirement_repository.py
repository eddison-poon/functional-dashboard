
"""Repository for canonical Requirement objects.

Purpose
-------
Provides deterministic storage, lookup, filtering, and text-search
operations for canonical Requirement objects.

The repository contains no connector, persistence, metrics, or dashboard
rendering logic. It operates only on validated canonical Requirement
instances held in memory.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from canonical.enums import (
    Priority,
    RequirementStatus,
    RequirementType,
    SourceSystem,
)
from canonical.requirement import Requirement

from .base import (
    InMemoryRepository,
    RepositoryValidationError,
)


ControlledValue = TypeVar("ControlledValue")


class RequirementRepository(
    InMemoryRepository[Requirement]
):
    """In-memory repository for canonical requirements."""

    def __init__(self) -> None:
        """Create an empty Requirement repository."""
        super().__init__(
            item_type=Requirement,
            id_getter=lambda requirement: (
                requirement.requirement_id
            ),
            entity_name="Requirement",
        )

    def find_by_status(
        self,
        status: RequirementStatus | str,
    ) -> tuple[Requirement, ...]:
        """Return requirements with the requested lifecycle status."""
        parsed_status = self._parse_controlled_value(
            RequirementStatus,
            status,
            "status",
        )

        return self._matching(
            lambda requirement: (
                requirement.status is parsed_status
            )
        )

    def find_by_priority(
        self,
        priority: Priority | str,
    ) -> tuple[Requirement, ...]:
        """Return requirements with the requested priority."""
        parsed_priority = self._parse_controlled_value(
            Priority,
            priority,
            "priority",
        )

        return self._matching(
            lambda requirement: (
                requirement.priority is parsed_priority
            )
        )

    def find_by_type(
        self,
        requirement_type: RequirementType | str,
    ) -> tuple[Requirement, ...]:
        """Return requirements with the requested requirement type."""
        parsed_type = self._parse_controlled_value(
            RequirementType,
            requirement_type,
            "requirement_type",
        )

        return self._matching(
            lambda requirement: (
                requirement.requirement_type is parsed_type
            )
        )

    def find_by_source_system(
        self,
        source_system: SourceSystem | str,
    ) -> tuple[Requirement, ...]:
        """Return requirements originating from a source system."""
        parsed_source = self._parse_controlled_value(
            SourceSystem,
            source_system,
            "source_system",
        )

        return self._matching(
            lambda requirement: (
                requirement.source_system is parsed_source
            )
        )

    def find_by_source_project(
        self,
        source_project: str,
    ) -> tuple[Requirement, ...]:
        """Return requirements belonging to a source project.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_project = self._normalize_query_text(
            source_project,
            "source_project",
        )

        return self._matching(
            lambda requirement: (
                requirement.source_project is not None
                and requirement.source_project.casefold()
                == normalized_project
            )
        )

    def find_by_component(
        self,
        component: str,
    ) -> tuple[Requirement, ...]:
        """Return requirements belonging to a component.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_component = self._normalize_query_text(
            component,
            "component",
        )

        return self._matching(
            lambda requirement: (
                requirement.component is not None
                and requirement.component.casefold()
                == normalized_component
            )
        )

    def find_by_owner(
        self,
        owner: str,
    ) -> tuple[Requirement, ...]:
        """Return requirements assigned to an owner.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_owner = self._normalize_query_text(
            owner,
            "owner",
        )

        return self._matching(
            lambda requirement: (
                requirement.owner is not None
                and requirement.owner.casefold()
                == normalized_owner
            )
        )

    def find_by_label(
        self,
        label: str,
    ) -> tuple[Requirement, ...]:
        """Return requirements containing a label.

        Canonical Requirement labels are already normalized to lowercase,
        so this lookup is also normalized to lowercase.
        """
        normalized_label = self._normalize_query_text(
            label,
            "label",
        )

        return self._matching(
            lambda requirement: (
                normalized_label in requirement.labels
            )
        )

    def find_by_release(
        self,
        release: str,
    ) -> tuple[Requirement, ...]:
        """Return requirements assigned to a release."""
        normalized_release = self._normalize_query_text(
            release,
            "release",
        )

        return self._matching(
            lambda requirement: (
                requirement.release is not None
                and requirement.release.casefold()
                == normalized_release
            )
        )

    def find_by_sprint(
        self,
        sprint: str,
    ) -> tuple[Requirement, ...]:
        """Return requirements assigned to a sprint."""
        normalized_sprint = self._normalize_query_text(
            sprint,
            "sprint",
        )

        return self._matching(
            lambda requirement: (
                requirement.sprint is not None
                and requirement.sprint.casefold()
                == normalized_sprint
            )
        )

    def find_active(
        self,
        active: bool = True,
    ) -> tuple[Requirement, ...]:
        """Return active or inactive requirements."""
        if type(active) is not bool:
            raise RepositoryValidationError(
                "active must be a Boolean value."
            )

        return self._matching(
            lambda requirement: (
                requirement.active is active
            )
        )

    def search_text(
        self,
        query: str,
    ) -> tuple[Requirement, ...]:
        """Search across commonly used Requirement text fields.

        The search is case-insensitive and performs substring matching
        across:

        - requirement ID
        - title
        - description
        - source project
        - component
        - labels
        - release
        - sprint
        - owner
        """
        normalized_query = self._normalize_query_text(
            query,
            "query",
        )

        def matches(requirement: Requirement) -> bool:
            searchable_values = (
                requirement.requirement_id,
                requirement.title,
                requirement.description,
                requirement.source_project,
                requirement.component,
                requirement.release,
                requirement.sprint,
                requirement.owner,
                *requirement.labels,
            )

            return any(
                value is not None
                and normalized_query in value.casefold()
                for value in searchable_values
            )

        return self._matching(matches)

    def _matching(
        self,
        predicate: Callable[[Requirement], bool],
    ) -> tuple[Requirement, ...]:
        """Return sorted requirements satisfying a predicate."""
        return tuple(
            requirement
            for requirement in self.list_all()
            if predicate(requirement)
        )

    @staticmethod
    def _normalize_query_text(
        value: object,
        field_name: str,
    ) -> str:
        """Validate and normalize text used by repository queries."""
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
