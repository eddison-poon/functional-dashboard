"""Immutable models for Phase 3.6 executive summary output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dashboard_engine.kpi import HealthStatus


@dataclass(frozen=True, slots=True)
class SummaryHighlight:
    """One concise management highlight."""

    category: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "category": self.category,
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class ExecutiveSummary:
    """Management-ready summary derived from a dashboard snapshot."""

    current_phase: str
    overall_health: HealthStatus
    headline: str
    achievements: tuple[SummaryHighlight, ...]
    risks: tuple[SummaryHighlight, ...]
    readiness_assessment: str
    standup_update: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "current_phase": self.current_phase,
            "overall_health": self.overall_health.value,
            "headline": self.headline,
            "achievements": [item.to_dict() for item in self.achievements],
            "risks": [item.to_dict() for item in self.risks],
            "readiness_assessment": self.readiness_assessment,
            "standup_update": self.standup_update,
        }
