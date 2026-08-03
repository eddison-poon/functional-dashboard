# Phase 3.7 File Manifest

## Create

```text
python/dashboard_engine/api/
├── __init__.py
├── configuration.py
├── engine.py
├── exceptions.py
└── models.py

scripts/
└── generate_dashboard.py

tests/
└── test_dashboard_api.py

docs/
└── PHASE_3_7_DASHBOARD_API.md
```

## Existing dependencies

Phase 3.7 requires all committed Phase 3 packages:

```text
python/dashboard_engine/discovery/
python/dashboard_engine/indexing/
python/dashboard_engine/aggregation/
python/dashboard_engine/kpi/
python/dashboard_engine/snapshot/
python/dashboard_engine/executive_summary/
```

Do not replace earlier Phase 3 files.

## Existing files to check

If `python/dashboard_engine/__init__.py` explicitly exports subpackages, add
`api`. Otherwise, no production file edit is required.

## Validation commands

Run Phase 3.7 tests:

```bash
python3 -m unittest tests.test_dashboard_api -v
```

Run the complete suite:

```bash
python3 -m unittest discover -s tests -v
```

Generate complete dashboard output:

```bash
python3 scripts/generate_dashboard.py \
  --strict-discovery \
  --output data/dashboard.json \
  --snapshot-output data/dashboard_snapshot.json \
  --summary-output data/executive_summary.json
```

## Acceptance criteria

1. One stable public Dashboard Engine API is exposed.
2. Configuration is immutable and validated.
3. The API orchestrates Phases 3.1 through 3.6 in order.
4. Snapshot-only generation is supported.
5. Executive-summary-only generation is supported.
6. Complete dashboard generation is supported.
7. Output is immutable and JSON-compatible.
8. Quality status is exposed to callers.
9. Fatal filesystem/configuration failures use `DashboardEngineError`.
10. The CLI supports combined and separate JSON outputs.
11. Phase 4 can depend only on `dashboard_engine.api`.
12. The complete repository test suite remains green.
