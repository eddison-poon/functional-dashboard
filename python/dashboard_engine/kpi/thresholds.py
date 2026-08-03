"""Configurable percentage thresholds for KPI health classification."""

from __future__ import annotations

from dataclasses import dataclass

from .enums import HealthStatus, KpiDirection


@dataclass(frozen=True, slots=True)
class PercentageThresholds:
    """Classify percentage KPIs using project-standard traffic-light bands.

    Default project rules:
    - Green: 80% or above
    - Amber: 70% to below 80%
    - Red: below 70%
    """

    green_minimum: float = 80.0
    amber_minimum: float = 70.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.amber_minimum <= 100.0:
            raise ValueError("amber_minimum must be between 0 and 100")
        if not 0.0 <= self.green_minimum <= 100.0:
            raise ValueError("green_minimum must be between 0 and 100")
        if self.amber_minimum > self.green_minimum:
            raise ValueError("amber_minimum cannot exceed green_minimum")

    def classify(
        self,
        value: float,
        *,
        direction: KpiDirection = KpiDirection.HIGHER_IS_BETTER,
    ) -> HealthStatus:
        if not 0.0 <= value <= 100.0:
            raise ValueError("percentage value must be between 0 and 100")

        if direction is KpiDirection.HIGHER_IS_BETTER:
            if value >= self.green_minimum:
                return HealthStatus.GREEN
            if value >= self.amber_minimum:
                return HealthStatus.AMBER
            return HealthStatus.RED

        # For lower-is-better percentages, the same thresholds are interpreted
        # as upper health boundaries after inversion.
        inverted = 100.0 - value
        if inverted >= self.green_minimum:
            return HealthStatus.GREEN
        if inverted >= self.amber_minimum:
            return HealthStatus.AMBER
        return HealthStatus.RED
