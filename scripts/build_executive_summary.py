#!/usr/bin/env python3
"""Generate a Phase 3.6 executive summary from repository assets."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = REPOSITORY_ROOT / "python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from dashboard_engine.aggregation import RepositoryAggregator  # noqa: E402
from dashboard_engine.discovery import RepositoryDiscovery  # noqa: E402
from dashboard_engine.executive_summary import (  # noqa: E402
    ExecutiveSummaryGenerator,
)
from dashboard_engine.indexing import RepositoryIndexBuilder  # noqa: E402
from dashboard_engine.kpi import (  # noqa: E402
    PercentageThresholds,
    RepositoryKpiCalculator,
)
from dashboard_engine.snapshot import DashboardSnapshotBuilder  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Phase 3.6 executive summary."
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
        default="data/executive_summary.json",
        help="Executive summary JSON output path.",
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
        "--current-phase",
        default="Test Design and Review",
        help="Management-facing current phase label.",
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

    repository_index = RepositoryIndexBuilder().build(discovery)
    aggregation = RepositoryAggregator().aggregate(repository_index)
    thresholds = PercentageThresholds(
        green_minimum=args.green_minimum,
        amber_minimum=args.amber_minimum,
    )
    kpis = RepositoryKpiCalculator(
        thresholds=thresholds
    ).calculate(aggregation)
    snapshot = DashboardSnapshotBuilder().build(
        discovery=discovery,
        repository_index=repository_index,
        aggregation=aggregation,
        kpis=kpis,
        generated_at=datetime.now(UTC),
    )
    summary = ExecutiveSummaryGenerator(
        current_phase=args.current_phase
    ).generate(snapshot)

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(args.repository_root) / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Executive summary written to {output_path}")
    print(summary.headline, file=sys.stderr)

    return 0 if snapshot.quality.is_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
