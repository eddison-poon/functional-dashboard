"""Dashboard-ready functional test execution summaries.

Purpose
-------
Transforms representative canonical Execution records into quantitative
management-reporting metrics.

The service uses ExecutionSelectionService so repeated execution attempts
and reruns do not inflate current-status totals.

Metric definitions
------------------
Executed:
    Every status except NOT_EXECUTED.

Terminal:
    PASSED, FAILED, BLOCKED, SKIPPED, or ABORTED.

Execution percentage:
    Executed / Total * 100.

Completion percentage:
    Terminal / Total * 100.

Pass rate:
    Passed / Terminal * 100.

Failure rate:
    Failed / Terminal * 100.

Blocked rate:
    Blocked / Terminal * 100.

When a denominator is zero, the percentage is returned as 0.0.
"""

from __future__ import annotations

from dataclasses import dataclass

from canonical.enums import Environment, ExecutionStatus
from canonical.execution import Execution
from repositories.base import RepositoryValidationError

from .execution_selection import ExecutionSelectionService


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    """Immutable dashboard-ready execution summary."""

    environment: Environment | None
    execution_cycle: str | None

    total: int
    executed: int
    terminal: int

    passed: int
    failed: int
    blocked: int
    skipped: int
    aborted: int
    in_progress: int
    not_executed: int

    execution_percentage: float
    completion_percentage: float
    pass_rate: float
    failure_rate: float
    blocked_rate: float

    includes_multiple_environments: bool = False
    includes_multiple_cycles: bool = False

    def __post_init__(self) -> None:
        """Validate internal summary consistency."""
        count_fields = {
            "total": self.total,
            "executed": self.executed,
            "terminal": self.terminal,
            "passed": self.passed,
            "failed": self.failed,
            "blocked": self.blocked,
            "skipped": self.skipped,
            "aborted": self.aborted,
            "in_progress": self.in_progress,
            "not_executed": self.not_executed,
        }

        for field_name, value in count_fields.items():
            if not isinstance(value, int):
                raise RepositoryValidationError(
                    f"{field_name} must be an integer."
                )

            if value < 0:
                raise RepositoryValidationError(
                    f"{field_name} must not be negative."
                )

        status_total = (
            self.passed
            + self.failed
            + self.blocked
            + self.skipped
            + self.aborted
            + self.in_progress
            + self.not_executed
        )

        if status_total != self.total:
            raise RepositoryValidationError(
                "ExecutionSummary status counts must equal total."
            )

        expected_terminal = (
            self.passed
            + self.failed
            + self.blocked
            + self.skipped
            + self.aborted
        )

        if self.terminal != expected_terminal:
            raise RepositoryValidationError(
                "ExecutionSummary terminal count is inconsistent."
            )

        expected_executed = (
            self.terminal
            + self.in_progress
        )

        if self.executed != expected_executed:
            raise RepositoryValidationError(
                "ExecutionSummary executed count is inconsistent."
            )

        percentage_fields = {
            "execution_percentage": self.execution_percentage,
            "completion_percentage": self.completion_percentage,
            "pass_rate": self.pass_rate,
            "failure_rate": self.failure_rate,
            "blocked_rate": self.blocked_rate,
        }

        for field_name, value in percentage_fields.items():
            if not isinstance(value, (int, float)):
                raise RepositoryValidationError(
                    f"{field_name} must be numeric."
                )

            if value < 0.0 or value > 100.0:
                raise RepositoryValidationError(
                    f"{field_name} must be between 0 and 100."
                )

    @property
    def outstanding(self) -> int:
        """Return test cases that are not terminal."""
        return self.in_progress + self.not_executed

    @property
    def unsuccessful_terminal(self) -> int:
        """Return terminal results that are not successful."""
        return (
            self.failed
            + self.blocked
            + self.skipped
            + self.aborted
        )

    @property
    def is_empty(self) -> bool:
        """Return whether the summary contains no test cases."""
        return self.total == 0

    @property
    def is_complete(self) -> bool:
        """Return whether all test cases have terminal results."""
        return (
            self.total > 0
            and self.terminal == self.total
        )

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible execution summary data."""
        return {
            "environment": (
                self.environment.value
                if self.environment is not None
                else None
            ),
            "execution_cycle": self.execution_cycle,
            "total": self.total,
            "executed": self.executed,
            "terminal": self.terminal,
            "passed": self.passed,
            "failed": self.failed,
            "blocked": self.blocked,
            "skipped": self.skipped,
            "aborted": self.aborted,
            "in_progress": self.in_progress,
            "not_executed": self.not_executed,
            "outstanding": self.outstanding,
            "unsuccessful_terminal": (
                self.unsuccessful_terminal
            ),
            "execution_percentage": (
                self.execution_percentage
            ),
            "completion_percentage": (
                self.completion_percentage
            ),
            "pass_rate": self.pass_rate,
            "failure_rate": self.failure_rate,
            "blocked_rate": self.blocked_rate,
            "includes_multiple_environments": (
                self.includes_multiple_environments
            ),
            "includes_multiple_cycles": (
                self.includes_multiple_cycles
            ),
            "is_empty": self.is_empty,
            "is_complete": self.is_complete,
        }


class ExecutionSummaryService:
    """Calculate dashboard metrics from current Execution records."""

    def __init__(
        self,
        execution_selection_service: ExecutionSelectionService,
    ) -> None:
        """Store the Execution selection dependency."""
        if not isinstance(
            execution_selection_service,
            ExecutionSelectionService,
        ):
            raise RepositoryValidationError(
                "execution_selection_service must be an "
                "ExecutionSelectionService."
            )

        self.selection = execution_selection_service

    def summarize(
        self,
        *,
        environment: Environment | str | None = None,
        execution_cycle: str | None = None,
    ) -> ExecutionSummary:
        """Summarize current results for an optional report scope.

        When environment is omitted, all environments are included.

        When execution_cycle is omitted, all execution cycles are
        included. Execution cycles remain separate during representative
        selection, but their selected records are combined into this
        overall summary.
        """
        selected = self.selection.select_current_executions(
            environment=environment,
            execution_cycle=execution_cycle,
        )

        normalized_environment = (
            None
            if environment is None
            else self._resolve_environment(selected, environment)
        )

        normalized_cycle = (
            None
            if execution_cycle is None
            else self._normalize_cycle(execution_cycle)
        )

        return self._build_summary(
            selected,
            environment=normalized_environment,
            execution_cycle=normalized_cycle,
        )

    def summarize_by_environment(
        self,
        *,
        execution_cycle: str | None = None,
    ) -> tuple[ExecutionSummary, ...]:
        """Return one summary for each represented environment."""
        selected = self.selection.select_current_executions(
            execution_cycle=execution_cycle,
        )

        grouped: dict[Environment, list[Execution]] = {}

        for execution in selected:
            grouped.setdefault(
                execution.environment,
                [],
            ).append(execution)

        normalized_cycle = (
            None
            if execution_cycle is None
            else self._normalize_cycle(execution_cycle)
        )

        return tuple(
            self._build_summary(
                tuple(grouped[environment]),
                environment=environment,
                execution_cycle=normalized_cycle,
            )
            for environment in sorted(
                grouped,
                key=lambda value: value.value,
            )
        )

    def summarize_by_cycle(
        self,
        *,
        environment: Environment | str | None = None,
    ) -> tuple[ExecutionSummary, ...]:
        """Return one summary for each represented execution cycle.

        Executions whose execution_cycle is None are included as a
        separate uncategorized cycle summary.
        """
        selected = self.selection.select_current_executions(
            environment=environment,
        )

        grouped: dict[
            str | None,
            list[Execution],
        ] = {}

        for execution in selected:
            grouped.setdefault(
                execution.execution_cycle,
                [],
            ).append(execution)

        normalized_environment = (
            None
            if environment is None
            else self._resolve_environment(selected, environment)
        )

        return tuple(
            self._build_summary(
                tuple(grouped[cycle]),
                environment=normalized_environment,
                execution_cycle=cycle,
            )
            for cycle in sorted(
                grouped,
                key=lambda value: value or "",
            )
        )

    def summarize_environment_cycle_matrix(
        self,
    ) -> tuple[ExecutionSummary, ...]:
        """Return one summary per environment and execution cycle."""
        selected = self.selection.select_current_executions()

        grouped: dict[
            tuple[Environment, str | None],
            list[Execution],
        ] = {}

        for execution in selected:
            key = (
                execution.environment,
                execution.execution_cycle,
            )

            grouped.setdefault(
                key,
                [],
            ).append(execution)

        return tuple(
            self._build_summary(
                tuple(grouped[key]),
                environment=key[0],
                execution_cycle=key[1],
            )
            for key in sorted(
                grouped,
                key=lambda value: (
                    value[0].value,
                    value[1] or "",
                ),
            )
        )

    @classmethod
    def _build_summary(
        cls,
        executions: tuple[Execution, ...],
        *,
        environment: Environment | None,
        execution_cycle: str | None,
    ) -> ExecutionSummary:
        """Build one immutable summary from selected Executions."""
        status_counts = {
            status: 0
            for status in ExecutionStatus
        }

        environments: set[Environment] = set()
        execution_cycles: set[str | None] = set()

        for execution in executions:
            status_counts[execution.status] += 1
            environments.add(execution.environment)
            execution_cycles.add(
                execution.execution_cycle
            )

        passed = status_counts[ExecutionStatus.PASSED]
        failed = status_counts[ExecutionStatus.FAILED]
        blocked = status_counts[ExecutionStatus.BLOCKED]
        skipped = status_counts[ExecutionStatus.SKIPPED]
        aborted = status_counts[ExecutionStatus.ABORTED]
        in_progress = status_counts[
            ExecutionStatus.IN_PROGRESS
        ]
        not_executed = status_counts[
            ExecutionStatus.NOT_EXECUTED
        ]

        terminal = (
            passed
            + failed
            + blocked
            + skipped
            + aborted
        )

        executed = terminal + in_progress
        total = len(executions)

        return ExecutionSummary(
            environment=environment,
            execution_cycle=execution_cycle,
            total=total,
            executed=executed,
            terminal=terminal,
            passed=passed,
            failed=failed,
            blocked=blocked,
            skipped=skipped,
            aborted=aborted,
            in_progress=in_progress,
            not_executed=not_executed,
            execution_percentage=cls._percentage(
                executed,
                total,
            ),
            completion_percentage=cls._percentage(
                terminal,
                total,
            ),
            pass_rate=cls._percentage(
                passed,
                terminal,
            ),
            failure_rate=cls._percentage(
                failed,
                terminal,
            ),
            blocked_rate=cls._percentage(
                blocked,
                terminal,
            ),
            includes_multiple_environments=(
                len(environments) > 1
            ),
            includes_multiple_cycles=(
                len(execution_cycles) > 1
            ),
        )

    @staticmethod
    def _percentage(
        numerator: int,
        denominator: int,
    ) -> float:
        """Return a percentage rounded to two decimal places."""
        if denominator == 0:
            return 0.0

        return round(
            numerator / denominator * 100,
            2,
        )

    @staticmethod
    def _normalize_cycle(
        execution_cycle: object,
    ) -> str:
        """Validate and normalize a requested execution cycle."""
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
    def _resolve_environment(
        executions: tuple[Execution, ...],
        requested_environment: Environment | str,
    ) -> Environment:
        """Return the normalized requested Environment."""
        if executions:
            return executions[0].environment

        try:
            return Environment.parse(requested_environment)
        except (TypeError, ValueError) as exc:
            raise RepositoryValidationError(
                "Invalid environment: "
                f"{requested_environment!r}."
            ) from exc
