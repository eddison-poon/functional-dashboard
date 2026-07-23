
"""Cross-repository validation for canonical dashboard entities.

Purpose
-------
Validates relationships spanning Requirement, Scenario,
TestDefinition, and Execution repositories.

Canonical entity models validate their own fields. Individual
repositories validate storage and query behaviour. This module validates
references and governance conditions that can only be assessed when
multiple repositories are considered together.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from canonical.enums import TestType
from canonical.execution import Execution
from canonical.scenario import Scenario
from canonical.test_definition import TestDefinition

from .execution_repository import ExecutionRepository
from .requirement_repository import RequirementRepository
from .scenario_repository import ScenarioRepository
from .test_definition_repository import TestDefinitionRepository


class ValidationSeverity(str, Enum):
    """Severity assigned to a cross-repository validation finding."""

    ERROR = "ERROR"
    WARNING = "WARNING"


class ValidationCode(str, Enum):
    """Stable identifiers for cross-repository validation findings."""

    MISSING_REQUIREMENT = "MISSING_REQUIREMENT"
    MISSING_SCENARIO = "MISSING_SCENARIO"
    MISSING_TEST_DEFINITION = "MISSING_TEST_DEFINITION"
    MISSING_RERUN_EXECUTION = "MISSING_RERUN_EXECUTION"

    RERUN_TEST_DEFINITION_MISMATCH = (
        "RERUN_TEST_DEFINITION_MISMATCH"
    )
    RERUN_ENVIRONMENT_MISMATCH = (
        "RERUN_ENVIRONMENT_MISMATCH"
    )

    REQUIREMENT_WITHOUT_SCENARIO = (
        "REQUIREMENT_WITHOUT_SCENARIO"
    )
    SCENARIO_WITHOUT_TEST_DEFINITION = (
        "SCENARIO_WITHOUT_TEST_DEFINITION"
    )
    TEST_DEFINITION_WITHOUT_EXECUTION = (
        "TEST_DEFINITION_WITHOUT_EXECUTION"
    )

    SCENARIO_WITHOUT_MANUAL_TEST = (
        "SCENARIO_WITHOUT_MANUAL_TEST"
    )
    SCENARIO_WITHOUT_AUTOMATION_TEST = (
        "SCENARIO_WITHOUT_AUTOMATION_TEST"
    )


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    """One immutable cross-repository validation finding."""

    severity: ValidationSeverity
    code: ValidationCode
    entity_type: str
    entity_id: str
    message: str
    referenced_entity_type: str | None = None
    referenced_entity_id: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Return JSON-compatible validation finding data."""
        return {
            "severity": self.severity.value,
            "code": self.code.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "message": self.message,
            "referenced_entity_type": (
                self.referenced_entity_type
            ),
            "referenced_entity_id": (
                self.referenced_entity_id
            ),
        }


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Immutable result of one cross-repository validation run."""

    findings: tuple[ValidationFinding, ...]

    @property
    def errors(self) -> tuple[ValidationFinding, ...]:
        """Return findings classified as errors."""
        return tuple(
            finding
            for finding in self.findings
            if finding.severity is ValidationSeverity.ERROR
        )

    @property
    def warnings(self) -> tuple[ValidationFinding, ...]:
        """Return findings classified as warnings."""
        return tuple(
            finding
            for finding in self.findings
            if finding.severity is ValidationSeverity.WARNING
        )

    @property
    def is_valid(self) -> bool:
        """Return whether no validation errors were detected."""
        return not self.errors

    @property
    def error_count(self) -> int:
        """Return the number of validation errors."""
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """Return the number of validation warnings."""
        return len(self.warnings)

    def has_code(
        self,
        code: ValidationCode,
    ) -> bool:
        """Return whether the report contains a finding code."""
        return any(
            finding.code is code
            for finding in self.findings
        )

    def findings_by_code(
        self,
        code: ValidationCode,
    ) -> tuple[ValidationFinding, ...]:
        """Return all findings carrying one validation code."""
        return tuple(
            finding
            for finding in self.findings
            if finding.code is code
        )

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible validation report data."""
        return {
            "is_valid": self.is_valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
        }


