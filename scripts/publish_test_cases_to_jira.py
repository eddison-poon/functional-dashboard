"""Publish approved Markdown test cases to Jira.

Dry-run is the default. Live publication requires --live plus Jira environment
variables. Successful items are updated and moved from reviewed/ to published/.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from test_case_common import (
    parse_front_matter,
    section_content,
    today_iso,
    utc_now_iso,
    validate_case,
    write_json,
    write_test_case,
)


def load_config(root: Path) -> dict[str, Any]:
    path = root / "config" / "jira.example.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing Jira config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_description(body: str) -> str:
    parts = []
    for heading in (
        "Business Objective",
        "Preconditions",
        "Test Data",
        "Test Steps",
        "Overall Expected Result",
        "Automation Notes",
        "Remarks",
    ):
        content = section_content(body, heading)
        if content:
            parts.append(f"h2. {heading}\n\n{content}")
    return "\n\n".join(parts)


def build_payload(config: dict[str, Any], metadata: dict[str, Any], body: str) -> dict[str, Any]:
    labels = [
        "functional-test-case",
        str(metadata.get("business_module") or "").lower().replace(" ", "-"),
        str(metadata.get("test_type") or "").lower().replace(" ", "-"),
    ]
    fields: dict[str, Any] = {
        "project": {"key": config["project_key"]},
        "issuetype": {"name": config.get("issue_type", "Test")},
        "summary": metadata["scenario_name"],
        "description": build_description(body),
        "labels": [item for item in labels if item],
        "priority": {"name": metadata["priority"]},
    }

    field_mapping = config.get("field_mapping", {})
    for metadata_key, jira_field in field_mapping.items():
        value = metadata.get(metadata_key)
        if jira_field and value not in (None, ""):
            fields[jira_field] = value

    return {"fields": fields}


def create_jira_issue(config: dict[str, Any], payload: dict[str, Any]) -> str:
    base_url = os.getenv("JIRA_BASE_URL", str(config.get("base_url") or "")).rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    if not base_url or not email or not token:
        raise RuntimeError("JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN are required for live mode.")

    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    request = urllib.request.Request(
        f"{base_url}/rest/api/2/issue",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Jira returned HTTP {exc.code}: {detail}") from exc
    key = result.get("key")
    if not key:
        raise RuntimeError(f"Jira response did not contain an issue key: {result}")
    return str(key)


def append_audit(root: Path, entry: dict[str, Any]) -> None:
    path = root / "logs" / "jira_publish_log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--live", action="store_true", help="Create Jira issues. Default is dry-run.")
    parser.add_argument("--scenario-id", help="Publish only one approved scenario ID.")
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)

    reviewed_dir = root / "test_cases" / "reviewed"
    published_dir = root / "test_cases" / "published"
    published_dir.mkdir(parents=True, exist_ok=True)
    registry = root / "data" / "test_case_registry.json"
    registry_data = json.loads(registry.read_text(encoding="utf-8")) if registry.exists() else {"test_cases": []}
    already_published = {
        item.get("scenario_id")
        for item in registry_data.get("test_cases", [])
        if item.get("review_status") == "Published"
    }

    candidates = sorted(reviewed_dir.glob("*.md"))
    if args.scenario_id:
        candidates = [path for path in candidates if path.stem == args.scenario_id]

    if not candidates:
        print("No approved test cases found for publication.")
        return 0

    failed = 0
    for path in candidates:
        case = parse_front_matter(path)
        metadata = dict(case.metadata)
        scenario_id = metadata.get("scenario_id")
        errors = validate_case(case, root)
        if errors:
            failed += 1
            print(f"SKIP {path.name}: validation failed")
            for error in errors:
                print(f"  - {error}")
            continue
        if metadata.get("review_status") != "Approved":
            print(f"SKIP {path.name}: review_status is not Approved")
            continue
        if metadata.get("jira_id"):
            print(f"SKIP {path.name}: Jira ID already exists")
            continue
        if scenario_id in already_published:
            print(f"SKIP {path.name}: scenario already published in registry")
            continue

        payload = build_payload(config, metadata, case.body)
        if not args.live:
            print(f"DRY-RUN {scenario_id}\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
            continue

        try:
            jira_id = create_jira_issue(config, payload)
            metadata["jira_id"] = jira_id
            metadata["review_status"] = "Published"
            metadata["published_date"] = today_iso()
            write_test_case(path, metadata, case.body)
            destination = published_dir / path.name
            shutil.move(str(path), destination)
            append_audit(
                root,
                {
                    "timestamp": utc_now_iso(),
                    "scenario_id": scenario_id,
                    "jira_id": jira_id,
                    "status": "CREATED",
                    "source_file": destination.relative_to(root).as_posix(),
                },
            )
            print(f"PUBLISHED {scenario_id} -> {jira_id}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            append_audit(
                root,
                {
                    "timestamp": utc_now_iso(),
                    "scenario_id": scenario_id,
                    "status": "FAILED",
                    "error": str(exc),
                },
            )
            print(f"FAIL {scenario_id}: {exc}", file=sys.stderr)

    if args.live:
        from build_test_case_registry import main as rebuild_registry

        original_argv = sys.argv
        try:
            sys.argv = ["build_test_case_registry.py", "--root", str(root)]
            rebuild_registry()
        finally:
            sys.argv = original_argv

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
