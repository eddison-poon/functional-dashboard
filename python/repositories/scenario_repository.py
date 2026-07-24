
"""Repository for canonical Scenario objects.

Purpose
-------
Provides deterministic storage, lookup, filtering, and text-search
operations for canonical Scenario objects.

The repository contains no connector, persistence, metrics, or dashboard
rendering logic. It operates only on validated canonical Scenario
instances held in memory.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

from canonical.enums import Priority, ScenarioType
from canonical.scenario import Scenario

from .base import (
    InMemoryRepository,
    RepositoryValidationError,
)


ControlledValue = TypeVar("ControlledValue")


class ScenarioRepository(
    InMemoryRepository[Scenario]
):
    """In-memory repository for canonical scenarios."""

    def __init__(self) -> None:
        """Create an empty Scenario repository."""
        super().__init__(
            item_type=Scenario,
            id_getter=lambda scenario: scenario.scenario_id,
            entity_name="Scenario",
        )

    def find_by_feature_id(
        self,
        feature_id: str,
    ) -> tuple[Scenario, ...]:
        """Return scenarios belonging to a feature.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_feature_id = self._normalize_query_text(
            feature_id,
            "feature_id",
        )

        return self._matching(
            lambda scenario: (
                scenario.feature_id.casefold()
                == normalized_feature_id
            )
        )

    def find_by_requirement_id(
        self,
        requirement_id: str,
    ) -> tuple[Scenario, ...]:
        """Return scenarios linked to one requirement identifier.

        Identifier matching is exact and case-sensitive after surrounding
        whitespace is removed.
        """
        normalized_requirement_id = self._normalize_identifier(
            requirement_id,
            "requirement_id",
        )

        return self._matching(
            lambda scenario: (
                normalized_requirement_id
                in scenario.requirement_ids
            )
        )

    def find_by_any_requirement_id(
        self,
        requirement_ids: Iterable[str],
    ) -> tuple[Scenario, ...]:
        """Return scenarios linked to any requested requirement ID.

        A scenario is returned when at least one of its requirement IDs
        appears in the supplied collection.
        """
        normalized_requirement_ids = self._normalize_identifier_collection(
            requirement_ids,
            "requirement_ids",
        )

        requested_ids = set(normalized_requirement_ids)

        return self._matching(
            lambda scenario: bool(
                requested_ids.intersection(
                    scenario.requirement_ids
                )
            )
        )

    def find_by_all_requirement_ids(
        self,
        requirement_ids: Iterable[str],
    ) -> tuple[Scenario, ...]:
        """Return scenarios linked to every requested requirement ID."""
        normalized_requirement_ids = self._normalize_identifier_collection(
            requirement_ids,
            "requirement_ids",
        )

        requested_ids = set(normalized_requirement_ids)

        return self._matching(
            lambda scenario: requested_ids.issubset(
                scenario.requirement_ids
            )
        )

    def find_by_type(
        self,
        scenario_type: ScenarioType | str,
    ) -> tuple[Scenario, ...]:
        """Return scenarios with the requested scenario type."""
        parsed_type = self._parse_controlled_value(
            ScenarioType,
            scenario_type,
            "scenario_type",
        )

        return self._matching(
            lambda scenario: (
                scenario.scenario_type is parsed_type
            )
        )

    def find_by_priority(
        self,
        priority: Priority | str,
    ) -> tuple[Scenario, ...]:
        """Return scenarios with the requested priority."""
        parsed_priority = self._parse_controlled_value(
            Priority,
            priority,
            "priority",
        )

        return self._matching(
            lambda scenario: (
                scenario.priority is parsed_priority
            )
        )

    def find_by_owner(
        self,
        owner: str,
    ) -> tuple[Scenario, ...]:
        """Return scenarios assigned to an owner.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_owner = self._normalize_query_text(
            owner,
            "owner",
        )

        return self._matching(
            lambda scenario: (
                scenario.owner is not None
                and scenario.owner.casefold()
                == normalized_owner
            )
        )

    def find_by_tag(
        self,
        tag: str,
    ) -> tuple[Scenario, ...]:
        """Return scenarios containing the requested tag.

        Scenario tags are normalized to lowercase by the canonical model.
        """
        normalized_tag = self._normalize_query_text(
            tag,
            "tag",
        )

        return self._matching(
            lambda scenario: (
                normalized_tag in scenario.tags
            )
        )

    def find_active(
        self,
        active: bool = True,
    ) -> tuple[Scenario, ...]:
        """Return active or inactive scenarios."""
        if type(active) is not bool:
            raise RepositoryValidationError(
                "active must be a Boolean value."
            )

        return self._matching(
            lambda scenario: (
                scenario.active is active
            )
        )

    def search_text(
        self,
        query: str,
    ) -> tuple[Scenario, ...]:
        """Search across commonly used Scenario text fields.

        The search is case-insensitive and performs substring matching
        across:

        - scenario ID
        - feature ID
        - requirement IDs
        - name
        - description
        - tags
        - preconditions
        - expected outcome
        - owner
        """
        normalized_query = self._normalize_query_text(
            query,
            "query",
        )

        def matches(scenario: Scenario) -> bool:
            searchable_values = (
                scenario.scenario_id,
                scenario.feature_id,
                scenario.name,
                scenario.description,
                scenario.expected_outcome,
                scenario.owner,
                *scenario.requirement_ids,
                *scenario.tags,
                *scenario.preconditions,
            )

            return any(
                value is not None
                and normalized_query in value.casefold()
                for value in searchable_values
            )

        return self._matching(matches)

    def _matching(
        self,
        predicate: Callable[[Scenario], bool],
    ) -> tuple[Scenario, ...]:
        """Return sorted scenarios satisfying a predicate.

        The inherited list_all() method already returns records sorted by
        scenario_id, so filtered results remain deterministic.
        """
        return tuple(
            scenario
            for scenario in self.list_all()
            if predicate(scenario)
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
        """Validate and trim a case-sensitive identifier."""
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

    @classmethod
    def _normalize_identifier_collection(
        cls,
        values: object,
        field_name: str,
    ) -> tuple[str, ...]:
        """Validate and normalize a collection of identifiers.

        Values are trimmed and deduplicated while preserving first-seen
        order. An empty collection is rejected because an any/all lookup
        without identifiers is ambiguous.
        """
        if isinstance(values, (str, bytes)):
            raise RepositoryValidationError(
                f"{field_name} must be a collection of strings, "
                "not a single string."
            )

        try:
            raw_values = list(values)
        except TypeError as exc:
            raise RepositoryValidationError(
                f"{field_name} must be a collection of strings."
            ) from exc

        normalized_values: list[str] = []
        seen_values: set[str] = set()

        for index, raw_value in enumerate(raw_values):
            try:
                normalized_value = cls._normalize_identifier(
                    raw_value,
                    f"{field_name}[{index}]",
                )
            except RepositoryValidationError:
                raise

            if normalized_value not in seen_values:
                seen_values.add(normalized_value)
                normalized_values.append(normalized_value)

        if not normalized_values:
            raise RepositoryValidationError(
                f"{field_name} must contain at least one identifier."
            )

        return tuple(normalized_values)

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
