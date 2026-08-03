# Phase 3.5 File Manifest

## Create

```text
python/dashboard_engine/snapshot/
├── __init__.py
├── builder.py
└── models.py

scripts/
└── build_dashboard_snapshot.py

tests/
└── test_dashboard_snapshot.py

docs/
└── PHASE_3_5_DASHBOARD_SNAPSHOT.md
```

## Existing dependencies

Phase 3.5 requires the committed packages:

```text
python/dashboard_engine/discovery/
python/dashboard_engine/indexing/
python/dashboard_engine/aggregation/
python/dashboard_engine/kpi/
```

Do not replace earlier Phase 3 files.

## Existing files to check

If `python/dashboard_engine/__init__.py` explicitly exports subpackages, add
`snapshot`. Otherwise, no existing production file requires modification.

## Validation commands

Run Phase 3.5 tests:

```bash
python3 -m unittest tests.test_dashboard_snapshot -v
```

Run the complete suite:

```bash
python3 -m unittest discover -s tests -v
```

Generate the first UI-ready snapshot:

```bash
python3 scripts/build_dashboard_snapshot.py \
  --strict-discovery \
  --output data/dashboard_snapshot.json
```

## Acceptance criteria

1. Phase 3.1–3.4 outputs are accepted as inputs.
2. One immutable `DashboardSnapshot` is produced.
3. Output contains metadata, quality, summary, KPIs, and repository hierarchy.
4. Output is JSON-compatible.
5. Generation timestamp is timezone-aware.
6. Schema version is explicit and stable.
7. Non-fatal upstream issues do not prevent snapshot generation.
8. Exit status reflects snapshot quality.
9. No HTML, trend, execution, defect, or narrative logic is included.
10. The complete repository test suite remains green.
