#!/usr/bin/env python3
"""Run discovery, indexing, aggregation, and Phase 3.4 KPI calculation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = REPOSITORY_ROOT / "python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from dashboard_engine.aggregation import RepositoryAggregator  # noqa: E402
from dashboard_engine.discovery import RepositoryDiscovery  # noqa: E402
from dashboard_engine.indexing import RepositoryIndexBuilder  # noqa: E402
from dashboard_engine.kpi import (  # noqa: E402
    PercentageThresholds,
    RepositoryKpiCalculator,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build repository KPIs from repository test assets."
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
        help="Optional JSON output path.",
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    discovery = RepositoryDiscovery(
        args.repository_root,
        asset_roots=args.asset_roots,
        strict_unknown_kind=args.strict_discovery,
        strict_unknown_state=args.strict_discovery,
    ).discover()

    index = RepositoryIndexBuilder().build(discovery)
    aggregation = RepositoryAggregator().aggregate(index)

    thresholds = PercentageThresholds(
        green_minimum=args.green_minimum,
        amber_minimum=args.amber_minimum,
    )
    kpis = RepositoryKpiCalculator(thresholds=thresholds).calculate(aggregation)

    payload = {
        "quality": {
            "discovery_issue_count": len(discovery.issues),
            "indexing_issue_count": len(index.issues),
            "ignored_asset_count": len(index.ignored_assets),
        },
        "thresholds": {
            "green_minimum": thresholds.green_minimum,
            "amber_minimum": thresholds.amber_minimum,
        },
        "repository_kpis": kpis.to_dict(),
    }

    rendered = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = Path(args.repository_root) / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Repository KPI output written to {output_path}")
    else:
        print(rendered)

    total_issues = len(discovery.issues) + len(index.issues)
    print(
        f"Calculated {len(kpis.all_results())} KPIs; "
        f"{total_issues} upstream issues.",
        file=sys.stderr,
    )

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
