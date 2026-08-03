"""Health evaluation rules used by the executive summary generator."""

from __future__ import annotations

from collections.abc import Iterable

from dashboard_engine.kpi import HealthStatus, KpiResult


class OverallHealthEvaluator:
    """Evaluate overall repository preparation health from selected KPIs."""

    def evaluate(self, kpis: Iterable[KpiResult]) -> HealthStatus:
        statuses = [
            item.status
            for item in kpis
            if item.status is not HealthStatus.NOT_APPLICABLE
        ]

        if not statuses:
            return HealthStatus.NOT_APPLICABLE
        if HealthStatus.RED in statuses:
            return HealthStatus.RED
        if HealthStatus.AMBER in statuses:
            return HealthStatus.AMBER
        return HealthStatus.GREEN
