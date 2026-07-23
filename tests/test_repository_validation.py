"""Unit tests for cross-repository relationship validation."""

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.execution import Execution  # noqa: E402
from canonical.requirement import Requirement  # noqa: E402
from canonical.scenario import Scenario  # noqa: E402
from canonical.test_definition import (  # noqa: E402
    TestDefinition,
    TestStep,
)
from repositories.execution_repository import (  # noqa: E402
    ExecutionRepository,
)
from repositories.requirement_repository import (  # noqa: E402
    RequirementRepository,
)
from repositories.scenario_repository import (  # noqa: E402
    ScenarioRepository,
)
from repositories.test_definition_repository import (  # noqa: E402
    TestDefinitionRepository,
)
from repositories.validation import (  # noqa: E402
    RepositoryRelationshipValidator,
    ValidationCode,
    ValidationFinding,
    ValidationReport,
    ValidationSeverity,
)


UTC = timezone.utc

BASE_TIME = datetime(
    2026,
    7,
    20,
    9,
    0,
    tzinfo=UTC,
)


def requirement(
    requirement_id: str = "REQ-001",
    *,
    title: str = "User can sign in",
) -> Requirement:
    """Create a valid canonical Requirement."""

    return Requirement(
        requirement_id=requirement_id,
        title=title,
        source_system="JIRA",
        requirement_type="STORY",
        status="READY",
        priority="HIGH",
        description="Authentication business requirement.",
        source_project="AUTH",
        source_url=(
            f"https://jira.example.com/browse/"
            f"{requirement_id}"
        ),
        component="Authentication",
        labels=["functional-testing"],
        release="Release 1",
        sprint="Sprint 1",
        owner="Product Owner",
        active=True,
    )


def scenario(
    scenario_id: str = "SCN-001",
    *,
    requirement_ids: tuple[str, ...] | list[str] = (
        "REQ-001",
    ),
    feature_id: str = "FEATURE-AUTH",
    name: str = "Successful user sign-in",
) -> Scenario:
    """Create a valid canonical Scenario."""

    return Scenario(
        scenario_id=scenario_id,
        feature_id=feature_id,
        requirement_ids=requirement_ids,
        name=name,
        scenario_type="POSITIVE",
        priority="HIGH",
        description="Validate successful authentication.",
        tags=["authentication"],
        preconditions=["A valid user account exists."],
        expected_outcome="The user reaches the home page.",
        owner="QA Lead",
        active=True,
    )


def manual_test_definition(
    test_definition_id: str = "TEST-MANUAL-001",
    *,
    scenario_id: str = "SCN-001",
    name: str = "Manual successful sign-in",
) -> TestDefinition:
    """Create a valid Manual Test Definition."""

    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="MANUAL",
        name=name,
        status="ACTIVE",
        version="1.0",
        description="Manual sign-in validation.",
        preconditions=["A valid user account exists."],
        steps=[
            TestStep(
                step_number=1,
                action="Open the sign-in page.",
                expected_result="The sign-in page is displayed.",
            ),
            TestStep(
                step_number=2,
                action="Enter valid credentials and submit.",
                expected_result="The home page is displayed.",
                test_data="Valid functional test user.",
            ),
        ],
        owner="Manual QA",
        tags=["authentication", "manual"],
    )


def automation_test_definition(
    test_definition_id: str = "TEST-AUTO-001",
    *,
    scenario_id: str = "SCN-001",
    name: str = "Automated successful sign-in",
) -> TestDefinition:
    """Create a valid Automation Test Definition."""

    return TestDefinition(
        test_definition_id=test_definition_id,
        scenario_id=scenario_id,
        test_type="AUTOMATION",
        name=name,
        status="ACTIVE",
        version="1.0",
        description="Automated sign-in validation.",
        preconditions=["A valid user account exists."],
        framework="PLAYWRIGHT",
        repository="functional-dashboard-tests",
        script_path="tests/authentication/test_login.py",
        pipeline_name="functional-regression",
        owner="Automation QA",
        tags=["authentication", "automation"],
    )


