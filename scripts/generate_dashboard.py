#!/usr/bin/env python3
"""Generate the complete Phase 3 dashboard output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = REPOSITORY_ROOT / "python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from dashboard_engine.api import (  # noqa: E402
    DashboardEngine,
    DashboardEngineConfig,
    DashboardEngineError,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the complete Functional Testing Dashboard output."
    )
    parser.add_argument(
        "--repository-root",
        default=str(REPOSITORY_ROOT),
        help="Repository root to scan.",
    )
    parser.add_argument(
        "--asset-root",
        action="append",
        dest="asset_roots",
        help="Optional asset root relative to the repository. May be repeated.",
    )
    parser.add_argument(
        "--output",
        default="data/dashboard.json",
        help="Complete dashboard JSON output path.",
    )
    parser.add_argument(
        "--snapshot-output",
        help="Optional standalone snapshot JSON output path.",
    )
    parser.add_argument(
        "--summary-output",
        help="Optional standalone executive-summary JSON output path.",
    )
    parser.add_argument(
        "--strict-discovery",
        action="store_true",
        help="Report unknown discovery kinds and lifecycle states.",
    )
    parser.add_argument(
        "--green-minimum",
        type=float,
        default=80.0,
        help="Minimum percentage for Green status.",
    )
    parser.add_argument(
        "--amber-minimum",
        type=float,
        default=70.0,
        help="Minimum percentage for Amber status.",
    )
    parser.add_argument(
        "--source",
        default="repository",
        help="Snapshot source label.",
    )
    parser.add_argument(
        "--current-phase",
        default="Test Design and Review",
        help="Management-facing current phase label.",
    )
    return parser.parse_args()


def write_json(repository_root: Path, output: str, payload: dict) -> Path:
    output_path = Path(output)
    if not output_path.is_absolute():
        output_path = repository_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def main() -> int:
    args = parse_args()
    repository_root = Path(args.repository_root).expanduser().resolve()

    config = DashboardEngineConfig(
        repository_root=repository_root,
        asset_roots=(
            tuple(Path(value) for value in args.asset_roots)
            if args.asset_roots
            else None
        ),
        strict_discovery=args.strict_discovery,
        green_minimum=args.green_minimum,
        amber_minimum=args.amber_minimum,
        source=args.source,
        current_phase=args.current_phase,
    )

    try:
        output = DashboardEngine(config=config).generate_dashboard()
    except DashboardEngineError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    dashboard_path = write_json(
        repository_root,
        args.output,
        output.to_dict(),
    )
    print(f"Dashboard output written to {dashboard_path}")

    if args.snapshot_output:
        snapshot_path = write_json(
            repository_root,
            args.snapshot_output,
            output.snapshot.to_dict(),
        )
        print(f"Snapshot output written to {snapshot_path}")

    if args.summary_output:
        summary_path = write_json(
            repository_root,
            args.summary_output,
            output.executive_summary.to_dict(),
        )
        print(f"Executive summary written to {summary_path}")

    print(output.executive_summary.headline, file=sys.stderr)
    return 0 if output.is_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
