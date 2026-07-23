"""Shared helpers for Phase 2.5 test-case governance scripts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install dependencies with: pip install -r requirements-phase-2.5.txt"
    ) from exc

SCENARIO_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3,}$")
JIRA_ID_RE = re.compile(r"^[A-Z][A-Z0-9_]*-[1-9][0-9]*$")

PRIORITIES = {"Critical", "High", "Medium", "Low"}
TEST_TYPES = {
    "Functional",
    "Smoke",
    "Sanity",
    "Regression",
    "Integration",
    "End-to-End",
    "API",
    "UI",
}
REVIEW_STATUSES = {"Pending", "Approved", "Published", "Rejected"}
WORKFLOW_FOLDERS = {
    "pending_review": "Pending",
    "reviewed": "Approved",
    "published": "Published",
    "rejected": "Rejected",
}
REQUIRED_METADATA = {
    "scenario_id",
    "scenario_name",
    "business_feature",
    "business_module",
    "priority",
    "test_type",
    "category",
    "manual_exists",
    "automation_exists",
    "review_status",
}
REQUIRED_SECTIONS = {
    "Business Objective",
    "Preconditions",
    "Test Steps",
    "Overall Expected Result",
}


@dataclass(frozen=True)
class ParsedTestCase:
    path: Path
    metadata: dict[str, Any]
    body: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_iso() -> str:
    return date.today().isoformat()


def parse_front_matter(path: Path) -> ParsedTestCase:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("File must start with YAML front matter delimited by '---'.")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("YAML front matter closing delimiter is missing.")
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        raise ValueError("YAML front matter must be a mapping/object.")
    return ParsedTestCase(path=path, metadata=metadata, body=parts[2].lstrip("\n"))


def render_test_case(metadata: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(
        metadata,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{yaml_text}\n---\n\n{body.lstrip()}"


def write_test_case(path: Path, metadata: dict[str, Any], body: str) -> None:
    path.write_text(render_test_case(metadata, body), encoding="utf-8")


def section_content(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^#\s+{re.escape(heading)}\s*$\n(.*?)(?=^#\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group(1).strip() if match else ""


def validate_case(case: ParsedTestCase, root: Path) -> list[str]:
    errors: list[str] = []
    data = case.metadata

    missing = sorted(key for key in REQUIRED_METADATA if key not in data)
    if missing:
        errors.append(f"Missing metadata fields: {', '.join(missing)}")

    scenario_id = str(data.get("scenario_id") or "").strip()
    if not SCENARIO_ID_RE.fullmatch(scenario_id):
        errors.append("scenario_id does not match the required uppercase hyphenated format.")
    if scenario_id and case.path.name != f"{scenario_id}.md":
        errors.append(f"File name must be {scenario_id}.md.")

    for key in ("scenario_name", "business_feature", "business_module", "category"):
        if not str(data.get(key) or "").strip():
            errors.append(f"{key} must not be empty.")

    if data.get("priority") not in PRIORITIES:
        errors.append(f"priority must be one of: {', '.join(sorted(PRIORITIES))}.")
    if data.get("test_type") not in TEST_TYPES:
        errors.append(f"test_type must be one of: {', '.join(sorted(TEST_TYPES))}.")
    if data.get("review_status") not in REVIEW_STATUSES:
        errors.append(f"review_status must be one of: {', '.join(sorted(REVIEW_STATUSES))}.")

    for key in ("manual_exists", "automation_exists"):
        if not isinstance(data.get(key), bool):
            errors.append(f"{key} must be YAML boolean true or false.")
    if data.get("manual_exists") is False and data.get("automation_exists") is False:
        errors.append("At least one of manual_exists or automation_exists must be true.")

    relative_parts = case.path.relative_to(root).parts
    folder = relative_parts[1] if len(relative_parts) > 1 else ""
    expected_status = WORKFLOW_FOLDERS.get(folder)
    if expected_status and data.get("review_status") != expected_status:
        errors.append(
            f"Folder '{folder}' requires review_status '{expected_status}', "
            f"not '{data.get('review_status')}'."
        )

    jira_id = data.get("jira_id")
    if jira_id not in (None, "") and not JIRA_ID_RE.fullmatch(str(jira_id)):
        errors.append("jira_id is not a valid Jira issue key.")
    if folder in {"pending_review", "reviewed"} and jira_id not in (None, ""):
        errors.append(f"jira_id must be empty while the file is in {folder}/.")
    if folder == "published" and jira_id in (None, ""):
        errors.append("Published test cases require jira_id.")

    if data.get("review_status") in {"Approved", "Published"}:
        if not data.get("reviewed_by"):
            errors.append("reviewed_by is required for Approved or Published cases.")
        if not data.get("reviewed_date"):
            errors.append("reviewed_date is required for Approved or Published cases.")
    if data.get("review_status") == "Published" and not data.get("published_date"):
        errors.append("published_date is required for Published cases.")

    for heading in REQUIRED_SECTIONS:
        content = section_content(case.body, heading)
        if not content:
            errors.append(f"Required section '# {heading}' is missing or empty.")

    steps = section_content(case.body, "Test Steps")
    if steps and "| Step | Action | Expected Outcome |" not in steps:
        errors.append("Test Steps must use the standard Step / Action / Expected Outcome table.")

    return errors


def discover_test_cases(root: Path) -> list[Path]:
    paths: list[Path] = []
    for folder in WORKFLOW_FOLDERS:
        directory = root / "test_cases" / folder
        if directory.exists():
            paths.extend(sorted(p for p in directory.glob("*.md") if p.name != ".gitkeep"))
    return paths


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
