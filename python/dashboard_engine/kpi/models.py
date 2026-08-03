"""Immutable KPI output models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums import HealthStatus, KpiDirection


@dataclass(frozen=True, slots=True)
class ThresholdBand:
    """Threshold information embedded with a KPI result."""

    green_minimum: float
    amber_minimum: float

    def to_dict(self) -> dict[str, float]:
        return {
            "green_minimum": self.green_minimum,
            "amber_minimum": self.amber_minimum,
        }


@dataclass(frozen=True, slots=True)
class KpiResult:
    """One management-ready KPI."""

    key: str
    title: str
    value: float
    unit: str
    status: HealthStatus
    direction: KpiDirection
    numerator: int
    denominator: int
    threshold: ThresholdBand
    description: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "value": self.value,
            "unit": self.unit,
            "status": self.status.value,
            "direction": self.direction.value,
            "numerator": self.numerator,
            "denominator": self.denominator,
            "threshold": self.threshold.to_dict(),
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class RepositoryKpiSet:
    """Phase 3.4 KPI collection derived from repository aggregation."""

    manual_coverage: KpiResult
    automation_coverage: KpiResult
    overall_test_coverage: KpiResult
    scenario_review_completion: KpiResult
    manual_test_review_completion: KpiResult
    automation_test_review_completion: KpiResult
    all_test_review_completion: KpiResult
    repository_data_quality: KpiResult

    def all_results(self) -> tuple[KpiResult, ...]:
        return (
            self.manual_coverage,
            self.automation_coverage,
            self.overall_test_coverage,
            self.scenario_review_completion,
            self.manual_test_review_completion,
            self.automation_test_review_completion,
            self.all_test_review_completion,
            self.repository_data_quality,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kpis": {
                result.key: result.to_dict()
                for result in self.all_results()
            }
        }
