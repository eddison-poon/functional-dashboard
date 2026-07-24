"""Repository for canonical Execution objects.

Purpose
-------
Provides deterministic storage, lookup, filtering, and text-search
operations for canonical test executions.

The repository contains no connector, persistence, metrics,
aggregation, or dashboard-rendering logic. It operates only on
validated canonical Execution instances held in memory.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import TypeVar

from canonical.enums import (
    Environment,
    ExecutionStatus,
    SourceSystem,
)
from canonical.execution import Execution

from .base import (
    InMemoryRepository,
    RepositoryValidationError,
)


ControlledValue = TypeVar("ControlledValue")


class ExecutionRepository(
    InMemoryRepository[Execution]
):
    """In-memory repository for canonical Executions."""

    def __init__(self) -> None:
        """Create an empty Execution repository."""
        super().__init__(
            item_type=Execution,
            id_getter=lambda item: item.execution_id,
            entity_name="Execution",
        )

    def find_by_test_definition_id(
        self,
        test_definition_id: str,
    ) -> tuple[Execution, ...]:
        """Return Executions linked to one Test Definition.

        Test Definition identifiers are matched exactly and
        case-sensitively after surrounding whitespace is removed.
        """
        normalized_id = self._normalize_identifier(
            test_definition_id,
            "test_definition_id",
        )

        return self._matching(
            lambda item: (
                item.test_definition_id == normalized_id
            )
        )

    def find_by_environment(
        self,
        environment: Environment | str,
    ) -> tuple[Execution, ...]:
        """Return Executions for the requested environment."""
        parsed_environment = self._parse_controlled_value(
            Environment,
            environment,
            "environment",
        )

        return self._matching(
            lambda item: (
                item.environment is parsed_environment
            )
        )

    def find_by_status(
        self,
        status: ExecutionStatus | str,
    ) -> tuple[Execution, ...]:
        """Return Executions with the requested status."""
        parsed_status = self._parse_controlled_value(
            ExecutionStatus,
            status,
            "status",
        )

        return self._matching(
            lambda item: item.status is parsed_status
        )

    def find_by_source_system(
        self,
        source_system: SourceSystem | str,
    ) -> tuple[Execution, ...]:
        """Return Executions originating from a source system."""
        parsed_source_system = self._parse_controlled_value(
            SourceSystem,
            source_system,
            "source_system",
        )

        return self._matching(
            lambda item: (
                item.source_system is parsed_source_system
            )
        )

    def find_by_execution_cycle(
        self,
        execution_cycle: str,
    ) -> tuple[Execution, ...]:
        """Return Executions belonging to an execution cycle.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_cycle = self._normalize_query_text(
            execution_cycle,
            "execution_cycle",
        )

        return self._matching(
            lambda item: (
                item.execution_cycle is not None
                and item.execution_cycle.casefold()
                == normalized_cycle
            )
        )

    def find_by_executed_by(
        self,
        executed_by: str,
    ) -> tuple[Execution, ...]:
        """Return Executions performed by a person or service account.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_executor = self._normalize_query_text(
            executed_by,
            "executed_by",
        )

        return self._matching(
            lambda item: (
                item.executed_by is not None
                and item.executed_by.casefold()
                == normalized_executor
            )
        )

    def find_by_build_version(
        self,
        build_version: str,
    ) -> tuple[Execution, ...]:
        """Return Executions associated with one build version.

        Matching is case-insensitive after surrounding whitespace is
        removed.
        """
        normalized_build = self._normalize_query_text(
            build_version,
            "build_version",
        )

        return self._matching(
            lambda item: (
                item.build_version is not None
                and item.build_version.casefold()
                == normalized_build
            )
        )

    def find_by_external_reference(
        self,
        external_reference: str,
    ) -> tuple[Execution, ...]:
        """Return Executions linked to an external reference.

        Examples include Jira execution keys, CI/CD run identifiers,
        or test-management execution identifiers.
        """
        normalized_reference = self._normalize_identifier(
            external_reference,
            "external_reference",
        )

        return self._matching(
            lambda item: (
                item.external_reference
                == normalized_reference
            )
        )

    def find_by_defect_id(
        self,
        defect_id: str,
    ) -> tuple[Execution, ...]:
        """Return Executions linked to one defect identifier."""
        normalized_defect_id = self._normalize_identifier(
            defect_id,
            "defect_id",
        )

        return self._matching(
            lambda item: (
                normalized_defect_id in item.defect_ids
            )
        )

    def find_by_evidence_id(
        self,
        evidence_id: str,
    ) -> tuple[Execution, ...]:
        """Return Executions linked to one evidence identifier."""
        normalized_evidence_id = self._normalize_identifier(
            evidence_id,
            "evidence_id",
        )

        return self._matching(
            lambda item: (
                normalized_evidence_id in item.evidence_ids
            )
        )

    def find_with_defects(
        self,
    ) -> tuple[Execution, ...]:
        """Return Executions linked to one or more defects."""
        return self._matching(
            lambda item: bool(item.defect_ids)
        )

    def find_with_evidence(
        self,
    ) -> tuple[Execution, ...]:
        """Return Executions linked to one or more evidence items."""
        return self._matching(
            lambda item: bool(item.evidence_ids)
        )

    def find_without_evidence(
        self,
    ) -> tuple[Execution, ...]:
        """Return Executions without linked evidence."""
        return self._matching(
            lambda item: not item.evidence_ids
        )

    def find_reruns(
        self,
    ) -> tuple[Execution, ...]:
        """Return Executions that are reruns of earlier executions."""
        return self._matching(
            lambda item: (
                item.rerun_of_execution_id is not None
            )
        )

    def find_reruns_of(
        self,
        execution_id: str,
    ) -> tuple[Execution, ...]:
        """Return Executions that rerun a specific execution."""
        normalized_execution_id = self._normalize_identifier(
            execution_id,
            "execution_id",
        )

        return self._matching(
            lambda item: (
                item.rerun_of_execution_id
                == normalized_execution_id
            )
        )

    def find_not_executed(
        self,
    ) -> tuple[Execution, ...]:
        """Return planned Executions that have not started."""
        return self.find_by_status(
            ExecutionStatus.NOT_EXECUTED
        )

    def find_executed(
        self,
    ) -> tuple[Execution, ...]:
        """Return Executions where activity has started."""
        return self._matching(
            lambda item: item.is_executed
        )

    def find_terminal(
        self,
    ) -> tuple[Execution, ...]:
        """Return Executions that have reached a final status."""
        return self._matching(
            lambda item: item.is_terminal
        )

    def find_successful(
        self,
    ) -> tuple[Execution, ...]:
        """Return successfully passed Executions."""
        return self._matching(
            lambda item: item.is_successful
        )

    def find_started_between(
        self,
        started_from: datetime,
        started_to: datetime,
    ) -> tuple[Execution, ...]:
        """Return Executions started within an inclusive time range."""
        normalized_from, normalized_to = (
            self._normalize_datetime_range(
                started_from,
                started_to,
                "started_from",
                "started_to",
            )
        )

        return self._matching(
            lambda item: (
                item.started_at is not None
                and normalized_from
                <= item.started_at
                <= normalized_to
            )
        )

    def find_completed_between(
        self,
        completed_from: datetime,
        completed_to: datetime,
    ) -> tuple[Execution, ...]:
        """Return Executions completed within an inclusive time range."""
        normalized_from, normalized_to = (
            self._normalize_datetime_range(
                completed_from,
                completed_to,
                "completed_from",
                "completed_to",
            )
        )

        return self._matching(
            lambda item: (
                item.completed_at is not None
                and normalized_from
                <= item.completed_at
                <= normalized_to
            )
        )

    def search_text(
        self,
        query: str,
    ) -> tuple[Execution, ...]:
        """Search across commonly used Execution text fields.

        The search is case-insensitive and performs substring matching
        across:

        - execution ID
        - Test Definition ID
        - execution cycle
        - executor
        - build version
        - external reference
        - defect IDs
        - evidence IDs
        - remarks
        - rerun execution ID
        """
        normalized_query = self._normalize_query_text(
            query,
            "query",
        )

        def matches(item: Execution) -> bool:
            searchable_values: list[str | None] = [
                item.execution_id,
                item.test_definition_id,
                item.execution_cycle,
                item.executed_by,
                item.build_version,
                item.external_reference,
                item.remarks,
                item.rerun_of_execution_id,
                *item.defect_ids,
                *item.evidence_ids,
            ]

            return any(
                value is not None
                and normalized_query in value.casefold()
                for value in searchable_values
            )

        return self._matching(matches)

    def _matching(
        self,
        predicate: Callable[[Execution], bool],
    ) -> tuple[Execution, ...]:
        """Return sorted Executions satisfying a predicate.

        The inherited list_all() method returns records sorted by
        execution_id, so filtered results remain deterministic.
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

    @staticmethod
    def _normalize_datetime(
        value: object,
        field_name: str,
    ) -> datetime:
        """Validate a timezone-aware datetime query value."""
        if not isinstance(value, datetime):
            raise RepositoryValidationError(
                f"{field_name} must be a datetime."
            )

        if value.tzinfo is None or value.utcoffset() is None:
            raise RepositoryValidationError(
                f"{field_name} must be timezone-aware."
            )

        return value

    @classmethod
    def _normalize_datetime_range(
        cls,
        range_from: object,
        range_to: object,
        from_field_name: str,
        to_field_name: str,
    ) -> tuple[datetime, datetime]:
        """Validate an inclusive timezone-aware datetime range."""
        normalized_from = cls._normalize_datetime(
            range_from,
            from_field_name,
        )
        normalized_to = cls._normalize_datetime(
            range_to,
            to_field_name,
        )

        if normalized_to < normalized_from:
            raise RepositoryValidationError(
                f"{to_field_name} must not be earlier than "
                f"{from_field_name}."
            )

        return normalized_from, normalized_to

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