def execution(
    execution_id: str = "EXEC-001",
    *,
    test_definition_id: str = "TEST-MANUAL-001",
    environment: str = "SIT",
    status: str = "PASSED",
    started_at: datetime | None = BASE_TIME,
    completed_at: datetime | None = (
        BASE_TIME + timedelta(minutes=5)
    ),
    rerun_of_execution_id: str | None = None,
) -> Execution:
    """Create a valid canonical Execution."""

    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status=status,
        execution_cycle="SIT Cycle 1",
        started_at=started_at,
        completed_at=completed_at,
        executed_by="QA Service",
        build_version="1.0.0",
        source_system="MANUAL_ENTRY",
        external_reference=f"EXT-{execution_id}",
        evidence_ids=[f"EVIDENCE-{execution_id}"],
        remarks="Functional execution result.",
        rerun_of_execution_id=rerun_of_execution_id,
    )


class RepositoryValidationFixtureTests(unittest.TestCase):
    """Base fixture for cross-repository validation tests."""

    def setUp(self) -> None:
        self.requirements = RequirementRepository()
        self.scenarios = ScenarioRepository()
        self.test_definitions = TestDefinitionRepository()
        self.executions = ExecutionRepository()

        self.validator = RepositoryRelationshipValidator(
            requirement_repository=self.requirements,
            scenario_repository=self.scenarios,
            test_definition_repository=(
                self.test_definitions
            ),
            execution_repository=self.executions,
        )

    def add_complete_graph(self) -> None:
        """Add one fully connected Manual and Automation graph."""

        self.requirements.add(
            requirement("REQ-001")
        )

        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=["REQ-001"],
            )
        )

        self.test_definitions.add_many(
            [
                manual_test_definition(
                    "TEST-MANUAL-001",
                    scenario_id="SCN-001",
                ),
                automation_test_definition(
                    "TEST-AUTO-001",
                    scenario_id="SCN-001",
                ),
            ]
        )

        self.executions.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-002",
                    test_definition_id=(
                        "TEST-AUTO-001"
                    ),
                ),
            ]
        )


class RepositoryValidationHealthyGraphTests(
    RepositoryValidationFixtureTests
):
    """Tests covering a fully connected repository graph."""

    def test_complete_graph_has_no_findings(self) -> None:
        self.add_complete_graph()

        report = self.validator.validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)
        self.assertEqual(report.findings, ())

    def test_empty_repositories_are_valid(self) -> None:
        report = self.validator.validate()

        self.assertTrue(report.is_valid)
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)


class RepositoryMissingReferenceTests(
    RepositoryValidationFixtureTests
):
    """Tests covering broken canonical references."""

    def test_missing_requirement_is_error(self) -> None:
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=["REQ-MISSING"],
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.MISSING_REQUIREMENT
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].severity,
            ValidationSeverity.ERROR,
        )
        self.assertEqual(
            findings[0].entity_type,
            "Scenario",
        )
        self.assertEqual(
            findings[0].entity_id,
            "SCN-001",
        )
        self.assertEqual(
            findings[0].referenced_entity_type,
            "Requirement",
        )
        self.assertEqual(
            findings[0].referenced_entity_id,
            "REQ-MISSING",
        )

    def test_all_missing_requirements_are_reported(
        self,
    ) -> None:
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=[
                    "REQ-MISSING-001",
                    "REQ-MISSING-002",
                ],
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.MISSING_REQUIREMENT
        )

        self.assertEqual(len(findings), 2)
        self.assertEqual(
            tuple(
                finding.referenced_entity_id
                for finding in findings
            ),
            (
                "REQ-MISSING-001",
                "REQ-MISSING-002",
            ),
        )

    def test_existing_and_missing_requirement_are_distinguished(
        self,
    ) -> None:
        self.requirements.add(
            requirement("REQ-001")
        )
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=[
                    "REQ-001",
                    "REQ-MISSING",
                ],
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.MISSING_REQUIREMENT
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].referenced_entity_id,
            "REQ-MISSING",
        )

    def test_missing_scenario_is_error(self) -> None:
        self.test_definitions.add(
            manual_test_definition(
                "TEST-MANUAL-001",
                scenario_id="SCN-MISSING",
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.MISSING_SCENARIO
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].entity_type,
            "TestDefinition",
        )
        self.assertEqual(
            findings[0].entity_id,
            "TEST-MANUAL-001",
        )
        self.assertEqual(
            findings[0].referenced_entity_id,
            "SCN-MISSING",
        )

    def test_missing_test_definition_is_error(
        self,
    ) -> None:
        self.executions.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-MISSING",
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.MISSING_TEST_DEFINITION
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].entity_type,
            "Execution",
        )
        self.assertEqual(
            findings[0].entity_id,
            "EXEC-001",
        )
        self.assertEqual(
            findings[0].referenced_entity_id,
            "TEST-MISSING",
        )


