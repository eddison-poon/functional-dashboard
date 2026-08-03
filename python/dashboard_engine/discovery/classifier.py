"""Classification rules for discovered repository assets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .enums import AssetKind, ReviewState
from .parsers import searchable_text


_KIND_DIRECTORY_HINTS = {
    AssetKind.BUSINESS_SCENARIO: {
        "business_scenario",
        "business_scenarios",
        "scenario",
        "scenarios",
    },
    AssetKind.MANUAL_TEST: {
        "manual",
        "manual_test",
        "manual_tests",
        "manual_test_definition",
        "manual_test_definitions",
    },
    AssetKind.AUTOMATION_TEST: {
        "automation",
        "automated",
        "automation_test",
        "automation_tests",
        "automation_test_definition",
        "automation_test_definitions",
    },
}

_STATE_DIRECTORY_HINTS = {
    ReviewState.PENDING_REVIEW: {"pending_review", "pending-review", "pending"},
    ReviewState.REVIEWED: {"reviewed", "approved"},
    ReviewState.PUBLISHED: {"published"},
}


def classify_review_state(relative_path: Path) -> ReviewState:
    parts = {part.lower() for part in relative_path.parts}
    for state, hints in _STATE_DIRECTORY_HINTS.items():
        if parts & hints:
            return state
    return ReviewState.UNKNOWN


def classify_asset_kind(relative_path: Path, metadata: dict[str, Any]) -> AssetKind:
    parts = {part.lower() for part in relative_path.parts}
    for kind, hints in _KIND_DIRECTORY_HINTS.items():
        if parts & hints:
            return kind

    text = searchable_text(metadata, relative_path)

    explicit_type = str(
        metadata.get("asset_type")
        or metadata.get("test_type")
        or metadata.get("definition_type")
        or metadata.get("type")
        or ""
    ).lower()

    if "automation" in explicit_type or "automated" in explicit_type:
        return AssetKind.AUTOMATION_TEST
    if "manual" in explicit_type:
        return AssetKind.MANUAL_TEST
    if "scenario" in explicit_type:
        return AssetKind.BUSINESS_SCENARIO

    if "automation_test_id" in metadata or "automation test id" in text:
        return AssetKind.AUTOMATION_TEST
    if "manual_test_id" in metadata or "manual test id" in text:
        return AssetKind.MANUAL_TEST
    if "scenario_id" in metadata or "business scenario" in text:
        return AssetKind.BUSINESS_SCENARIO

    return AssetKind.UNKNOWN
