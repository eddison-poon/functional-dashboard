"""Public output models exposed by the Dashboard Engine API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dashboard_engine.executive_summary import ExecutiveSummary
from dashboard_engine.snapshot import DashboardSnapshot


@dataclass(frozen=True, slots=True)
class DashboardOutput:
    """Complete public output from one dashboard-generation run."""

    snapshot: DashboardSnapshot
    executive_summary: ExecutiveSummary

    @property
    def is_clean(self) -> bool:
        return self.snapshot.quality.is_clean

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot": self.snapshot.to_dict(),
            "executive_summary": self.executive_summary.to_dict(),
        }
