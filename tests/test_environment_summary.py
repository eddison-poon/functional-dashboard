
"""Unit tests for environment readiness reporting."""

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from canonical.enums import Environment  # noqa: E402
from canonical.execution import Execution  # noqa: E402
from repositories.base import (  # noqa: E402
    RepositoryValidationError,
)
from repositories.execution_repository import (  # noqa: E402
    ExecutionRepository,
)
from services.environment_summary import (  # noqa: E402
    EnvironmentReadinessService,
    EnvironmentReadinessStatus,
    EnvironmentReadinessSummary,
    ReadinessColour,
)
from services.execution_selection import (  # noqa: E402
    ExecutionSelectionService,
)
from services.execution_summary import (  # noqa: E402
    ExecutionSummary,
    ExecutionSummaryService,
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


def execution(
    execution_id: str,
    *,
    test_definition_id: str,
    environment: Environment | str = "SIT",
    status: str = "PASSED",
    execution_cycle: str | None = "SIT Cycle 1",
    build_version: str | None = "1.0.0",
    started_at: datetime | None = BASE_TIME,
    completed_at: datetime | None = (
        BASE_TIME + timedelta(minutes=5)
    ),
    rerun_of_execution_id: str | None = None,
) -> Execution:
    """Create a valid canonical Execution."""
    if status == "NOT_EXECUTED":
        started_at = None
        completed_at = None

    elif status == "IN_PROGRESS":
        completed_at = None

    return Execution(
        execution_id=execution_id,
        test_definition_id=test_definition_id,
        environment=environment,
        status=status,
        execution_cycle=execution_cycle,
        started_at=started_at,
        completed_at=completed_at,
        executed_by=(
            None
            if status == "NOT_EXECUTED"
            else "QA User"
        ),
        build_version=build_version,
        rerun_of_execution_id=rerun_of_execution_id,
    )


def empty_execution_summary(
    environment: Environment = Environment.SIT,
) -> ExecutionSummary:
    """Return an empty environment execution summary."""
    return ExecutionSummary(
        environment=environment,
        execution_cycle=None,
        total=0,
        executed=0,
        terminal=0,
        passed=0,
        failed=0,
        blocked=0,
        skipped=0,
        aborted=0,
        in_progress=0,
        not_executed=0,
        execution_percentage=0.0,
        completion_percentage=0.0,
        pass_rate=0.0,
        failure_rate=0.0,
        blocked_rate=0.0,
    )


class EnvironmentReadinessSummaryModelTests(
    unittest.TestCase
):
    """Tests covering readiness summary properties."""

    def valid_summary(
        self,
    ) -> EnvironmentReadinessSummary:
        """Return a valid NOT_READY summary."""
        return EnvironmentReadinessSummary(
            environment=Environment.SIT,
            readiness=(
                EnvironmentReadinessStatus.NOT_READY
            ),
            colour=ReadinessColour.RED,
            execution_cycle=None,
            build_versions=(),
            execution_summary=(
                empty_execution_summary()
            ),
            rationale=(
                "No execution data is available.",
            ),
            recommended_actions=(
                "Prepare the environment.",
            ),
        )

    def test_not_ready_properties(self) -> None:
        summary = self.valid_summary()

        self.assertFalse(summary.is_ready)
        self.assertFalse(summary.has_execution_data)
        self.assertIsNone(
            summary.primary_build_version
        )
        self.assertFalse(
            summary.has_mixed_build_versions
        )

    def test_single_build_is_primary_build(self) -> None:
        summary = self.valid_summary()

        values = {
            field_name: getattr(summary, field_name)
            for field_name
            in summary.__dataclass_fields__
        }
        values["build_versions"] = ("1.0.0",)

        updated = EnvironmentReadinessSummary(
            **values
        )

        self.assertEqual(
            updated.primary_build_version,
            "1.0.0",
        )

    def test_multiple_builds_are_identified(self) -> None:
        summary = self.valid_summary()

        values = {
            field_name: getattr(summary, field_name)
            for field_name
            in summary.__dataclass_fields__
        }
        values["build_versions"] = (
            "1.0.0",
            "1.0.1",
        )

        updated = EnvironmentReadinessSummary(
            **values
        )

        self.assertTrue(
            updated.has_mixed_build_versions
        )
        self.assertIsNone(
            updated.primary_build_version
        )

    def test_colour_must_match_readiness(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            EnvironmentReadinessSummary(
                environment=Environment.SIT,
                readiness=(
                    EnvironmentReadinessStatus.READY
                ),
                colour=ReadinessColour.RED,
                execution_cycle=None,
                build_versions=(),
                execution_summary=(
                    empty_execution_summary()
                ),
                rationale=("Ready.",),
                recommended_actions=(),
            )

    def test_build_versions_must_be_sorted(
        self,
    ) -> None:
        summary = self.valid_summary()

        values = {
            field_name: getattr(summary, field_name)
            for field_name
            in summary.__dataclass_fields__
        }
        values["build_versions"] = (
            "1.0.1",
            "1.0.0",
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            EnvironmentReadinessSummary(**values)

    def test_to_dict(self) -> None:
        result = self.valid_summary().to_dict()

        self.assertEqual(result["environment"], "SIT")
        self.assertEqual(
            result["readiness"],
            "NOT_READY",
        )
        self.assertEqual(result["colour"], "RED")
        self.assertIn(
            "execution_summary",
            result,
        )


class EnvironmentReadinessServiceValidationTests(
    unittest.TestCase
):
    """Tests covering dependency and input validation."""

    def setUp(self) -> None:
        self.repository = ExecutionRepository()
        self.selection = ExecutionSelectionService(
            self.repository
        )
        self.execution_summaries = (
            ExecutionSummaryService(
                self.selection
            )
        )

    def test_selection_service_is_required(
        self,
    ) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            EnvironmentReadinessService(  # type: ignore[arg-type]
                execution_selection_service={},
                execution_summary_service=(
                    self.execution_summaries
                ),
            )

    def test_summary_service_is_required(self) -> None:
        with self.assertRaises(
            RepositoryValidationError
        ):
            EnvironmentReadinessService(  # type: ignore[arg-type]
                execution_selection_service=(
                    self.selection
                ),
                execution_summary_service={},
            )

    def test_invalid_environment_is_rejected(
        self,
    ) -> None:
        service = EnvironmentReadinessService(
            self.selection,
            self.execution_summaries,
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            service.summarize("LOCAL")

    def test_blank_cycle_is_rejected(self) -> None:
        service = EnvironmentReadinessService(
            self.selection,
            self.execution_summaries,
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            service.summarize(
                "SIT",
                execution_cycle=" ",
            )

    def test_environment_collection_is_required(
        self,
    ) -> None:
        service = EnvironmentReadinessService(
            self.selection,
            self.execution_summaries,
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            service.summarize_all(
                environments="SIT"
            )

    def test_empty_environment_collection_is_rejected(
        self,
    ) -> None:
        service = EnvironmentReadinessService(
            self.selection,
            self.execution_summaries,
        )

        with self.assertRaises(
            RepositoryValidationError
        ):
            service.summarize_all(
                environments=[]
            )


class EnvironmentReadinessFixtureTests(
    unittest.TestCase
):
    """Shared readiness-service fixture."""

    def setUp(self) -> None:
        self.repository = ExecutionRepository()
        self.selection = ExecutionSelectionService(
            self.repository
        )
        self.execution_summaries = (
            ExecutionSummaryService(
                self.selection
            )
        )
        self.service = EnvironmentReadinessService(
            self.selection,
            self.execution_summaries,
        )


class EnvironmentReadyTests(
    EnvironmentReadinessFixtureTests
):
    """Tests covering fully ready environments."""

    def test_complete_passing_environment_is_ready(
        self,
    ) -> None:
        self.repository.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-001",
                    status="PASSED",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-002",
                    status="PASSED",
                ),
            ]
        )

        summary = self.service.summarize(
            "SIT",
            execution_cycle="SIT Cycle 1",
        )

        self.assertEqual(
            summary.readiness,
            EnvironmentReadinessStatus.READY,
        )
        self.assertEqual(
            summary.colour,
            ReadinessColour.GREEN,
        )
        self.assertTrue(summary.is_ready)
        self.assertEqual(
            summary.primary_build_version,
            "1.0.0",
        )
        self.assertEqual(
            summary.execution_summary
            .completion_percentage,
            100.0,
        )

    def test_skipped_result_does_not_block_ready(
        self,
    ) -> None:
        self.repository.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-001",
                    status="PASSED",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-002",
                    status="SKIPPED",
                ),
            ]
        )

        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            EnvironmentReadinessStatus.READY,
        )


