#!/usr/bin/env python3
"""Run Phase 3.1 repository discovery and optionally write JSON output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = REPOSITORY_ROOT / "python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from dashboard_engine.discovery import RepositoryDiscovery  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover business scenarios, manual tests, and automation tests."
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
        "--strict",
        action="store_true",
        help="Report unknown asset kinds and lifecycle states as issues.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    discovery = RepositoryDiscovery(
        args.repository_root,
        asset_roots=args.asset_roots,
        strict_unknown_kind=args.strict,
        strict_unknown_state=args.strict,
    )
    report = discovery.discover()
    payload = report.to_dict()
    rendered = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = Path(args.repository_root) / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Discovery report written to {output_path}")
    else:
        print(rendered)

    print(
        f"Discovered {len(report.assets)} assets; "
        f"{len(report.issues)} issues; "
        f"{report.ignored_files} ignored files.",
        file=sys.stderr,
    )
    return 0 if report.is_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
