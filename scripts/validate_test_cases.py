"""Validate all governed Markdown test cases."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from test_case_common import discover_test_cases, parse_front_matter, validate_case


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    paths = discover_test_cases(root)
    failures = 0
    scenario_ids: list[str] = []

    if not paths:
        print("No governed test-case Markdown files found. Validation passed.")
        return 0

    for path in paths:
        try:
            case = parse_front_matter(path)
            errors = validate_case(case, root)
            scenario_id = str(case.metadata.get("scenario_id") or "")
            if scenario_id:
                scenario_ids.append(scenario_id)
        except Exception as exc:  # noqa: BLE001
            errors = [str(exc)]

        relative = path.relative_to(root)
        if errors:
            failures += 1
            print(f"FAIL {relative}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {relative}")

    duplicates = {item for item, count in Counter(scenario_ids).items() if count > 1}
    if duplicates:
        failures += len(duplicates)
        for scenario_id in sorted(duplicates):
            print(f"FAIL duplicate scenario_id: {scenario_id}")

    print(f"\nValidated {len(paths)} file(s); {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
