"""Lightweight parsers used by repository discovery.

Phase 3.1 intentionally extracts only enough metadata to identify and
classify assets. Full canonical-model validation remains outside discovery.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


_ID_KEYS = (
    "scenario_id",
    "manual_test_id",
    "automation_test_id",
    "test_id",
    "id",
)
_TITLE_KEYS = (
    "scenario_name",
    "test_name",
    "title",
    "name",
)


def parse_asset_file(path: Path) -> tuple[dict[str, Any], str]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _parse_json(path), "json"
    if suffix in {".md", ".markdown"}:
        return _parse_markdown(path), "markdown"
    raise ValueError(f"Unsupported asset format: {suffix}")


def _parse_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("Top-level JSON value must be an object")
    return value


def _parse_markdown(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, Any] = {}

    # YAML-like front matter without adding a PyYAML dependency.
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            front_matter = text[3:end].strip()
            for raw_line in front_matter.splitlines():
                if ":" not in raw_line:
                    continue
                key, value = raw_line.split(":", 1)
                metadata[_normalize_key(key)] = value.strip().strip('"').strip("'")

    # Markdown table rows: | Scenario ID | MCP-JIRA-001 |
    for line in text.splitlines():
        match = re.match(r"^\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
        if not match:
            continue
        key = _normalize_key(match.group(1))
        value = match.group(2).strip()
        if key and value and not set(value) <= {"-", ":"}:
            metadata.setdefault(key, value)

    # First heading is a safe fallback title.
    heading = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if heading:
        metadata.setdefault("title", heading.group(1).strip())

    metadata["_raw_text"] = text
    return metadata


def first_value(metadata: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    normalized = {_normalize_key(str(k)): v for k, v in metadata.items()}
    for key in keys:
        value = normalized.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def extract_asset_id(metadata: dict[str, Any]) -> str | None:
    return first_value(metadata, _ID_KEYS)


def extract_title(metadata: dict[str, Any]) -> str | None:
    return first_value(metadata, _TITLE_KEYS)


def searchable_text(metadata: dict[str, Any], path: Path) -> str:
    values = [path.name, path.as_posix()]
    values.extend(str(value) for value in metadata.values())
    return " ".join(values).lower()


def _normalize_key(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")
