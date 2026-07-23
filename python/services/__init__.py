"""Application services for dashboard reporting and aggregation."""

from .coverage_summary import (
    CoverageSummaryService,
    FrameworkCoverage,
    TestCoverageSummary,
)
from .dashboard_snapshot import (
    DashboardHealth,
    DashboardSnapshot,
    DashboardSnapshotService,
    ExecutiveSummary,
    ValidationReportProtocol,
    ValidationSnapshot,
)
from .environment_summary import (
    EnvironmentReadinessService,
    EnvironmentReadinessStatus,
    EnvironmentReadinessSummary,
    ReadinessColour,
)
from .execution_selection import (
    ExecutionGroupKey,
    ExecutionSelectionService,
)
from .execution_summary import (
    ExecutionSummary,
    ExecutionSummaryService,
)

__all__ = [
    "CoverageSummaryService",
    "DashboardHealth",
    "DashboardSnapshot",
    "DashboardSnapshotService",
    "EnvironmentReadinessService",
    "EnvironmentReadinessStatus",
    "EnvironmentReadinessSummary",
    "ExecutiveSummary",
    "ExecutionGroupKey",
    "ExecutionSelectionService",
    "ExecutionSummary",
    "ExecutionSummaryService",
    "FrameworkCoverage",
    "ReadinessColour",
    "TestCoverageSummary",
    "ValidationReportProtocol",
    "ValidationSnapshot",
]
