
"""Combined reporting snapshot for the Functional Testing Dashboard.

Purpose
-------
Combines execution, coverage, environment-readiness, and repository
validation results into one immutable dashboard payload.

The service contains management-reporting policy only. It does not
render HTML and does not write files.

Overall health policy
---------------------
RED:
    - repository validation contains errors
    - any requested environment is NOT_READY
    - current execution results contain FAILED, BLOCKED, or ABORTED tests

AMBER:
    - repository validation contains warnings
    - any environment is PARTIALLY_READY
    - testing is incomplete
    - Scenario coverage is incomplete
    - Automation pipeline or repository readiness is incomplete
    - execution results span multiple environments, cycles, or builds

GREEN:
    - no Red or Amber condition is present

Health is evaluated in that order. Red conditions always take precedence
over Amber conditions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable, Protocol, runtime_checkable

from canonical.enums import Environment
from repositories.base import RepositoryValidationError

from .coverage_summary import (
    CoverageSummaryService,
    TestCoverageSummary,
)
from .environment_summary import (
    EnvironmentReadinessService,
    EnvironmentReadinessStatus,
    EnvironmentReadinessSummary,
)
from .execution_summary import (
    ExecutionSummary,
    ExecutionSummaryService,
)


class DashboardHealth(StrEnum):
    """Management-facing dashboard health states."""

    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"


@runtime_checkable
class ValidationReportProtocol(Protocol):
    """Structural interface required from a validation report."""

    @property
    def error_count(self) -> int:
        """Return validation error count."""

    @property
    def warning_count(self) -> int:
        """Return validation warning count."""

    @property
    def is_valid(self) -> bool:
        """Return whether no validation errors exist."""

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible validation data."""


@dataclass(frozen=True, slots=True)
class ValidationSnapshot:
    """Dashboard-safe validation summary."""

    error_count: int
    warning_count: int
    is_valid: bool
    report: dict[str, object] | None = None

    def __post_init__(self) -> None:
        """Validate validation-summary values."""
        for field_name, value in {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
        }.items():
            if type(value) is not int:
                raise RepositoryValidationError(
                    f"{field_name} must be an integer."
                )

            if value < 0:
                raise RepositoryValidationError(
                    f"{field_name} must not be negative."
                )

        if type(self.is_valid) is not bool:
            raise RepositoryValidationError(
                "is_valid must be a Boolean value."
            )

        if self.is_valid != (self.error_count == 0):
            raise RepositoryValidationError(
                "is_valid must be true exactly when "
                "error_count is zero."
            )

        if (
            self.report is not None
            and not isinstance(self.report, dict)
        ):
            raise RepositoryValidationError(
                "report must be a dictionary or None."
            )

    @classmethod
    def empty(cls) -> ValidationSnapshot:
        """Return an empty successful validation result."""
        return cls(
            error_count=0,
            warning_count=0,
            is_valid=True,
            report=None,
        )

    @classmethod
    def from_report(
        cls,
        report: ValidationReportProtocol,
    ) -> ValidationSnapshot:
        """Create a dashboard snapshot from a validation report."""
        if not isinstance(
            report,
            ValidationReportProtocol,
        ):
            raise RepositoryValidationError(
                "validation_report must expose error_count, "
                "warning_count, is_valid, and to_dict()."
            )

        serialized = report.to_dict()

        if not isinstance(serialized, dict):
            raise RepositoryValidationError(
                "validation_report.to_dict() must return "
                "a dictionary."
            )

        return cls(
            error_count=report.error_count,
            warning_count=report.warning_count,
            is_valid=report.is_valid,
            report=serialized,
        )

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible validation data."""
        return {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "is_valid": self.is_valid,
            "report": self.report,
        }


@dataclass(frozen=True, slots=True)
class ExecutiveSummary:
    """Concise management-facing dashboard summary."""

    health: DashboardHealth
    headline: str
    achievements: tuple[str, ...]
    risks: tuple[str, ...]
    recommended_actions: tuple[str, ...]
    readiness_assessment: str

    def __post_init__(self) -> None:
        """Validate executive-summary content."""
        if not isinstance(self.health, DashboardHealth):
            raise RepositoryValidationError(
                "health must be a DashboardHealth."
            )

        for field_name, value in {
            "headline": self.headline,
            "readiness_assessment": (
                self.readiness_assessment
            ),
        }.items():
            if not isinstance(value, str) or not value.strip():
                raise RepositoryValidationError(
                    f"{field_name} must be a non-empty string."
                )

        for field_name, values in {
            "achievements": self.achievements,
            "risks": self.risks,
            "recommended_actions": (
                self.recommended_actions
            ),
        }.items():
            self._validate_string_tuple(
                values,
                field_name,
            )

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible executive-summary data."""
        return {
            "health": self.health.value,
            "headline": self.headline,
            "achievements": list(self.achievements),
            "risks": list(self.risks),
            "recommended_actions": list(
                self.recommended_actions
            ),
            "readiness_assessment": (
                self.readiness_assessment
            ),
        }

    @staticmethod
    def _validate_string_tuple(
        values: object,
        field_name: str,
    ) -> None:
        """Validate a tuple of non-empty strings."""
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


