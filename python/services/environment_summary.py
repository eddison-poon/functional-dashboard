
"""Environment readiness reporting services.

Purpose
-------
Transforms representative Execution records and execution summaries into
management-friendly environment readiness assessments.

Readiness policy
----------------
READY:
    The environment contains current execution data, all current tests
    are terminal, and there are no FAILED, BLOCKED, or ABORTED results.

PARTIALLY_READY:
    The environment contains execution data but testing is incomplete,
    or one or more FAILED, BLOCKED, or ABORTED results exist.

NOT_READY:
    No current Execution records exist for the requested environment and
    execution-cycle scope.

SKIPPED results do not automatically prevent READY because their release
impact depends on project-specific acceptance rules. They remain visible
in the underlying execution summary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from canonical.enums import Environment
from canonical.execution import Execution
from repositories.base import RepositoryValidationError

from .execution_selection import ExecutionSelectionService
from .execution_summary import (
    ExecutionSummary,
    ExecutionSummaryService,
)


class EnvironmentReadinessStatus(StrEnum):
    """Management-facing environment readiness states."""

    READY = "READY"
    PARTIALLY_READY = "PARTIALLY_READY"
    NOT_READY = "NOT_READY"


class ReadinessColour(StrEnum):
    """Dashboard colour associated with readiness."""

    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"


@dataclass(frozen=True, slots=True)
class EnvironmentReadinessSummary:
    """Immutable readiness assessment for one environment."""

    environment: Environment
    readiness: EnvironmentReadinessStatus
    colour: ReadinessColour

    execution_cycle: str | None
    build_versions: tuple[str, ...]

    execution_summary: ExecutionSummary

    rationale: tuple[str, ...]
    recommended_actions: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate readiness-summary consistency."""
        if not isinstance(self.environment, Environment):
            raise RepositoryValidationError(
                "environment must be an Environment."
            )

        if not isinstance(
            self.readiness,
            EnvironmentReadinessStatus,
        ):
            raise RepositoryValidationError(
                "readiness must be an "
                "EnvironmentReadinessStatus."
            )

        if not isinstance(self.colour, ReadinessColour):
            raise RepositoryValidationError(
                "colour must be a ReadinessColour."
            )

        expected_colour = {
            EnvironmentReadinessStatus.READY: (
                ReadinessColour.GREEN
            ),
            EnvironmentReadinessStatus.PARTIALLY_READY: (
                ReadinessColour.AMBER
            ),
            EnvironmentReadinessStatus.NOT_READY: (
                ReadinessColour.RED
            ),
        }[self.readiness]

        if self.colour is not expected_colour:
            raise RepositoryValidationError(
                "colour is inconsistent with readiness."
            )

        if not isinstance(
            self.execution_summary,
            ExecutionSummary,
        ):
            raise RepositoryValidationError(
                "execution_summary must be an "
                "ExecutionSummary."
            )

        if (
            self.execution_summary.environment
            is not None
            and self.execution_summary.environment
            is not self.environment
        ):
            raise RepositoryValidationError(
                "execution_summary environment is inconsistent."
            )

        self._validate_string_tuple(
            self.build_versions,
            "build_versions",
        )
        self._validate_string_tuple(
            self.rationale,
            "rationale",
        )
        self._validate_string_tuple(
            self.recommended_actions,
            "recommended_actions",
        )

        if tuple(sorted(self.build_versions)) != (
            self.build_versions
        ):
            raise RepositoryValidationError(
                "build_versions must be sorted."
            )

        if not self.rationale:
            raise RepositoryValidationError(
                "rationale must contain at least one item."
            )

    @property
    def is_ready(self) -> bool:
        """Return whether the environment is fully ready."""
        return (
            self.readiness
            is EnvironmentReadinessStatus.READY
        )

    @property
    def has_execution_data(self) -> bool:
        """Return whether current execution data exists."""
        return self.execution_summary.total > 0

    @property
    def primary_build_version(self) -> str | None:
        """Return a build when exactly one build is represented."""
        if len(self.build_versions) == 1:
            return self.build_versions[0]

        return None

    @property
    def has_mixed_build_versions(self) -> bool:
        """Return whether results span multiple builds."""
        return len(self.build_versions) > 1

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible readiness data."""
        return {
            "environment": self.environment.value,
            "readiness": self.readiness.value,
            "colour": self.colour.value,
            "execution_cycle": self.execution_cycle,
            "build_versions": list(self.build_versions),
            "primary_build_version": (
                self.primary_build_version
            ),
            "has_mixed_build_versions": (
                self.has_mixed_build_versions
            ),
            "is_ready": self.is_ready,
            "has_execution_data": (
                self.has_execution_data
            ),
            "rationale": list(self.rationale),
            "recommended_actions": list(
                self.recommended_actions
            ),
            "execution_summary": (
                self.execution_summary.to_dict()
            ),
        }

    @staticmethod
    def _validate_string_tuple(
        values: object,
        field_name: str,
    ) -> None:
        """Validate a tuple containing non-empty strings."""
        if not isinstance(values, tuple):
            raise RepositoryValidationError(
                f"{field_name} must be a tuple."
            )

        if any(
            not isinstance(value, str)
            or not value.strip()
            for value in values
        ):
            raise RepositoryValidationError(
                f"{field_name} must contain "
                "non-empty strings."
            )


class EnvironmentReadinessService:
    """Calculate readiness for functional-test environments."""

    def __init__(
        self,
        execution_selection_service: ExecutionSelectionService,
        execution_summary_service: ExecutionSummaryService,
    ) -> None:
        """Store execution reporting dependencies."""
        if not isinstance(
            execution_selection_service,
            ExecutionSelectionService,
        ):
            raise RepositoryValidationError(
                "execution_selection_service must be an "
                "ExecutionSelectionService."
            )

        if not isinstance(
            execution_summary_service,
            ExecutionSummaryService,
        ):
            raise RepositoryValidationError(
                "execution_summary_service must be an "
                "ExecutionSummaryService."
            )

        self.selection = execution_selection_service
        self.execution_summaries = execution_summary_service

    def summarize(
        self,
        environment: Environment | str,
        *,
        execution_cycle: str | None = None,
    ) -> EnvironmentReadinessSummary:
        """Return readiness for one environment."""
        normalized_environment = (
            self._normalize_environment(environment)
        )

        normalized_cycle = (
            None
            if execution_cycle is None
            else self._normalize_cycle(execution_cycle)
        )

        selected = self.selection.select_current_executions(
            environment=normalized_environment,
            execution_cycle=normalized_cycle,
        )

        execution_summary = (
            self.execution_summaries.summarize(
                environment=normalized_environment,
                execution_cycle=normalized_cycle,
            )
        )

        readiness = self._assess_readiness(
            execution_summary
        )

        return EnvironmentReadinessSummary(
            environment=normalized_environment,
            readiness=readiness,
            colour=self._colour_for(readiness),
            execution_cycle=normalized_cycle,
            build_versions=self._build_versions(selected),
            execution_summary=execution_summary,
            rationale=self._build_rationale(
                execution_summary,
                selected,
                readiness,
            ),
            recommended_actions=(
                self._build_recommended_actions(
                    execution_summary,
                    selected,
                    readiness,
                )
            ),
        )

    def summarize_all(
        self,
        *,
        execution_cycle: str | None = None,
        environments: (
            Iterable[Environment | str] | None
        ) = None,
    ) -> tuple[EnvironmentReadinessSummary, ...]:
        """Return readiness summaries for multiple environments.

        When environments is omitted, only environments represented by
        current execution data are returned.

        When environments is supplied, every requested environment is
        included, even when no execution data exists. This supports
        management dashboards that must always show DEV, SIT, UAT, and
        other expected environments.
        """
        normalized_cycle = (
            None
            if execution_cycle is None
            else self._normalize_cycle(execution_cycle)
        )

        if environments is None:
            selected = (
                self.selection.select_current_executions(
                    execution_cycle=normalized_cycle
                )
            )

            normalized_environments = tuple(
                sorted(
                    {
                        execution.environment
                        for execution in selected
                    },
                    key=lambda value: value.value,
                )
            )
        else:
            normalized_environments = (
                self._normalize_environments(
                    environments
                )
            )

        return tuple(
            self.summarize(
                environment,
                execution_cycle=normalized_cycle,
            )
            for environment in normalized_environments
        )

    @staticmethod
    def _assess_readiness(
        summary: ExecutionSummary,
    ) -> EnvironmentReadinessStatus:
        """Apply the deterministic readiness policy."""
        if summary.total == 0:
            return EnvironmentReadinessStatus.NOT_READY

        has_execution_exception = (
            summary.failed > 0
            or summary.blocked > 0
            or summary.aborted > 0
        )

        if (
            summary.is_complete
            and not has_execution_exception
        ):
            return EnvironmentReadinessStatus.READY

        return (
            EnvironmentReadinessStatus.PARTIALLY_READY
        )

    @staticmethod
    def _colour_for(
        readiness: EnvironmentReadinessStatus,
    ) -> ReadinessColour:
        """Return the dashboard colour for readiness."""
        return {
            EnvironmentReadinessStatus.READY: (
                ReadinessColour.GREEN
            ),
            EnvironmentReadinessStatus.PARTIALLY_READY: (
                ReadinessColour.AMBER
            ),
            EnvironmentReadinessStatus.NOT_READY: (
                ReadinessColour.RED
            ),
        }[readiness]

    @classmethod
    def _build_rationale(
        cls,
        summary: ExecutionSummary,
        executions: tuple[Execution, ...],
        readiness: EnvironmentReadinessStatus,
    ) -> tuple[str, ...]:
        """Build concise management-facing rationale."""
        if readiness is (
            EnvironmentReadinessStatus.NOT_READY
        ):
            return (
                "No current execution data is available "
                "for the requested reporting scope.",
            )

        rationale = [
            (
                f"{summary.terminal} of {summary.total} "
                "tests are complete "
                f"({summary.completion_percentage:.2f}%)."
            )
        ]

        if summary.passed:
            rationale.append(
                f"{summary.passed} tests passed."
            )

        if summary.failed:
            rationale.append(
                f"{summary.failed} tests failed."
            )

        if summary.blocked:
            rationale.append(
                f"{summary.blocked} tests are blocked."
            )

        if summary.aborted:
            rationale.append(
                f"{summary.aborted} tests were aborted."
            )

        if summary.in_progress:
            rationale.append(
                f"{summary.in_progress} tests are in progress."
            )

        if summary.not_executed:
            rationale.append(
                f"{summary.not_executed} tests are not executed."
            )

        build_versions = cls._build_versions(executions)

        if len(build_versions) > 1:
            rationale.append(
                "Current results span multiple build versions."
            )

        if readiness is EnvironmentReadinessStatus.READY:
            rationale.append(
                "No failed, blocked, or aborted results "
                "remain in the current scope."
            )

        return tuple(rationale)

    @staticmethod
    def _build_recommended_actions(
        summary: ExecutionSummary,
        executions: tuple[Execution, ...],
        readiness: EnvironmentReadinessStatus,
    ) -> tuple[str, ...]:
        """Build actionable readiness recommendations."""
        if readiness is (
            EnvironmentReadinessStatus.NOT_READY
        ):
            return (
                "Confirm environment availability and deploy "
                "the intended test build.",
                "Create or import execution records for the "
                "required test cycle.",
            )

        actions: list[str] = []

        if summary.failed:
            actions.append(
                "Triage failed tests and confirm whether "
                "defects or test-data issues are responsible."
            )

        if summary.blocked:
            actions.append(
                "Remove blockers or agree an explicit "
                "release-risk acceptance."
            )

        if summary.aborted:
            actions.append(
                "Review aborted executions and schedule reruns."
            )

        if summary.in_progress:
            actions.append(
                "Complete tests currently in progress."
            )

        if summary.not_executed:
            actions.append(
                "Prioritize outstanding test execution."
            )

        if len(
            EnvironmentReadinessService._build_versions(
                executions
            )
        ) > 1:
            actions.append(
                "Align execution results to one intended "
                "build version before readiness approval."
            )

        if not actions:
            actions.append(
                "Maintain the current build and proceed to "
                "the next release-readiness checkpoint."
            )

        return tuple(actions)

    @staticmethod
    def _build_versions(
        executions: tuple[Execution, ...],
    ) -> tuple[str, ...]:
        """Return sorted unique non-empty build versions."""
        return tuple(
            sorted(
                {
                    execution.build_version.strip()
                    for execution in executions
                    if (
                        isinstance(
                            execution.build_version,
                            str,
                        )
                        and execution.build_version.strip()
                    )
                }
            )
        )

    @staticmethod
    def _normalize_environment(
        environment: Environment | str,
    ) -> Environment:
        """Return a canonical Environment."""
        try:
            return Environment.parse(environment)
        except (TypeError, ValueError) as exc:
            raise RepositoryValidationError(
                f"Invalid environment: {environment!r}."
            ) from exc

    @staticmethod
    def _normalize_cycle(
        execution_cycle: object,
    ) -> str:
        """Validate and normalize an execution cycle."""
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

    @classmethod
    def _normalize_environments(
        cls,
        environments: object,
    ) -> tuple[Environment, ...]:
        """Validate and normalize requested environments."""
        if isinstance(environments, (str, bytes)):
            raise RepositoryValidationError(
                "environments must be a collection."
            )

        try:
            raw_environments = list(environments)
        except TypeError as exc:
            raise RepositoryValidationError(
                "environments must be a collection."
            ) from exc

        if not raw_environments:
            raise RepositoryValidationError(
                "environments must contain at least "
                "one environment."
            )

        normalized = {
            cls._normalize_environment(environment)
            for environment in raw_environments
        }

        return tuple(
            sorted(
                normalized,
                key=lambda value: value.value,
            )
        )
