
"""Execution selection policies for dashboard reporting.

Purpose
-------
Selects one representative Execution for each reporting context while
preserving access to the complete execution history.

Dashboard current-status reporting must avoid counting repeated
execution attempts as separate test cases. Executions are therefore
grouped by Test Definition, environment, and execution cycle.

The representative Execution is selected using the following order:

1. Latest completed_at timestamp.
2. Latest started_at timestamp when no completed timestamp exists.
3. Lexicographically greatest execution_id as a deterministic fallback.

The execution_id fallback guarantees deterministic output but does not
claim chronological ordering.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from canonical.enums import Environment
from canonical.execution import Execution
from repositories.base import RepositoryValidationError
from repositories.execution_repository import ExecutionRepository


@dataclass(frozen=True, slots=True, order=True)
class ExecutionGroupKey:
    """Grouping identity used for current execution reporting."""

    test_definition_id: str
    environment: Environment
    execution_cycle: str | None

    def to_dict(self) -> dict[str, str | None]:
        """Return JSON-compatible grouping key data."""
        return {
            "test_definition_id": self.test_definition_id,
            "environment": self.environment.value,
            "execution_cycle": self.execution_cycle,
        }


class ExecutionSelectionService:
    """Select representative Executions for reporting."""

    def __init__(
        self,
        execution_repository: ExecutionRepository,
    ) -> None:
        """Store the canonical Execution repository."""
        if not isinstance(
            execution_repository,
            ExecutionRepository,
        ):
            raise RepositoryValidationError(
                "execution_repository must be an "
                "ExecutionRepository."
            )

        self.executions = execution_repository

    def select_current_executions(
        self,
        *,
        environment: Environment | str | None = None,
        execution_cycle: str | None = None,
    ) -> tuple[Execution, ...]:
        """Return one representative Execution per reporting group.

        Executions are grouped by:

        - test_definition_id
        - environment
        - execution_cycle

        Optional environment and execution-cycle filters are applied
        before representative records are selected.

        Passing execution_cycle=None means that all cycles are included.
        Use select_current_by_cycle() when a specific cycle is required.
        """
        candidates = self._filtered_executions(
            environment=environment,
            execution_cycle=execution_cycle,
            filter_cycle=execution_cycle is not None,
        )

        grouped_history = self._group_records(candidates)

        selected = tuple(
            self._select_representative(history)
            for _, history in sorted(
                grouped_history.items(),
                key=lambda item: self._group_sort_key(
                    item[0]
                ),
            )
        )

        return tuple(
            sorted(
                selected,
                key=self._execution_output_sort_key,
            )
        )

    def select_current_by_environment(
        self,
        environment: Environment | str,
    ) -> tuple[Execution, ...]:
        """Return current Executions for one environment."""
        return self.select_current_executions(
            environment=environment,
        )

    def select_current_by_cycle(
        self,
        execution_cycle: str,
        *,
        environment: Environment | str | None = None,
    ) -> tuple[Execution, ...]:
        """Return current Executions for one execution cycle."""
        normalized_cycle = self._normalize_cycle(
            execution_cycle
        )

        candidates = self._filtered_executions(
            environment=environment,
            execution_cycle=normalized_cycle,
            filter_cycle=True,
        )

        grouped_history = self._group_records(candidates)

        selected = tuple(
            self._select_representative(history)
            for _, history in sorted(
                grouped_history.items(),
                key=lambda item: self._group_sort_key(
                    item[0]
                ),
            )
        )

        return tuple(
            sorted(
                selected,
                key=self._execution_output_sort_key,
            )
        )

    def group_execution_history(
        self,
        *,
        environment: Environment | str | None = None,
        execution_cycle: str | None = None,
    ) -> dict[ExecutionGroupKey, tuple[Execution, ...]]:
        """Return complete execution history grouped by report context.

        History records within each group are ordered from oldest to
        newest using the same timestamp policy as current selection.

        Passing execution_cycle=None includes all cycles.
        """
        candidates = self._filtered_executions(
            environment=environment,
            execution_cycle=execution_cycle,
            filter_cycle=execution_cycle is not None,
        )

        grouped = self._group_records(candidates)

        return {
            key: tuple(
                sorted(
                    history,
                    key=self._history_sort_key,
                )
            )
            for key, history in sorted(
                grouped.items(),
                key=lambda item: self._group_sort_key(
                    item[0]
                ),
            )
        }

    def group_execution_history_by_test_definition(
        self,
        test_definition_id: str,
        *,
        environment: Environment | str | None = None,
        execution_cycle: str | None = None,
    ) -> dict[ExecutionGroupKey, tuple[Execution, ...]]:
        """Return grouped history for one Test Definition."""
        normalized_id = self._normalize_identifier(
            test_definition_id,
            "test_definition_id",
        )

        grouped = self.group_execution_history(
            environment=environment,
            execution_cycle=execution_cycle,
        )

        return {
            key: history
            for key, history in grouped.items()
            if key.test_definition_id == normalized_id
        }

    def _filtered_executions(
        self,
        *,
        environment: Environment | str | None,
        execution_cycle: str | None,
        filter_cycle: bool,
    ) -> tuple[Execution, ...]:
        """Return Executions matching optional report filters."""
        records = self.executions.list_all()

        parsed_environment: Environment | None = None

        if environment is not None:
            parsed_environment = self._parse_environment(
                environment
            )

        normalized_cycle: str | None = None

        if filter_cycle:
            normalized_cycle = self._normalize_cycle(
                execution_cycle
            )

        return tuple(
            execution
            for execution in records
            if (
                parsed_environment is None
                or execution.environment
                is parsed_environment
            )
            and (
                not filter_cycle
                or self._cycles_equal(
                    execution.execution_cycle,
                    normalized_cycle,
                )
            )
        )

    @staticmethod
    def _group_records(
        executions: tuple[Execution, ...],
    ) -> dict[ExecutionGroupKey, tuple[Execution, ...]]:
        """Group Executions by canonical reporting identity."""
        grouped_lists: dict[
            ExecutionGroupKey,
            list[Execution],
        ] = {}

        for execution in executions:
            key = ExecutionGroupKey(
                test_definition_id=(
                    execution.test_definition_id
                ),
                environment=execution.environment,
                execution_cycle=(
                    execution.execution_cycle
                ),
            )

            grouped_lists.setdefault(
                key,
                [],
            ).append(execution)

        return {
            key: tuple(history)
            for key, history in grouped_lists.items()
        }

    @classmethod
    def _select_representative(
        cls,
        executions: tuple[Execution, ...],
    ) -> Execution:
        """Select the current representative of one history group."""
        if not executions:
            raise RepositoryValidationError(
                "Cannot select a representative Execution "
                "from an empty group."
            )

        return max(
            executions,
            key=cls._representative_sort_key,
        )

    @classmethod
    def _representative_sort_key(
        cls,
        execution: Execution,
    ) -> tuple[
        int,
        datetime,
        int,
        datetime,
        str,
    ]:
        """Return precedence key for representative selection.

        Completed records take precedence over records that have only
        started. Planned records without timestamps use execution_id as
        the deterministic fallback.
        """
        completed_marker = (
            1
            if execution.completed_at is not None
            else 0
        )
        completed_value = (
            execution.completed_at
            if execution.completed_at is not None
            else cls._minimum_datetime()
        )

        started_marker = (
            1
            if execution.started_at is not None
            else 0
        )
        started_value = (
            execution.started_at
            if execution.started_at is not None
            else cls._minimum_datetime()
        )

        return (
            completed_marker,
            completed_value,
            started_marker,
            started_value,
            execution.execution_id,
        )

    @classmethod
    def _history_sort_key(
        cls,
        execution: Execution,
    ) -> tuple[
        datetime,
        datetime,
        str,
    ]:
        """Return deterministic oldest-to-newest history order."""
        primary_timestamp = (
            execution.completed_at
            or execution.started_at
            or cls._minimum_datetime()
        )

        secondary_timestamp = (
            execution.started_at
            or cls._minimum_datetime()
        )

        return (
            primary_timestamp,
            secondary_timestamp,
            execution.execution_id,
        )

    @staticmethod
    def _execution_output_sort_key(
        execution: Execution,
    ) -> tuple[str, str, str, str]:
        """Return deterministic ordering for selected output."""
        return (
            execution.environment.value,
            execution.execution_cycle or "",
            execution.test_definition_id,
            execution.execution_id,
        )

    @staticmethod
    def _group_sort_key(
        key: ExecutionGroupKey,
    ) -> tuple[str, str, str]:
        """Return deterministic group-key ordering."""
        return (
            key.environment.value,
            key.execution_cycle or "",
            key.test_definition_id,
        )

    @staticmethod
    def _cycles_equal(
        actual_cycle: str | None,
        requested_cycle: str | None,
    ) -> bool:
        """Return whether two optional cycles match."""
        if actual_cycle is None or requested_cycle is None:
            return actual_cycle is requested_cycle

        return (
            actual_cycle.casefold()
            == requested_cycle.casefold()
        )

    @staticmethod
    def _normalize_cycle(
        execution_cycle: object,
    ) -> str:
        """Validate and normalize a required execution cycle."""
        if not isinstance(execution_cycle, str):
            raise RepositoryValidationError(
                "execution_cycle must be a string."
            )

        normalized = execution_cycle.strip()

        if not normalized:
            raise RepositoryValidationError(
                "execution_cycle must not be empty."
            )

        return normalized

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

        normalized = value.strip()

        if not normalized:
            raise RepositoryValidationError(
                f"{field_name} must not be empty."
            )

        return normalized

    @staticmethod
    def _parse_environment(
        environment: Environment | str,
    ) -> Environment:
        """Parse a canonical environment query value."""
        try:
            return Environment.parse(environment)
        except (TypeError, ValueError) as exc:
            raise RepositoryValidationError(
                f"Invalid environment: {environment!r}."
            ) from exc

    @staticmethod
    def _minimum_datetime() -> datetime:
        """Return a timezone-aware minimum comparison value."""
        return datetime.min.replace(tzinfo=timezone.utc)
