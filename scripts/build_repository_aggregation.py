#!/usr/bin/env python3
"""Run discovery, indexing, and Phase 3.3 repository aggregation."""

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build repository discovery, index, and aggregation output."
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

    payload = {
        "discovery": {
            "is_clean": discovery.is_clean,
            "issue_count": len(discovery.issues),
        },
        "repository_index": {
            "is_clean": index.is_clean,
            "issue_count": len(index.issues),
        },
        "aggregation": aggregation.to_dict(),
    }

    rendered = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = Path(args.repository_root) / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Repository aggregation written to {output_path}")
    else:
        print(rendered)

    total_issues = len(discovery.issues) + len(index.issues)
    print(
        f"Aggregated {len(index.scenarios)} scenarios and "
        f"{len(index.test_definitions)} test definitions; "
        f"{total_issues} upstream issues.",
        file=sys.stderr,
    )

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
