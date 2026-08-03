# Phase 3.6 File Manifest

## Create

```text
python/dashboard_engine/executive_summary/
├── __init__.py
├── generator.py
├── models.py
└── rules.py

scripts/
└── build_executive_summary.py

tests/
└── test_executive_summary.py

docs/
└── PHASE_3_6_EXECUTIVE_SUMMARY.md
```

## Existing dependencies

Phase 3.6 requires:

```text
python/dashboard_engine/discovery/
python/dashboard_engine/indexing/
python/dashboard_engine/aggregation/
python/dashboard_engine/kpi/
python/dashboard_engine/snapshot/
```

Do not replace earlier Phase 3 files.

## Existing files to check

If `python/dashboard_engine/__init__.py` explicitly exports subpackages, add
`executive_summary`. Otherwise, no production file edit is required.

## Validation commands

Run Phase 3.6 tests:

```bash
python3 -m unittest tests.test_executive_summary -v
```

Run the complete suite:

```bash
python3 -m unittest discover -s tests -v
```

Generate executive-summary output:

```bash
python3 scripts/build_executive_summary.py \
  --strict-discovery \
  --output data/executive_summary.json
```

## Acceptance criteria

1. Phase 3.5 `DashboardSnapshot` is accepted as input.
2. Current phase and overall health are generated.
3. Headline is concise and management-ready.
4. Achievements are derived from measurable repository results.
5. Risks identify coverage, review, and data-quality gaps.
6. Readiness assessment reflects overall health.
7. Daily standup text follows the agreed format.
8. Output is immutable and JSON-compatible.
9. No execution, defect, environment, or trend logic is added.
10. The complete repository test suite remains green.
