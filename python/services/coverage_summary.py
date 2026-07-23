"""Manual and Automation test coverage reporting services.

Purpose
-------
Transforms canonical Scenario and TestDefinition repositories into
dashboard-ready coverage and automation-readiness metrics.

Coverage definitions
--------------------
Scenario coverage:
    A Scenario is covered when at least one eligible Test Definition
    references it.

Manual coverage:
    A Scenario has at least one eligible MANUAL Test Definition.

Automation coverage:
    A Scenario has at least one eligible AUTOMATION Test Definition.

Dual coverage:
    A Scenario has both Manual and Automation Test Definitions.

Automation pipeline backlog:
    An Automation Test Definition without a pipeline_name.

Automation repository backlog:
    An Automation Test Definition without a repository.

Active-only policy
------------------
By default, reporting includes:

- active Scenarios
- ACTIVE Test Definitions

Governance consumers may set active_only=False to include inactive
Scenarios and Test Definitions in all lifecycle states.
"""

from __future__ import annotations

from dataclasses import dataclass

from canonical.enums import (
    AutomationFramework,
    TestDefinitionStatus,
    TestType,
)
from canonical.scenario import Scenario
from canonical.test_definition import TestDefinition
from repositories.base import RepositoryValidationError
from repositories.scenario_repository import ScenarioRepository
from repositories.test_definition_repository import (
    TestDefinitionRepository,
)


