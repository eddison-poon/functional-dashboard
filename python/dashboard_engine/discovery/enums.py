"""Controlled vocabularies used by repository discovery."""

from __future__ import annotations

from enum import Enum


class AssetKind(str, Enum):
    """Canonical repository asset categories understood in Phase 3.1."""

    BUSINESS_SCENARIO = "business_scenario"
    MANUAL_TEST = "manual_test"
    AUTOMATION_TEST = "automation_test"
    UNKNOWN = "unknown"


class ReviewState(str, Enum):
    """Lifecycle location of a repository asset."""

    PENDING_REVIEW = "pending_review"
    REVIEWED = "reviewed"
    PUBLISHED = "published"
    UNKNOWN = "unknown"
