"""Metadata extraction helpers for repository indexing."""

from __future__ import annotations

import re
from typing import Any


_PARENT_SCENARIO_KEYS = (
    "parent_scenario_id",
    "business_scenario_id",
    "scenario_id",
    "parent_id",
)


def extract_parent_scenario_id(metadata: dict[str, Any]) -> str | None:
    """Return the parent Business Scenario ID from normalized metadata."""

    normalized = {
        _normalize_key(str(key)): value
        for key, value in metadata.items()
    }

    for key in _PARENT_SCENARIO_KEYS:
        value = normalized.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()

    return None


def _normalize_key(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")