@dataclass(frozen=True, slots=True)
class FrameworkCoverage:
    """Automation Test Definition count for one framework."""

    framework: AutomationFramework
    test_definition_count: int

    def __post_init__(self) -> None:
        """Validate framework coverage values."""
        if not isinstance(
            self.framework,
            AutomationFramework,
        ):
            raise RepositoryValidationError(
                "framework must be an AutomationFramework."
            )

        if type(self.test_definition_count) is not int:
            raise RepositoryValidationError(
                "test_definition_count must be an integer."
            )

        if self.test_definition_count < 0:
            raise RepositoryValidationError(
                "test_definition_count must not be negative."
            )

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible framework coverage data."""
        return {
            "framework": self.framework.value,
            "test_definition_count": (
                self.test_definition_count
            ),
        }


@dataclass(frozen=True, slots=True)
class TestCoverageSummary:
    """Immutable Manual and Automation coverage summary."""

    active_only: bool

    total_scenarios: int
    covered_scenarios: int
    uncovered_scenarios: int

    manual_covered_scenarios: int
    automation_covered_scenarios: int
    dual_covered_scenarios: int
    manual_only_scenarios: int
    automation_only_scenarios: int

    total_test_definitions: int
    manual_test_definitions: int
    automation_test_definitions: int

    automation_with_repository: int
    automation_without_repository: int
    automation_with_pipeline: int
    automation_without_pipeline: int

    scenario_coverage_percentage: float
    manual_coverage_percentage: float
    automation_coverage_percentage: float
    dual_coverage_percentage: float
    automation_pipeline_readiness_percentage: float
    automation_repository_readiness_percentage: float

    framework_coverage: tuple[FrameworkCoverage, ...]

    uncovered_scenario_ids: tuple[str, ...]
    manual_only_scenario_ids: tuple[str, ...]
    automation_only_scenario_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate internal summary consistency."""
        if type(self.active_only) is not bool:
            raise RepositoryValidationError(
                "active_only must be a Boolean value."
            )

        count_fields = {
            "total_scenarios": self.total_scenarios,
            "covered_scenarios": self.covered_scenarios,
            "uncovered_scenarios": self.uncovered_scenarios,
            "manual_covered_scenarios": (
                self.manual_covered_scenarios
            ),
            "automation_covered_scenarios": (
                self.automation_covered_scenarios
            ),
            "dual_covered_scenarios": (
                self.dual_covered_scenarios
            ),
            "manual_only_scenarios": (
                self.manual_only_scenarios
            ),
            "automation_only_scenarios": (
                self.automation_only_scenarios
            ),
            "total_test_definitions": (
                self.total_test_definitions
            ),
            "manual_test_definitions": (
                self.manual_test_definitions
            ),
            "automation_test_definitions": (
                self.automation_test_definitions
            ),
            "automation_with_repository": (
                self.automation_with_repository
            ),
            "automation_without_repository": (
                self.automation_without_repository
            ),
            "automation_with_pipeline": (
                self.automation_with_pipeline
            ),
            "automation_without_pipeline": (
                self.automation_without_pipeline
            ),
        }

        for field_name, value in count_fields.items():
            if type(value) is not int:
                raise RepositoryValidationError(
                    f"{field_name} must be an integer."
                )

            if value < 0:
                raise RepositoryValidationError(
                    f"{field_name} must not be negative."
                )

        if (
            self.covered_scenarios
            + self.uncovered_scenarios
            != self.total_scenarios
        ):
            raise RepositoryValidationError(
                "Covered and uncovered Scenario counts "
                "must equal total_scenarios."
            )

        if (
            self.dual_covered_scenarios
            + self.manual_only_scenarios
            + self.automation_only_scenarios
            != self.covered_scenarios
        ):
            raise RepositoryValidationError(
                "Scenario coverage categories must equal "
                "covered_scenarios."
            )

        if (
            self.manual_only_scenarios
            + self.dual_covered_scenarios
            != self.manual_covered_scenarios
        ):
            raise RepositoryValidationError(
                "Manual Scenario coverage counts are inconsistent."
            )

        if (
            self.automation_only_scenarios
            + self.dual_covered_scenarios
            != self.automation_covered_scenarios
        ):
            raise RepositoryValidationError(
                "Automation Scenario coverage counts "
                "are inconsistent."
            )

        if (
            self.manual_test_definitions
            + self.automation_test_definitions
            != self.total_test_definitions
        ):
            raise RepositoryValidationError(
                "Manual and Automation Test Definition counts "
                "must equal total_test_definitions."
            )

        if (
            self.automation_with_repository
            + self.automation_without_repository
            != self.automation_test_definitions
        ):
            raise RepositoryValidationError(
                "Automation repository-readiness counts "
                "are inconsistent."
            )

        if (
            self.automation_with_pipeline
            + self.automation_without_pipeline
            != self.automation_test_definitions
        ):
            raise RepositoryValidationError(
                "Automation pipeline-readiness counts "
                "are inconsistent."
            )

        percentage_fields = {
            "scenario_coverage_percentage": (
                self.scenario_coverage_percentage
            ),
            "manual_coverage_percentage": (
                self.manual_coverage_percentage
            ),
            "automation_coverage_percentage": (
                self.automation_coverage_percentage
            ),
            "dual_coverage_percentage": (
                self.dual_coverage_percentage
            ),
            "automation_pipeline_readiness_percentage": (
                self
                .automation_pipeline_readiness_percentage
            ),
            "automation_repository_readiness_percentage": (
                self
                .automation_repository_readiness_percentage
            ),
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

        identifier_collections = {
            "uncovered_scenario_ids": (
                self.uncovered_scenario_ids
            ),
            "manual_only_scenario_ids": (
                self.manual_only_scenario_ids
            ),
            "automation_only_scenario_ids": (
                self.automation_only_scenario_ids
            ),
        }

        for field_name, identifiers in (
            identifier_collections.items()
        ):
            if not isinstance(identifiers, tuple):
                raise RepositoryValidationError(
                    f"{field_name} must be a tuple."
                )

            if any(
                not isinstance(identifier, str)
                or not identifier
                for identifier in identifiers
            ):
                raise RepositoryValidationError(
                    f"{field_name} must contain "
                    "non-empty strings."
                )

            if tuple(sorted(identifiers)) != identifiers:
                raise RepositoryValidationError(
                    f"{field_name} must be sorted."
                )

    @property
    def has_full_scenario_coverage(self) -> bool:
        """Return whether every Scenario has a test definition."""
        return (
            self.total_scenarios > 0
            and self.uncovered_scenarios == 0
        )

    @property
    def has_full_manual_coverage(self) -> bool:
        """Return whether every Scenario has Manual coverage."""
        return (
            self.total_scenarios > 0
            and self.manual_covered_scenarios
            == self.total_scenarios
        )

    @property
    def has_full_automation_coverage(self) -> bool:
        """Return whether every Scenario has Automation coverage."""
        return (
            self.total_scenarios > 0
            and self.automation_covered_scenarios
            == self.total_scenarios
        )

    @property
    def automation_backlog(self) -> int:
        """Return Scenarios covered manually but not automatically."""
        return self.manual_only_scenarios

    @property
    def is_empty(self) -> bool:
        """Return whether no Scenarios are in reporting scope."""
        return self.total_scenarios == 0

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible coverage summary data."""
        return {
            "active_only": self.active_only,
            "total_scenarios": self.total_scenarios,
            "covered_scenarios": self.covered_scenarios,
            "uncovered_scenarios": self.uncovered_scenarios,
            "manual_covered_scenarios": (
                self.manual_covered_scenarios
            ),
            "automation_covered_scenarios": (
                self.automation_covered_scenarios
            ),
            "dual_covered_scenarios": (
                self.dual_covered_scenarios
            ),
            "manual_only_scenarios": (
                self.manual_only_scenarios
            ),
            "automation_only_scenarios": (
                self.automation_only_scenarios
            ),
            "automation_backlog": self.automation_backlog,
            "total_test_definitions": (
                self.total_test_definitions
            ),
            "manual_test_definitions": (
                self.manual_test_definitions
            ),
            "automation_test_definitions": (
                self.automation_test_definitions
            ),
            "automation_with_repository": (
                self.automation_with_repository
            ),
            "automation_without_repository": (
                self.automation_without_repository
            ),
            "automation_with_pipeline": (
                self.automation_with_pipeline
            ),
            "automation_without_pipeline": (
                self.automation_without_pipeline
            ),
            "scenario_coverage_percentage": (
                self.scenario_coverage_percentage
            ),
            "manual_coverage_percentage": (
                self.manual_coverage_percentage
            ),
            "automation_coverage_percentage": (
                self.automation_coverage_percentage
            ),
            "dual_coverage_percentage": (
                self.dual_coverage_percentage
            ),
            "automation_pipeline_readiness_percentage": (
                self
                .automation_pipeline_readiness_percentage
            ),
            "automation_repository_readiness_percentage": (
                self
                .automation_repository_readiness_percentage
            ),
            "framework_coverage": [
                item.to_dict()
                for item in self.framework_coverage
            ],
            "uncovered_scenario_ids": list(
                self.uncovered_scenario_ids
            ),
            "manual_only_scenario_ids": list(
                self.manual_only_scenario_ids
            ),
            "automation_only_scenario_ids": list(
                self.automation_only_scenario_ids
            ),
            "has_full_scenario_coverage": (
                self.has_full_scenario_coverage
            ),
            "has_full_manual_coverage": (
                self.has_full_manual_coverage
            ),
            "has_full_automation_coverage": (
                self.has_full_automation_coverage
            ),
            "is_empty": self.is_empty,
        }


class CoverageSummaryService:
    """Calculate Manual and Automation test coverage metrics."""

    def __init__(
        self,
        scenario_repository: ScenarioRepository,
        test_definition_repository: TestDefinitionRepository,
    ) -> None:
        """Store canonical repository dependencies."""
        if not isinstance(
            scenario_repository,
            ScenarioRepository,
        ):
            raise RepositoryValidationError(
                "scenario_repository must be a "
                "ScenarioRepository."
            )

        if not isinstance(
            test_definition_repository,
            TestDefinitionRepository,
        ):
            raise RepositoryValidationError(
                "test_definition_repository must be a "
                "TestDefinitionRepository."
            )

        self.scenarios = scenario_repository
        self.test_definitions = test_definition_repository

    def summarize(
        self,
        *,
        active_only: bool = True,
    ) -> TestCoverageSummary:
        """Return an overall coverage and readiness summary."""
        self._validate_active_only(active_only)

        scenarios = self._eligible_scenarios(
            active_only=active_only
        )
        test_definitions = self._eligible_test_definitions(
            active_only=active_only
        )

        scenario_ids = {
            scenario.scenario_id
            for scenario in scenarios
        }

        relevant_test_definitions = tuple(
            test_definition
            for test_definition in test_definitions
            if test_definition.scenario_id in scenario_ids
        )

        definitions_by_scenario = (
            self._group_by_scenario(
                relevant_test_definitions
            )
        )

        manual_covered_ids: set[str] = set()
        automation_covered_ids: set[str] = set()

        for scenario in scenarios:
            scenario_tests = definitions_by_scenario.get(
                scenario.scenario_id,
                (),
            )

            test_types = {
                test_definition.test_type
                for test_definition in scenario_tests
            }

            if TestType.MANUAL in test_types:
                manual_covered_ids.add(
                    scenario.scenario_id
                )

            if TestType.AUTOMATION in test_types:
                automation_covered_ids.add(
                    scenario.scenario_id
                )

        covered_ids = (
            manual_covered_ids
            | automation_covered_ids
        )
        dual_covered_ids = (
            manual_covered_ids
            & automation_covered_ids
        )
        manual_only_ids = (
            manual_covered_ids
            - automation_covered_ids
        )
        automation_only_ids = (
            automation_covered_ids
            - manual_covered_ids
        )
        uncovered_ids = scenario_ids - covered_ids

        manual_definitions = tuple(
            test_definition
            for test_definition
            in relevant_test_definitions
            if test_definition.test_type
            is TestType.MANUAL
        )
        automation_definitions = tuple(
            test_definition
            for test_definition
            in relevant_test_definitions
            if test_definition.test_type
            is TestType.AUTOMATION
        )

        automation_with_repository = sum(
            test_definition.repository is not None
            for test_definition in automation_definitions
        )
        automation_with_pipeline = sum(
            test_definition.pipeline_name is not None
            for test_definition in automation_definitions
        )

        framework_coverage = (
            self._build_framework_coverage(
                automation_definitions
            )
        )

        total_scenarios = len(scenarios)
        automation_total = len(automation_definitions)

        return TestCoverageSummary(
            active_only=active_only,
            total_scenarios=total_scenarios,
            covered_scenarios=len(covered_ids),
            uncovered_scenarios=len(uncovered_ids),
            manual_covered_scenarios=len(
                manual_covered_ids
            ),
            automation_covered_scenarios=len(
                automation_covered_ids
            ),
            dual_covered_scenarios=len(
                dual_covered_ids
            ),
            manual_only_scenarios=len(
                manual_only_ids
            ),
            automation_only_scenarios=len(
                automation_only_ids
            ),
            total_test_definitions=len(
                relevant_test_definitions
            ),
            manual_test_definitions=len(
                manual_definitions
            ),
            automation_test_definitions=automation_total,
            automation_with_repository=(
                automation_with_repository
            ),
            automation_without_repository=(
                automation_total
                - automation_with_repository
            ),
            automation_with_pipeline=(
                automation_with_pipeline
            ),
            automation_without_pipeline=(
                automation_total
                - automation_with_pipeline
            ),
            scenario_coverage_percentage=(
                self._percentage(
                    len(covered_ids),
                    total_scenarios,
                )
            ),
            manual_coverage_percentage=(
                self._percentage(
                    len(manual_covered_ids),
                    total_scenarios,
                )
            ),
            automation_coverage_percentage=(
                self._percentage(
                    len(automation_covered_ids),
                    total_scenarios,
                )
            ),
            dual_coverage_percentage=(
                self._percentage(
                    len(dual_covered_ids),
                    total_scenarios,
                )
            ),
            automation_pipeline_readiness_percentage=(
                self._percentage(
                    automation_with_pipeline,
                    automation_total,
                )
            ),
            automation_repository_readiness_percentage=(
                self._percentage(
                    automation_with_repository,
                    automation_total,
                )
            ),
            framework_coverage=framework_coverage,
            uncovered_scenario_ids=tuple(
                sorted(uncovered_ids)
            ),
            manual_only_scenario_ids=tuple(
                sorted(manual_only_ids)
            ),
            automation_only_scenario_ids=tuple(
                sorted(automation_only_ids)
            ),
        )

    def summarize_by_feature(
        self,
        *,
        active_only: bool = True,
    ) -> dict[str, TestCoverageSummary]:
        """Return one coverage summary for each Scenario feature."""
        self._validate_active_only(active_only)

        scenarios = self._eligible_scenarios(
            active_only=active_only
        )

        feature_ids = sorted(
            {
                scenario.feature_id
                for scenario in scenarios
            }
        )

        return {
            feature_id: self._summarize_scenario_subset(
                tuple(
                    scenario
                    for scenario in scenarios
                    if scenario.feature_id
                    == feature_id
                ),
                active_only=active_only,
            )
            for feature_id in feature_ids
        }

    def summarize_for_scenario_ids(
        self,
        scenario_ids: tuple[str, ...] | list[str],
        *,
        active_only: bool = True,
    ) -> TestCoverageSummary:
        """Return coverage for a requested Scenario subset."""
        self._validate_active_only(active_only)

        normalized_ids = self._normalize_scenario_ids(
            scenario_ids
        )

        eligible_scenarios = self._eligible_scenarios(
            active_only=active_only
        )

        requested_ids = set(normalized_ids)

        selected_scenarios = tuple(
            scenario
            for scenario in eligible_scenarios
            if scenario.scenario_id in requested_ids
        )

        return self._summarize_scenario_subset(
            selected_scenarios,
            active_only=active_only,
        )

    def _summarize_scenario_subset(
        self,
        scenarios: tuple[Scenario, ...],
        *,
        active_only: bool,
    ) -> TestCoverageSummary:
        """Build coverage for a supplied Scenario subset."""
        temporary_repository = ScenarioRepository()
        temporary_repository.add_many(scenarios)

        service = CoverageSummaryService(
            scenario_repository=temporary_repository,
            test_definition_repository=(
                self.test_definitions
            ),
        )

        return service.summarize(
            active_only=active_only
        )

    def _eligible_scenarios(
        self,
        *,
        active_only: bool,
    ) -> tuple[Scenario, ...]:
        """Return Scenarios eligible for reporting."""
        if active_only:
            return self.scenarios.find_active(True)

        return self.scenarios.list_all()

    def _eligible_test_definitions(
        self,
        *,
        active_only: bool,
    ) -> tuple[TestDefinition, ...]:
        """Return Test Definitions eligible for reporting."""
        if active_only:
            return self.test_definitions.find_by_status(
                TestDefinitionStatus.ACTIVE
            )

        return self.test_definitions.list_all()

    @staticmethod
    def _group_by_scenario(
        test_definitions: tuple[TestDefinition, ...],
    ) -> dict[str, tuple[TestDefinition, ...]]:
        """Group Test Definitions by Scenario identifier."""
        grouped_lists: dict[
            str,
            list[TestDefinition],
        ] = {}

        for test_definition in test_definitions:
            grouped_lists.setdefault(
                test_definition.scenario_id,
                [],
            ).append(test_definition)

        return {
            scenario_id: tuple(
                sorted(
                    definitions,
                    key=lambda item: (
                        item.test_type.value,
                        item.test_definition_id,
                    ),
                )
            )
            for scenario_id, definitions
            in grouped_lists.items()
        }

    @staticmethod
    def _build_framework_coverage(
        automation_definitions: tuple[
            TestDefinition,
            ...
        ],
    ) -> tuple[FrameworkCoverage, ...]:
        """Return Automation Definition counts by framework."""
        counts: dict[AutomationFramework, int] = {}

        for test_definition in automation_definitions:
            if test_definition.framework is None:
                continue

            counts[test_definition.framework] = (
                counts.get(
                    test_definition.framework,
                    0,
                )
                + 1
            )

        return tuple(
            FrameworkCoverage(
                framework=framework,
                test_definition_count=counts[framework],
            )
            for framework in sorted(
                counts,
                key=lambda item: item.value,
            )
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
    def _validate_active_only(
        active_only: object,
    ) -> None:
        """Validate the active-only reporting policy."""
        if type(active_only) is not bool:
            raise RepositoryValidationError(
                "active_only must be a Boolean value."
            )

    @staticmethod
    def _normalize_scenario_ids(
        scenario_ids: object,
    ) -> tuple[str, ...]:
        """Validate and normalize requested Scenario IDs."""
        if isinstance(scenario_ids, (str, bytes)):
            raise RepositoryValidationError(
                "scenario_ids must be a collection of strings."
            )

        try:
            raw_ids = list(scenario_ids)
        except TypeError as exc:
            raise RepositoryValidationError(
                "scenario_ids must be a collection of strings."
            ) from exc

        normalized_ids: list[str] = []
        seen_ids: set[str] = set()

        for index, raw_id in enumerate(raw_ids):
            if not isinstance(raw_id, str):
                raise RepositoryValidationError(
                    f"scenario_ids[{index}] must be a string."
                )

            normalized_id = raw_id.strip()

            if not normalized_id:
                raise RepositoryValidationError(
                    f"scenario_ids[{index}] must not be empty."
                )

            if normalized_id not in seen_ids:
                seen_ids.add(normalized_id)
                normalized_ids.append(normalized_id)

        if not normalized_ids:
            raise RepositoryValidationError(
                "scenario_ids must contain at least one ID."
            )

        return tuple(normalized_ids)
