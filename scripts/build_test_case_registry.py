"""Build the dashboard-friendly JSON registry from governed Markdown files."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from test_case_common import (
    discover_test_cases,
    parse_front_matter,
    utc_now_iso,
    validate_case,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--include-invalid", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()

    config_path = root / "config" / "jira.example.json"
    jira_base_url = ""
    if config_path.exists():
        import json

        config = json.loads(config_path.read_text(encoding="utf-8"))
        jira_base_url = str(config.get("base_url") or "").rstrip("/")

    records: list[dict] = []
    for path in discover_test_cases(root):
        case = parse_front_matter(path)
        errors = validate_case(case, root)
        if errors and not args.include_invalid:
            continue

        data = dict(case.metadata)
        relative = path.relative_to(root).as_posix()
        folder = path.parent.name
        jira_id = data.get("jira_id") or None
        jira_url = f"{jira_base_url}/browse/{quote(str(jira_id))}" if jira_base_url and jira_id else None

        records.append(
            {
                "scenario_id": data.get("scenario_id"),
                "jira_id": jira_id,
                "scenario_name": data.get("scenario_name"),
                "business_module": data.get("business_module"),
                "business_feature": data.get("business_feature"),
                "category": data.get("category"),
                "priority": data.get("priority"),
                "test_type": data.get("test_type"),
                "manual_exists": data.get("manual_exists"),
                "automation_exists": data.get("automation_exists"),
                "review_status": data.get("review_status"),
                "scenario_pattern": data.get("scenario_pattern"),
                "owner": data.get("owner"),
                "created_date": data.get("created_date"),
                "reviewed_date": data.get("reviewed_date"),
                "published_date": data.get("published_date"),
                "source_file": relative,
                "workflow_folder": folder,
                "jira_url": jira_url,
                "validation_status": "Invalid" if errors else "Valid",
                "validation_errors": errors,
            }
        )

    records.sort(key=lambda item: (str(item.get("business_module")), str(item.get("scenario_id"))))
    statuses = Counter(str(record.get("review_status")) for record in records)
    total = len(records)
    published = statuses.get("Published", 0)
    payload = {
        "generated_at": utc_now_iso(),
        "summary": {
            "total_test_cases": total,
            "manual_test_cases": sum(bool(r.get("manual_exists")) for r in records),
            "automated_test_cases": sum(bool(r.get("automation_exists")) for r in records),
            "pending_review": statuses.get("Pending", 0),
            "approved_unpublished": statuses.get("Approved", 0),
            "published": published,
            "rejected": statuses.get("Rejected", 0),
            "publication_rate_percent": round((published / total * 100), 1) if total else 0.0,
        },
        "test_cases": records,
    }
    output = root / "data" / "test_case_registry.json"
    write_json(output, payload)
    print(f"Wrote {output.relative_to(root)} with {len(records)} record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
