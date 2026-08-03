"""Executive summary generation for the Functional Testing Dashboard."""

from .generator import ExecutiveSummaryGenerator
from .models import ExecutiveSummary, SummaryHighlight
from .rules import OverallHealthEvaluator

__all__ = [
    "ExecutiveSummary",
    "SummaryHighlight",
    "OverallHealthEvaluator",
    "ExecutiveSummaryGenerator",
]