class EnvironmentPartiallyReadyTests(
    EnvironmentReadinessFixtureTests
):
    """Tests covering Amber readiness conditions."""

    def test_failed_test_produces_partial_readiness(
        self,
    ) -> None:
        self.repository.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-001",
                    status="PASSED",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-002",
                    status="FAILED",
                ),
            ]
        )

        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            (
                EnvironmentReadinessStatus
                .PARTIALLY_READY
            ),
        )
        self.assertEqual(
            summary.colour,
            ReadinessColour.AMBER,
        )
        self.assertTrue(
            any(
                "failed" in item.lower()
                for item in summary.rationale
            )
        )
        self.assertTrue(
            any(
                "triage" in item.lower()
                for item
                in summary.recommended_actions
            )
        )

    def test_blocked_test_produces_partial_readiness(
        self,
    ) -> None:
        self.repository.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-001",
                status="BLOCKED",
            )
        )

        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            (
                EnvironmentReadinessStatus
                .PARTIALLY_READY
            ),
        )

    def test_in_progress_test_produces_partial_readiness(
        self,
    ) -> None:
        self.repository.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-001",
                status="IN_PROGRESS",
            )
        )

        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            (
                EnvironmentReadinessStatus
                .PARTIALLY_READY
            ),
        )
        self.assertEqual(
            summary.execution_summary
            .completion_percentage,
            0.0,
        )

    def test_not_executed_test_produces_partial_readiness(
        self,
    ) -> None:
        self.repository.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-001",
                status="NOT_EXECUTED",
            )
        )

        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            (
                EnvironmentReadinessStatus
                .PARTIALLY_READY
            ),
        )

    def test_multiple_builds_produce_warning_and_action(
        self,
    ) -> None:
        self.repository.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-001",
                    build_version="1.0.0",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-002",
                    build_version="1.0.1",
                ),
            ]
        )

        summary = self.service.summarize("SIT")

        self.assertTrue(
            summary.has_mixed_build_versions
        )
        self.assertTrue(
            any(
                "multiple build" in item.lower()
                for item in summary.rationale
            )
        )
        self.assertTrue(
            any(
                "one intended build" in item.lower()
                for item
                in summary.recommended_actions
            )
        )