class RepositoryRerunValidationTests(
    RepositoryValidationFixtureTests
):
    """Tests covering Execution rerun relationships."""

    def test_valid_rerun_has_no_rerun_error(self) -> None:
        self.requirements.add(
            requirement("REQ-001")
        )
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=["REQ-001"],
            )
        )
        self.test_definitions.add_many(
            [
                manual_test_definition(
                    "TEST-MANUAL-001",
                    scenario_id="SCN-001",
                ),
                automation_test_definition(
                    "TEST-AUTO-001",
                    scenario_id="SCN-001",
                ),
            ]
        )

        original = execution(
            "EXEC-001",
            test_definition_id="TEST-MANUAL-001",
            environment="SIT",
            status="FAILED",
        )
        rerun = execution(
            "EXEC-002",
            test_definition_id="TEST-MANUAL-001",
            environment="SIT",
            status="PASSED",
            started_at=BASE_TIME + timedelta(hours=1),
            completed_at=(
                BASE_TIME
                + timedelta(hours=1, minutes=5)
            ),
            rerun_of_execution_id="EXEC-001",
        )
        automation_result = execution(
            "EXEC-003",
            test_definition_id="TEST-AUTO-001",
        )

        self.executions.add_many(
            [
                original,
                rerun,
                automation_result,
            ]
        )

        report = self.validator.validate()

        rerun_error_codes = {
            ValidationCode.MISSING_RERUN_EXECUTION,
            ValidationCode.RERUN_TEST_DEFINITION_MISMATCH,
            ValidationCode.RERUN_ENVIRONMENT_MISMATCH,
        }

        self.assertFalse(
            any(
                finding.code in rerun_error_codes
                for finding in report.findings
            )
        )

    def test_missing_original_execution_is_error(
        self,
    ) -> None:
        self.executions.add(
            execution(
                "EXEC-002",
                rerun_of_execution_id="EXEC-MISSING",
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.MISSING_RERUN_EXECUTION
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].entity_id,
            "EXEC-002",
        )
        self.assertEqual(
            findings[0].referenced_entity_id,
            "EXEC-MISSING",
        )

    def test_rerun_test_definition_mismatch_is_error(
        self,
    ) -> None:
        self.executions.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-MANUAL-001",
                    status="FAILED",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-AUTO-001",
                    rerun_of_execution_id="EXEC-001",
                ),
            ]
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode
            .RERUN_TEST_DEFINITION_MISMATCH
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].entity_id,
            "EXEC-002",
        )
        self.assertEqual(
            findings[0].referenced_entity_id,
            "EXEC-001",
        )

    def test_rerun_environment_mismatch_is_error(
        self,
    ) -> None:
        self.executions.add_many(
            [
                execution(
                    "EXEC-001",
                    environment="SIT",
                    status="FAILED",
                ),
                execution(
                    "EXEC-002",
                    environment="UAT",
                    rerun_of_execution_id="EXEC-001",
                ),
            ]
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.RERUN_ENVIRONMENT_MISMATCH
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].entity_id,
            "EXEC-002",
        )

    def test_rerun_can_report_both_consistency_errors(
        self,
    ) -> None:
        self.executions.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-MANUAL-001",
                    environment="SIT",
                    status="FAILED",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-AUTO-001",
                    environment="UAT",
                    rerun_of_execution_id="EXEC-001",
                ),
            ]
        )

        report = self.validator.validate()

        self.assertTrue(
            report.has_code(
                ValidationCode
                .RERUN_TEST_DEFINITION_MISMATCH
            )
        )
        self.assertTrue(
            report.has_code(
                ValidationCode
                .RERUN_ENVIRONMENT_MISMATCH
            )
        )