@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    """Immutable Functional Testing Dashboard payload."""

    schema_version: str
    generated_at: datetime

    health: DashboardHealth
    execution_cycle: str | None

    executive_summary: ExecutiveSummary
    execution_summary: ExecutionSummary
    coverage_summary: TestCoverageSummary

    environment_summaries: tuple[
        EnvironmentReadinessSummary,
        ...
    ]

    validation: ValidationSnapshot

    def __post_init__(self) -> None:
        """Validate snapshot consistency."""
        if (
            not isinstance(self.schema_version, str)
            or not self.schema_version.strip()
        ):
            raise RepositoryValidationError(
                "schema_version must be a non-empty string."
            )

        if not isinstance(self.generated_at, datetime):
            raise RepositoryValidationError(
                "generated_at must be a datetime."
            )

        if (
            self.generated_at.tzinfo is None
            or self.generated_at.utcoffset() is None
        ):
            raise RepositoryValidationError(
                "generated_at must be timezone-aware."
            )

        if not isinstance(self.health, DashboardHealth):
            raise RepositoryValidationError(
                "health must be a DashboardHealth."
            )

        if not isinstance(
            self.executive_summary,
            ExecutiveSummary,
        ):
            raise RepositoryValidationError(
                "executive_summary must be an "
                "ExecutiveSummary."
            )

        if self.executive_summary.health is not self.health:
            raise RepositoryValidationError(
                "Executive-summary health must match "
                "snapshot health."
            )

        if not isinstance(
            self.execution_summary,
            ExecutionSummary,
        ):
            raise RepositoryValidationError(
                "execution_summary must be an "
                "ExecutionSummary."
            )

        if not isinstance(
            self.coverage_summary,
            TestCoverageSummary,
        ):
            raise RepositoryValidationError(
                "coverage_summary must be a "
                "TestCoverageSummary."
            )

        if not isinstance(
            self.environment_summaries,
            tuple,
        ):
            raise RepositoryValidationError(
                "environment_summaries must be a tuple."
            )

        if any(
            not isinstance(
                summary,
                EnvironmentReadinessSummary,
            )
            for summary in self.environment_summaries
        ):
            raise RepositoryValidationError(
                "environment_summaries must contain "
                "EnvironmentReadinessSummary values."
            )

        environments = tuple(
            summary.environment
            for summary in self.environment_summaries
        )

        if len(set(environments)) != len(environments):
            raise RepositoryValidationError(
                "environment_summaries must not contain "
                "duplicate environments."
            )

        if environments != tuple(
            sorted(
                environments,
                key=lambda value: value.value,
            )
        ):
            raise RepositoryValidationError(
                "environment_summaries must be sorted."
            )

        if not isinstance(
            self.validation,
            ValidationSnapshot,
        ):
            raise RepositoryValidationError(
                "validation must be a ValidationSnapshot."
            )

    @property
    def environment_count(self) -> int:
        """Return the number of represented environments."""
        return len(self.environment_summaries)

    @property
    def ready_environment_count(self) -> int:
        """Return environments assessed as Ready."""
        return sum(
            summary.readiness
            is EnvironmentReadinessStatus.READY
            for summary in self.environment_summaries
        )

    @property
    def partially_ready_environment_count(self) -> int:
        """Return environments assessed as Partially Ready."""
        return sum(
            summary.readiness
            is EnvironmentReadinessStatus.PARTIALLY_READY
            for summary in self.environment_summaries
        )

    @property
    def not_ready_environment_count(self) -> int:
        """Return environments assessed as Not Ready."""
        return sum(
            summary.readiness
            is EnvironmentReadinessStatus.NOT_READY
            for summary in self.environment_summaries
        )

    def to_dict(self) -> dict[str, object]:
        """Return the complete JSON-compatible dashboard payload."""
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at.isoformat(),
            "health": self.health.value,
            "execution_cycle": self.execution_cycle,
            "environment_count": self.environment_count,
            "ready_environment_count": (
                self.ready_environment_count
            ),
            "partially_ready_environment_count": (
                self.partially_ready_environment_count
            ),
            "not_ready_environment_count": (
                self.not_ready_environment_count
            ),
            "executive_summary": (
                self.executive_summary.to_dict()
            ),
            "execution_summary": (
                self.execution_summary.to_dict()
            ),
            "coverage_summary": (
                self.coverage_summary.to_dict()
            ),
            "environment_summaries": [
                summary.to_dict()
                for summary in self.environment_summaries
            ],
            "validation": self.validation.to_dict(),
        }


