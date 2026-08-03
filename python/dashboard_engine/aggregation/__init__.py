"""Repository aggregation services for the Functional Testing Dashboard."""

from .aggregator import RepositoryAggregator
from .models import (
    AssetLifecycleSummary,
    CoverageSummary,
    RepositoryAggregation,
    ScenarioCompositionSummary,
)

__all__ = [
    "AssetLifecycleSummary",
    "CoverageSummary",
    "RepositoryAggregation",
    "ScenarioCompositionSummary",
    "RepositoryAggregator",
]