class RepositoryGovernanceWarningTests(
    RepositoryValidationFixtureTests
):
    """Tests covering non-blocking governance findings."""

    def test_requirement_without_scenario_is_warning(
        self,
    ) -> None:
        self.requirements.add(
            requirement("REQ-001")
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.REQUIREMENT_WITHOUT_SCENARIO
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(report.error_count, 0)
        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].severity,
            ValidationSeverity.WARNING,
        )
        self.assertEqual(
            findings[0].entity_id,
            "REQ-001",
        )

    def test_scenario_without_test_definition_is_warning(
        self,
    ) -> None:
        self.requirements.add(
            requirement("REQ-001")
        )
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=["REQ-001"],
            )
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode
            .SCENARIO_WITHOUT_TEST_DEFINITION
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0].entity_id,
            "SCN-001",
        )

    def test_test_definition_without_execution_is_warning(
        self,
    ) -> None:
        self.requirements.add(
            requirement("REQ-001")
        )
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=["REQ-001"],
            )
        )
        self.test_definitions.add_many(
            [
                manual_test_definition(
                    "TEST-MANUAL-001",
                    scenario_id="SCN-001",
                ),
                automation_test_definition(
                    "TEST-AUTO-001",
                    scenario_id="SCN-001",
                ),
            ]
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode
            .TEST_DEFINITION_WITHOUT_EXECUTION
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(len(findings), 2)
        self.assertEqual(
            tuple(
                finding.entity_id
                for finding in findings
            ),
            (
                "TEST-AUTO-001",
                "TEST-MANUAL-001",
            ),
        )

    def test_warnings_do_not_make_report_invalid(
        self,
    ) -> None:
        self.requirements.add(
            requirement("REQ-001")
        )

        report = self.validator.validate()

        self.assertTrue(report.is_valid)
        self.assertGreater(report.warning_count, 0)
        self.assertEqual(report.error_count, 0)


class RepositoryCoverageGapTests(
    RepositoryValidationFixtureTests
):
    """Tests covering Manual and Automation coverage gaps."""

    def setUp(self) -> None:
        super().setUp()

        self.requirements.add(
            requirement("REQ-001")
        )
        self.scenarios.add(
            scenario(
                "SCN-001",
                requirement_ids=["REQ-001"],
            )
        )

    def test_manual_only_scenario_warns_about_automation(
        self,
    ) -> None:
        self.test_definitions.add(
            manual_test_definition(
                "TEST-MANUAL-001",
                scenario_id="SCN-001",
            )
        )
        self.executions.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-MANUAL-001",
            )
        )

        report = self.validator.validate()

        self.assertFalse(
            report.has_code(
                ValidationCode.SCENARIO_WITHOUT_MANUAL_TEST
            )
        )
        self.assertTrue(
            report.has_code(
                ValidationCode
                .SCENARIO_WITHOUT_AUTOMATION_TEST
            )
        )
        self.assertTrue(report.is_valid)

    def test_automation_only_scenario_warns_about_manual(
        self,
    ) -> None:
        self.test_definitions.add(
            automation_test_definition(
                "TEST-AUTO-001",
                scenario_id="SCN-001",
            )
        )
        self.executions.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-AUTO-001",
            )
        )

        report = self.validator.validate()

        self.assertTrue(
            report.has_code(
                ValidationCode.SCENARIO_WITHOUT_MANUAL_TEST
            )
        )
        self.assertFalse(
            report.has_code(
                ValidationCode
                .SCENARIO_WITHOUT_AUTOMATION_TEST
            )
        )
        self.assertTrue(report.is_valid)

    def test_manual_and_automation_have_no_coverage_gap(
        self,
    ) -> None:
        self.test_definitions.add_many(
            [
                manual_test_definition(
                    "TEST-MANUAL-001",
                    scenario_id="SCN-001",
                ),
                automation_test_definition(
                    "TEST-AUTO-001",
                    scenario_id="SCN-001",
                ),
            ]
        )
        self.executions.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id=(
                        "TEST-MANUAL-001"
                    ),
                ),
                execution(
                    "EXEC-002",
                    test_definition_id=(
                        "TEST-AUTO-001"
                    ),
                ),
            ]
        )

        report = self.validator.validate()

        self.assertFalse(
            report.has_code(
                ValidationCode.SCENARIO_WITHOUT_MANUAL_TEST
            )
        )
        self.assertFalse(
            report.has_code(
                ValidationCode
                .SCENARIO_WITHOUT_AUTOMATION_TEST
            )
        )

    def test_scenario_with_no_tests_does_not_duplicate_gap_warnings(
        self,
    ) -> None:
        report = self.validator.validate()

        self.assertTrue(
            report.has_code(
                ValidationCode
                .SCENARIO_WITHOUT_TEST_DEFINITION
            )
        )
        self.assertFalse(
            report.has_code(
                ValidationCode.SCENARIO_WITHOUT_MANUAL_TEST
            )
        )
        self.assertFalse(
            report.has_code(
                ValidationCode
                .SCENARIO_WITHOUT_AUTOMATION_TEST
            )
        )


