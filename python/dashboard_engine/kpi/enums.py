"""Controlled vocabularies used by Phase 3.4 KPI calculations."""

from __future__ import annotations

from enum import Enum


class HealthStatus(str, Enum):
    """Traffic-light health status."""

    GREEN = "green"
    AMBER = "amber"
    RED = "red"
    NOT_APPLICABLE = "not_applicable"


class KpiDirection(str, Enum):
    """Indicates whether a higher or lower KPI value is preferable."""

    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"