class EnvironmentNotReadyTests(
    EnvironmentReadinessFixtureTests
):
    """Tests covering missing execution data."""

    def test_no_data_is_not_ready(self) -> None:
        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            EnvironmentReadinessStatus.NOT_READY,
        )
        self.assertEqual(
            summary.colour,
            ReadinessColour.RED,
        )
        self.assertEqual(
            summary.execution_summary.total,
            0,
        )
        self.assertFalse(
            summary.has_execution_data
        )
        self.assertGreaterEqual(
            len(summary.recommended_actions),
            1,
        )

    def test_missing_cycle_is_not_ready(self) -> None:
        self.repository.add(
            execution(
                "EXEC-001",
                test_definition_id="TEST-001",
                execution_cycle="SIT Cycle 1",
            )
        )

        summary = self.service.summarize(
            "SIT",
            execution_cycle="SIT Cycle 2",
        )

        self.assertEqual(
            summary.readiness,
            EnvironmentReadinessStatus.NOT_READY,
        )


class EnvironmentSelectionTests(
    EnvironmentReadinessFixtureTests
):
    """Tests covering representative-execution behaviour."""

    def test_successful_rerun_replaces_failure(
        self,
    ) -> None:
        self.repository.add_many(
            [
                execution(
                    "EXEC-001",
                    test_definition_id="TEST-001",
                    status="FAILED",
                ),
                execution(
                    "EXEC-002",
                    test_definition_id="TEST-001",
                    status="PASSED",
                    started_at=(
                        BASE_TIME
                        + timedelta(hours=1)
                    ),
                    completed_at=(
                        BASE_TIME
                        + timedelta(
                            hours=1,
                            minutes=5,
                        )
                    ),
                    rerun_of_execution_id="EXEC-001",
                ),
            ]
        )

        summary = self.service.summarize("SIT")

        self.assertEqual(
            summary.readiness,
            EnvironmentReadinessStatus.READY,
        )
        self.assertEqual(
            summary.execution_summary.total,
            1,
        )
        self.assertEqual(
            summary.execution_summary.failed,
            0,
        )


class EnvironmentSummaryGroupingTests(
    EnvironmentReadinessFixtureTests
):
    """Tests covering multi-environment reporting."""

    def setUp(self) -> None:
        super().setUp()

        self.repository.add_many(
            [
                execution(
                    "EXEC-SIT-001",
                    test_definition_id="TEST-001",
                    environment="SIT",
                    execution_cycle="Cycle 1",
                    status="PASSED",
                ),
                execution(
                    "EXEC-UAT-001",
                    test_definition_id="TEST-002",
                    environment="UAT",
                    execution_cycle="Cycle 1",
                    status="FAILED",
                ),
            ]
        )

    def test_summarize_all_represented_environments(
        self,
    ) -> None:
        summaries = self.service.summarize_all()

        self.assertEqual(
            tuple(
                summary.environment
                for summary in summaries
            ),
            (
                Environment.SIT,
                Environment.UAT,
            ),
        )

    def test_requested_environments_include_no_data(
        self,
    ) -> None:
        summaries = self.service.summarize_all(
            environments=[
                "SIT",
                "UAT",
                "DEV",
            ]
        )

        by_environment = {
            summary.environment: summary
            for summary in summaries
        }

        self.assertEqual(
            by_environment[Environment.DEV].readiness,
            EnvironmentReadinessStatus.NOT_READY,
        )
        self.assertEqual(
            by_environment[Environment.SIT].readiness,
            EnvironmentReadinessStatus.READY,
        )
        self.assertEqual(
            by_environment[Environment.UAT].readiness,
            (
                EnvironmentReadinessStatus
                .PARTIALLY_READY
            ),
        )

    def test_environment_inputs_are_deduplicated(
        self,
    ) -> None:
        summaries = self.service.summarize_all(
            environments=[
                "SIT",
                "sit",
                Environment.SIT,
            ]
        )

        self.assertEqual(len(summaries), 1)

    def test_cycle_filter_is_applied(self) -> None:
        summaries = self.service.summarize_all(
            execution_cycle="Cycle 2",
            environments=["SIT", "UAT"],
        )

        self.assertTrue(
            all(
                summary.readiness
                is EnvironmentReadinessStatus.NOT_READY
                for summary in summaries
            )
        )


if __name__ == "__main__":
    unittest.main()