class ValidationFindingTests(unittest.TestCase):
    """Tests covering the immutable finding model."""

    def test_finding_to_dict(self) -> None:
        finding = ValidationFinding(
            severity=ValidationSeverity.ERROR,
            code=ValidationCode.MISSING_REQUIREMENT,
            entity_type="Scenario",
            entity_id="SCN-001",
            message=(
                "Scenario references a missing Requirement."
            ),
            referenced_entity_type="Requirement",
            referenced_entity_id="REQ-MISSING",
        )

        self.assertEqual(
            finding.to_dict(),
            {
                "severity": "ERROR",
                "code": "MISSING_REQUIREMENT",
                "entity_type": "Scenario",
                "entity_id": "SCN-001",
                "message": (
                    "Scenario references a missing Requirement."
                ),
                "referenced_entity_type": "Requirement",
                "referenced_entity_id": "REQ-MISSING",
            },
        )

    def test_finding_without_reference_serializes_nulls(
        self,
    ) -> None:
        finding = ValidationFinding(
            severity=ValidationSeverity.WARNING,
            code=(
                ValidationCode
                .REQUIREMENT_WITHOUT_SCENARIO
            ),
            entity_type="Requirement",
            entity_id="REQ-001",
            message="Requirement has no Scenario.",
        )

        result = finding.to_dict()

        self.assertIsNone(
            result["referenced_entity_type"]
        )
        self.assertIsNone(
            result["referenced_entity_id"]
        )


