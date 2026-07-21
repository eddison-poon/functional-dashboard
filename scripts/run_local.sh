#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 build_snapshot.py
echo "Dashboard available at http://localhost:8000"
python3 -m http.server 8000
