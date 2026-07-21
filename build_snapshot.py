#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from dashboard_engine.builder import SnapshotBuilder  # noqa: E402
from dashboard_engine.validation import validate_source  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the dashboard snapshot JSON.")
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "sample_data" / "canonical_input.json",
        help="Canonical input JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "snapshot.json",
        help="Generated snapshot JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_payload = json.loads(args.source.read_text(encoding="utf-8"))
    errors = validate_source(source_payload)
    if errors:
        print("Source validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    snapshot = SnapshotBuilder(ROOT).build(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

    print(f"Snapshot generated: {args.output}")
    print(
        f"Overall health: {snapshot['kpis']['overall_health'].upper()} "
        f"({snapshot['kpis']['overall_score']}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