class ValidationReportTests(unittest.TestCase):
    """Tests covering report properties and serialization."""

    def setUp(self) -> None:
        self.error = ValidationFinding(
            severity=ValidationSeverity.ERROR,
            code=ValidationCode.MISSING_SCENARIO,
            entity_type="TestDefinition",
            entity_id="TEST-001",
            message="Missing Scenario.",
            referenced_entity_type="Scenario",
            referenced_entity_id="SCN-MISSING",
        )

        self.warning = ValidationFinding(
            severity=ValidationSeverity.WARNING,
            code=(
                ValidationCode
                .TEST_DEFINITION_WITHOUT_EXECUTION
            ),
            entity_type="TestDefinition",
            entity_id="TEST-002",
            message="No Execution exists.",
        )

        self.report = ValidationReport(
            findings=(
                self.error,
                self.warning,
            )
        )

    def test_errors_property(self) -> None:
        self.assertEqual(
            self.report.errors,
            (self.error,),
        )

    def test_warnings_property(self) -> None:
        self.assertEqual(
            self.report.warnings,
            (self.warning,),
        )

    def test_report_with_error_is_invalid(self) -> None:
        self.assertFalse(self.report.is_valid)

    def test_report_counts(self) -> None:
        self.assertEqual(self.report.error_count, 1)
        self.assertEqual(self.report.warning_count, 1)

    def test_has_code(self) -> None:
        self.assertTrue(
            self.report.has_code(
                ValidationCode.MISSING_SCENARIO
            )
        )
        self.assertFalse(
            self.report.has_code(
                ValidationCode.MISSING_REQUIREMENT
            )
        )

    def test_findings_by_code(self) -> None:
        self.assertEqual(
            self.report.findings_by_code(
                ValidationCode.MISSING_SCENARIO
            ),
            (self.error,),
        )

    def test_report_to_dict(self) -> None:
        result = self.report.to_dict()

        self.assertEqual(
            result["is_valid"],
            False,
        )
        self.assertEqual(
            result["error_count"],
            1,
        )
        self.assertEqual(
            result["warning_count"],
            1,
        )
        self.assertEqual(
            result["findings"],
            [
                self.error.to_dict(),
                self.warning.to_dict(),
            ],
        )

    def test_warning_only_report_is_valid(self) -> None:
        report = ValidationReport(
            findings=(self.warning,)
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 1)


class ValidationFindingSortingTests(
    RepositoryValidationFixtureTests
):
    """Tests covering deterministic finding ordering."""

    def test_errors_are_sorted_before_warnings(
        self,
    ) -> None:
        self.requirements.add(
            requirement("REQ-ORPHAN")
        )

        self.test_definitions.add(
            manual_test_definition(
                "TEST-001",
                scenario_id="SCN-MISSING",
            )
        )

        report = self.validator.validate()

        severities = [
            finding.severity
            for finding in report.findings
        ]

        first_warning_index = severities.index(
            ValidationSeverity.WARNING
        )

        self.assertTrue(
            all(
                severity is ValidationSeverity.ERROR
                for severity in severities[
                    :first_warning_index
                ]
            )
        )
        self.assertTrue(
            all(
                severity is ValidationSeverity.WARNING
                for severity in severities[
                    first_warning_index:
                ]
            )
        )

    def test_findings_are_sorted_by_code_within_severity(
        self,
    ) -> None:
        self.executions.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-MISSING",
                rerun_of_execution_id="EXEC-MISSING",
            )
        )

        report = self.validator.validate()

        error_codes = [
            finding.code.value
            for finding in report.errors
        ]

        self.assertEqual(
            error_codes,
            sorted(error_codes),
        )

    def test_same_code_findings_are_sorted_by_entity_id(
        self,
    ) -> None:
        self.requirements.add_many(
            [
                requirement("REQ-003"),
                requirement("REQ-001"),
                requirement("REQ-002"),
            ]
        )

        report = self.validator.validate()

        findings = report.findings_by_code(
            ValidationCode.REQUIREMENT_WITHOUT_SCENARIO
        )

        self.assertEqual(
            tuple(
                finding.entity_id
                for finding in findings
            ),
            (
                "REQ-001",
                "REQ-002",
                "REQ-003",
            ),
        )


if __name__ == "__main__":
    unittest.main()