class DashboardSnapshotService:
    """Build the combined Functional Testing Dashboard snapshot."""

    SCHEMA_VERSION = "1.0"

    def __init__(
        self,
        execution_summary_service: ExecutionSummaryService,
        coverage_summary_service: CoverageSummaryService,
        environment_readiness_service: (
            EnvironmentReadinessService
        ),
    ) -> None:
        """Store reporting-service dependencies."""
        if not isinstance(
            execution_summary_service,
            ExecutionSummaryService,
        ):
            raise RepositoryValidationError(
                "execution_summary_service must be an "
                "ExecutionSummaryService."
            )

        if not isinstance(
            coverage_summary_service,
            CoverageSummaryService,
        ):
            raise RepositoryValidationError(
                "coverage_summary_service must be a "
                "CoverageSummaryService."
            )

        if not isinstance(
            environment_readiness_service,
            EnvironmentReadinessService,
        ):
            raise RepositoryValidationError(
                "environment_readiness_service must be an "
                "EnvironmentReadinessService."
            )

        self.execution_summaries = (
            execution_summary_service
        )
        self.coverage_summaries = (
            coverage_summary_service
        )
        self.environment_readiness = (
            environment_readiness_service
        )

    def build(
        self,
        *,
        generated_at: datetime,
        execution_cycle: str | None = None,
        environments: (
            Iterable[Environment | str] | None
        ) = None,
        active_only: bool = True,
        validation_report: (
            ValidationReportProtocol | None
        ) = None,
    ) -> DashboardSnapshot:
        """Build one dashboard reporting snapshot."""
        self._validate_generated_at(generated_at)

        normalized_cycle = (
            None
            if execution_cycle is None
            else self._normalize_cycle(execution_cycle)
        )

        execution_summary = (
            self.execution_summaries.summarize(
                execution_cycle=normalized_cycle
            )
        )

        coverage_summary = (
            self.coverage_summaries.summarize(
                active_only=active_only
            )
        )

        environment_summaries = (
            self.environment_readiness.summarize_all(
                execution_cycle=normalized_cycle,
                environments=environments,
            )
        )

        validation = (
            ValidationSnapshot.empty()
            if validation_report is None
            else ValidationSnapshot.from_report(
                validation_report
            )
        )

        health = self._assess_health(
            execution_summary=execution_summary,
            coverage_summary=coverage_summary,
            environment_summaries=(
                environment_summaries
            ),
            validation=validation,
        )

        executive_summary = (
            self._build_executive_summary(
                health=health,
                execution_summary=execution_summary,
                coverage_summary=coverage_summary,
                environment_summaries=(
                    environment_summaries
                ),
                validation=validation,
            )
        )

        return DashboardSnapshot(
            schema_version=self.SCHEMA_VERSION,
            generated_at=generated_at,
            health=health,
            execution_cycle=normalized_cycle,
            executive_summary=executive_summary,
            execution_summary=execution_summary,
            coverage_summary=coverage_summary,
            environment_summaries=(
                environment_summaries
            ),
            validation=validation,
        )

    @staticmethod
    def _assess_health(
        *,
        execution_summary: ExecutionSummary,
        coverage_summary: TestCoverageSummary,
        environment_summaries: tuple[
            EnvironmentReadinessSummary,
            ...
        ],
        validation: ValidationSnapshot,
    ) -> DashboardHealth:
        """Apply deterministic overall-health policy."""
        has_not_ready_environment = any(
            summary.readiness
            is EnvironmentReadinessStatus.NOT_READY
            for summary in environment_summaries
        )

        has_execution_exception = (
            execution_summary.failed > 0
            or execution_summary.blocked > 0
            or execution_summary.aborted > 0
        )

        if (
            validation.error_count > 0
            or has_not_ready_environment
            or has_execution_exception
        ):
            return DashboardHealth.RED

        has_partial_environment = any(
            summary.readiness
            is EnvironmentReadinessStatus.PARTIALLY_READY
            for summary in environment_summaries
        )

        has_mixed_builds = any(
            summary.has_mixed_build_versions
            for summary in environment_summaries
        )

        has_coverage_gap = (
            coverage_summary.uncovered_scenarios > 0
            or not coverage_summary
            .has_full_automation_coverage
            or coverage_summary
            .automation_without_pipeline
            > 0
            or coverage_summary
            .automation_without_repository
            > 0
        )

        has_incomplete_testing = (
            execution_summary.total == 0
            or not execution_summary.is_complete
        )

        if (
            validation.warning_count > 0
            or has_partial_environment
            or has_mixed_builds
            or has_coverage_gap
            or has_incomplete_testing
            or execution_summary
            .includes_multiple_environments
            or execution_summary.includes_multiple_cycles
        ):
            return DashboardHealth.AMBER

        return DashboardHealth.GREEN

    @classmethod
    def _build_executive_summary(
        cls,
        *,
        health: DashboardHealth,
        execution_summary: ExecutionSummary,
        coverage_summary: TestCoverageSummary,
        environment_summaries: tuple[
            EnvironmentReadinessSummary,
            ...
        ],
        validation: ValidationSnapshot,
    ) -> ExecutiveSummary:
        """Build concise executive narrative."""
        headline = {
            DashboardHealth.GREEN: (
                "Functional testing is on track with no "
                "material readiness exceptions."
            ),
            DashboardHealth.AMBER: (
                "Functional testing is progressing, but "
                "readiness gaps require management attention."
            ),
            DashboardHealth.RED: (
                "Functional testing has critical exceptions "
                "affecting release readiness."
            ),
        }[health]

        achievements = cls._build_achievements(
            execution_summary,
            coverage_summary,
            environment_summaries,
        )

        risks = cls._build_risks(
            execution_summary,
            coverage_summary,
            environment_summaries,
            validation,
        )

        actions = cls._build_actions(
            execution_summary,
            coverage_summary,
            environment_summaries,
            validation,
        )

        readiness_assessment = (
            cls._build_readiness_assessment(
                environment_summaries
            )
        )

        return ExecutiveSummary(
            health=health,
            headline=headline,
            achievements=achievements,
            risks=risks,
            recommended_actions=actions,
            readiness_assessment=readiness_assessment,
        )

    @staticmethod
    def _build_achievements(
        execution_summary: ExecutionSummary,
        coverage_summary: TestCoverageSummary,
        environment_summaries: tuple[
            EnvironmentReadinessSummary,
            ...
        ],
    ) -> tuple[str, ...]:
        """Build measurable achievements."""
        achievements: list[str] = []

        if execution_summary.terminal > 0:
            achievements.append(
                f"{execution_summary.terminal} tests "
                "have completed."
            )

        if execution_summary.passed > 0:
            achievements.append(
                f"{execution_summary.passed} tests "
                f"passed, with a {execution_summary.pass_rate:.2f}% "
                "terminal-result pass rate."
            )

        if coverage_summary.covered_scenarios > 0:
            achievements.append(
                f"{coverage_summary.covered_scenarios} of "
                f"{coverage_summary.total_scenarios} Scenarios "
                "have test coverage."
            )

        ready_count = sum(
            summary.readiness
            is EnvironmentReadinessStatus.READY
            for summary in environment_summaries
        )

        if ready_count:
            achievements.append(
                f"{ready_count} environment"
                f"{'' if ready_count == 1 else 's'} "
                "assessed as Ready."
            )

        return tuple(achievements)

    @staticmethod
    def _build_risks(
        execution_summary: ExecutionSummary,
        coverage_summary: TestCoverageSummary,
        environment_summaries: tuple[
            EnvironmentReadinessSummary,
            ...
        ],
        validation: ValidationSnapshot,
    ) -> tuple[str, ...]:
        """Build material dashboard risks."""
        risks: list[str] = []

        if validation.error_count:
            risks.append(
                f"{validation.error_count} repository "
                "validation errors affect reporting integrity."
            )

        if validation.warning_count:
            risks.append(
                f"{validation.warning_count} repository "
                "validation warnings require review."
            )

        if execution_summary.failed:
            risks.append(
                f"{execution_summary.failed} tests are failed."
            )

        if execution_summary.blocked:
            risks.append(
                f"{execution_summary.blocked} tests are blocked."
            )

        if execution_summary.aborted:
            risks.append(
                f"{execution_summary.aborted} tests are aborted."
            )

        if execution_summary.outstanding:
            risks.append(
                f"{execution_summary.outstanding} tests remain "
                "in progress or not executed."
            )

        if coverage_summary.uncovered_scenarios:
            risks.append(
                f"{coverage_summary.uncovered_scenarios} active "
                "Scenarios have no eligible Test Definition."
            )

        if coverage_summary.automation_backlog:
            risks.append(
                f"{coverage_summary.automation_backlog} "
                "manually covered Scenarios remain in the "
                "automation backlog."
            )

        not_ready_count = sum(
            summary.readiness
            is EnvironmentReadinessStatus.NOT_READY
            for summary in environment_summaries
        )

        if not_ready_count:
            risks.append(
                f"{not_ready_count} environment"
                f"{'' if not_ready_count == 1 else 's'} "
                "are Not Ready."
            )

        partial_count = sum(
            summary.readiness
            is EnvironmentReadinessStatus.PARTIALLY_READY
            for summary in environment_summaries
        )

        if partial_count:
            risks.append(
                f"{partial_count} environment"
                f"{'' if partial_count == 1 else 's'} "
                "are only Partially Ready."
            )

        return tuple(risks)

    @staticmethod
    def _build_actions(
        execution_summary: ExecutionSummary,
        coverage_summary: TestCoverageSummary,
        environment_summaries: tuple[
            EnvironmentReadinessSummary,
            ...
        ],
        validation: ValidationSnapshot,
    ) -> tuple[str, ...]:
        """Build deduplicated management actions."""
        actions: list[str] = []

        if validation.error_count:
            actions.append(
                "Resolve repository validation errors before "
                "using the snapshot for release approval."
            )

        if execution_summary.failed:
            actions.append(
                "Triage failed tests and link confirmed defects."
            )

        if execution_summary.blocked:
            actions.append(
                "Assign owners and target dates to testing blockers."
            )

        if execution_summary.aborted:
            actions.append(
                "Review aborted tests and schedule controlled reruns."
            )

        if execution_summary.outstanding:
            actions.append(
                "Prioritize outstanding execution against "
                "release-critical Scenarios."
            )

        if coverage_summary.uncovered_scenarios:
            actions.append(
                "Create Test Definitions for uncovered active "
                "Scenarios."
            )

        if coverage_summary.automation_backlog:
            actions.append(
                "Prioritize automation backlog by business "
                "criticality and regression frequency."
            )

        for summary in environment_summaries:
            actions.extend(summary.recommended_actions)

        deduplicated: list[str] = []
        seen: set[str] = set()

        for action in actions:
            if action not in seen:
                seen.add(action)
                deduplicated.append(action)

        if not deduplicated:
            deduplicated.append(
                "Maintain current execution momentum and "
                "proceed to the next readiness checkpoint."
            )

        return tuple(deduplicated)

    @staticmethod
    def _build_readiness_assessment(
        environment_summaries: tuple[
            EnvironmentReadinessSummary,
            ...
        ],
    ) -> str:
        """Build a concise readiness statement."""
        if not environment_summaries:
            return (
                "No environment readiness data is available."
            )

        ready = sum(
            summary.readiness
            is EnvironmentReadinessStatus.READY
            for summary in environment_summaries
        )
        partial = sum(
            summary.readiness
            is EnvironmentReadinessStatus.PARTIALLY_READY
            for summary in environment_summaries
        )
        not_ready = sum(
            summary.readiness
            is EnvironmentReadinessStatus.NOT_READY
            for summary in environment_summaries
        )

        return (
            f"{ready} Ready, {partial} Partially Ready, "
            f"and {not_ready} Not Ready across "
            f"{len(environment_summaries)} environments."
        )

    @staticmethod
    def _validate_generated_at(
        generated_at: object,
    ) -> None:
        """Validate the snapshot generation timestamp."""
        if not isinstance(generated_at, datetime):
            raise RepositoryValidationError(
                "generated_at must be a datetime."
            )

        if (
            generated_at.tzinfo is None
            or generated_at.utcoffset() is None
        ):
            raise RepositoryValidationError(
                "generated_at must be timezone-aware."
            )

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