class RepositoryRelationshipValidator:
    """Validate relationships across all canonical repositories."""

    def __init__(
        self,
        requirement_repository: RequirementRepository,
        scenario_repository: ScenarioRepository,
        test_definition_repository: TestDefinitionRepository,
        execution_repository: ExecutionRepository,
    ) -> None:
        """Store the repositories participating in validation."""
        self.requirements = requirement_repository
        self.scenarios = scenario_repository
        self.test_definitions = test_definition_repository
        self.executions = execution_repository

    def validate(self) -> ValidationReport:
        """Run all cross-repository validation checks."""
        findings: list[ValidationFinding] = []

        findings.extend(
            self._validate_scenario_requirements()
        )
        findings.extend(
            self._validate_test_definition_scenarios()
        )
        findings.extend(
            self._validate_execution_test_definitions()
        )
        findings.extend(
            self._validate_execution_reruns()
        )
        findings.extend(
            self._find_orphan_requirements()
        )
        findings.extend(
            self._find_orphan_scenarios()
        )
        findings.extend(
            self._find_unexecuted_test_definitions()
        )
        findings.extend(
            self._find_scenario_test_type_gaps()
        )

        return ValidationReport(
            findings=self._sort_findings(findings)
        )

    def _validate_scenario_requirements(
        self,
    ) -> list[ValidationFinding]:
        """Detect Scenario references to missing Requirements."""
        findings: list[ValidationFinding] = []

        for scenario in self.scenarios.list_all():
            for requirement_id in scenario.requirement_ids:
                if self.requirements.exists(requirement_id):
                    continue

                findings.append(
                    ValidationFinding(
                        severity=ValidationSeverity.ERROR,
                        code=ValidationCode.MISSING_REQUIREMENT,
                        entity_type="Scenario",
                        entity_id=scenario.scenario_id,
                        referenced_entity_type="Requirement",
                        referenced_entity_id=requirement_id,
                        message=(
                            f"Scenario {scenario.scenario_id!r} "
                            f"references missing Requirement "
                            f"{requirement_id!r}."
                        ),
                    )
                )

        return findings

    def _validate_test_definition_scenarios(
        self,
    ) -> list[ValidationFinding]:
        """Detect Test Definitions referencing missing Scenarios."""
        findings: list[ValidationFinding] = []

        for test_definition in self.test_definitions.list_all():
            if self.scenarios.exists(
                test_definition.scenario_id
            ):
                continue

            findings.append(
                ValidationFinding(
                    severity=ValidationSeverity.ERROR,
                    code=ValidationCode.MISSING_SCENARIO,
                    entity_type="TestDefinition",
                    entity_id=(
                        test_definition.test_definition_id
                    ),
                    referenced_entity_type="Scenario",
                    referenced_entity_id=(
                        test_definition.scenario_id
                    ),
                    message=(
                        "Test Definition "
                        f"{test_definition.test_definition_id!r} "
                        "references missing Scenario "
                        f"{test_definition.scenario_id!r}."
                    ),
                )
            )

        return findings

    def _validate_execution_test_definitions(
        self,
    ) -> list[ValidationFinding]:
        """Detect Executions referencing missing Test Definitions."""
        findings: list[ValidationFinding] = []

        for execution in self.executions.list_all():
            if self.test_definitions.exists(
                execution.test_definition_id
            ):
                continue

            findings.append(
                ValidationFinding(
                    severity=ValidationSeverity.ERROR,
                    code=(
                        ValidationCode
                        .MISSING_TEST_DEFINITION
                    ),
                    entity_type="Execution",
                    entity_id=execution.execution_id,
                    referenced_entity_type="TestDefinition",
                    referenced_entity_id=(
                        execution.test_definition_id
                    ),
                    message=(
                        f"Execution {execution.execution_id!r} "
                        "references missing Test Definition "
                        f"{execution.test_definition_id!r}."
                    ),
                )
            )

        return findings

    def _validate_execution_reruns(
        self,
    ) -> list[ValidationFinding]:
        """Validate rerun references and relationship consistency."""
        findings: list[ValidationFinding] = []

        for execution in self.executions.find_reruns():
            original_id = execution.rerun_of_execution_id

            if original_id is None:
                continue

            original = self.executions.get_or_none(
                original_id
            )

            if original is None:
                findings.append(
                    ValidationFinding(
                        severity=ValidationSeverity.ERROR,
                        code=(
                            ValidationCode
                            .MISSING_RERUN_EXECUTION
                        ),
                        entity_type="Execution",
                        entity_id=execution.execution_id,
                        referenced_entity_type="Execution",
                        referenced_entity_id=original_id,
                        message=(
                            f"Execution {execution.execution_id!r} "
                            "references missing original Execution "
                            f"{original_id!r}."
                        ),
                    )
                )
                continue

            findings.extend(
                self._validate_rerun_consistency(
                    execution,
                    original,
                )
            )

        return findings

    @staticmethod
    def _validate_rerun_consistency(
        rerun: Execution,
        original: Execution,
    ) -> list[ValidationFinding]:
        """Validate identity constraints between a rerun and original."""
        findings: list[ValidationFinding] = []

        if (
            rerun.test_definition_id
            != original.test_definition_id
        ):
            findings.append(
                ValidationFinding(
                    severity=ValidationSeverity.ERROR,
                    code=(
                        ValidationCode
                        .RERUN_TEST_DEFINITION_MISMATCH
                    ),
                    entity_type="Execution",
                    entity_id=rerun.execution_id,
                    referenced_entity_type="Execution",
                    referenced_entity_id=(
                        original.execution_id
                    ),
                    message=(
                        f"Rerun Execution {rerun.execution_id!r} "
                        "uses Test Definition "
                        f"{rerun.test_definition_id!r}, but its "
                        "original Execution "
                        f"{original.execution_id!r} uses "
                        f"{original.test_definition_id!r}."
                    ),
                )
            )

        if rerun.environment is not original.environment:
            findings.append(
                ValidationFinding(
                    severity=ValidationSeverity.ERROR,
                    code=(
                        ValidationCode
                        .RERUN_ENVIRONMENT_MISMATCH
                    ),
                    entity_type="Execution",
                    entity_id=rerun.execution_id,
                    referenced_entity_type="Execution",
                    referenced_entity_id=(
                        original.execution_id
                    ),
                    message=(
                        f"Rerun Execution {rerun.execution_id!r} "
                        f"uses environment "
                        f"{rerun.environment.value!r}, but its "
                        "original Execution "
                        f"{original.execution_id!r} uses "
                        f"{original.environment.value!r}."
                    ),
                )
            )

        return findings

    def _find_orphan_requirements(
        self,
    ) -> list[ValidationFinding]:
        """Find Requirements not covered by any Scenario."""
        referenced_requirement_ids = {
            requirement_id
            for scenario in self.scenarios.list_all()
            for requirement_id in scenario.requirement_ids
        }

        return [
            ValidationFinding(
                severity=ValidationSeverity.WARNING,
                code=(
                    ValidationCode
                    .REQUIREMENT_WITHOUT_SCENARIO
                ),
                entity_type="Requirement",
                entity_id=requirement.requirement_id,
                message=(
                    f"Requirement {requirement.requirement_id!r} "
                    "is not covered by any Scenario."
                ),
            )
            for requirement in self.requirements.list_all()
            if requirement.requirement_id
            not in referenced_requirement_ids
        ]

    def _find_orphan_scenarios(
        self,
    ) -> list[ValidationFinding]:
        """Find Scenarios without any Test Definition."""
        referenced_scenario_ids = {
            test_definition.scenario_id
            for test_definition
            in self.test_definitions.list_all()
        }

        return [
            ValidationFinding(
                severity=ValidationSeverity.WARNING,
                code=(
                    ValidationCode
                    .SCENARIO_WITHOUT_TEST_DEFINITION
                ),
                entity_type="Scenario",
                entity_id=scenario.scenario_id,
                message=(
                    f"Scenario {scenario.scenario_id!r} "
                    "has no Test Definition."
                ),
            )
            for scenario in self.scenarios.list_all()
            if scenario.scenario_id
            not in referenced_scenario_ids
        ]

    def _find_unexecuted_test_definitions(
        self,
    ) -> list[ValidationFinding]:
        """Find Test Definitions with no Execution records."""
        referenced_test_definition_ids = {
            execution.test_definition_id
            for execution in self.executions.list_all()
        }

        return [
            ValidationFinding(
                severity=ValidationSeverity.WARNING,
                code=(
                    ValidationCode
                    .TEST_DEFINITION_WITHOUT_EXECUTION
                ),
                entity_type="TestDefinition",
                entity_id=(
                    test_definition.test_definition_id
                ),
                message=(
                    "Test Definition "
                    f"{test_definition.test_definition_id!r} "
                    "has no Execution record."
                ),
            )
            for test_definition
            in self.test_definitions.list_all()
            if test_definition.test_definition_id
            not in referenced_test_definition_ids
        ]

    def _find_scenario_test_type_gaps(
        self,
    ) -> list[ValidationFinding]:
        """Identify Manual and Automation coverage gaps by Scenario."""
        findings: list[ValidationFinding] = []

        test_definitions_by_scenario: dict[
            str,
            list[TestDefinition],
        ] = {}

        for test_definition in self.test_definitions.list_all():
            test_definitions_by_scenario.setdefault(
                test_definition.scenario_id,
                [],
            ).append(test_definition)

        for scenario in self.scenarios.list_all():
            scenario_tests = test_definitions_by_scenario.get(
                scenario.scenario_id,
                [],
            )

            if not scenario_tests:
                continue

            test_types = {
                test_definition.test_type
                for test_definition in scenario_tests
            }

            if TestType.MANUAL not in test_types:
                findings.append(
                    self._coverage_gap_finding(
                        scenario,
                        ValidationCode
                        .SCENARIO_WITHOUT_MANUAL_TEST,
                        "Manual",
                    )
                )

            if TestType.AUTOMATION not in test_types:
                findings.append(
                    self._coverage_gap_finding(
                        scenario,
                        ValidationCode
                        .SCENARIO_WITHOUT_AUTOMATION_TEST,
                        "Automation",
                    )
                )

        return findings

    @staticmethod
    def _coverage_gap_finding(
        scenario: Scenario,
        code: ValidationCode,
        test_type_name: str,
    ) -> ValidationFinding:
        """Build one Scenario test-type coverage warning."""
        return ValidationFinding(
            severity=ValidationSeverity.WARNING,
            code=code,
            entity_type="Scenario",
            entity_id=scenario.scenario_id,
            message=(
                f"Scenario {scenario.scenario_id!r} "
                f"has no {test_type_name} Test Definition."
            ),
        )

    @staticmethod
    def _sort_findings(
        findings: Iterable[ValidationFinding],
    ) -> tuple[ValidationFinding, ...]:
        """Return findings in deterministic management-friendly order."""
        severity_order = {
            ValidationSeverity.ERROR: 0,
            ValidationSeverity.WARNING: 1,
        }

        return tuple(
            sorted(
                findings,
                key=lambda finding: (
                    severity_order[finding.severity],
                    finding.code.value,
                    finding.entity_type,
                    finding.entity_id,
                    finding.referenced_entity_id or "",
                ),
            )
        )
