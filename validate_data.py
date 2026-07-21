#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from dashboard_engine.validation import validate_source  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical dashboard source data.")
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "sample_data" / "canonical_input.json",
    )
    args = parser.parse_args()

    payload = json.loads(args.source.read_text(encoding="utf-8"))
    errors = validate_source(payload)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"Validation passed: {args.source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
