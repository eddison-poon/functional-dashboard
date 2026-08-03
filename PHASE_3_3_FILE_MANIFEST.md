# Phase 3.3 File Manifest

## Create

```text
python/dashboard_engine/aggregation/
├── __init__.py
├── aggregator.py
└── models.py

scripts/
└── build_repository_aggregation.py

tests/
└── test_repository_aggregation.py

docs/
└── PHASE_3_3_AGGREGATION_ENGINE.md
```

## Existing dependencies

Phase 3.3 requires the committed packages:

```text
python/dashboard_engine/discovery/
python/dashboard_engine/indexing/
```

Do not duplicate or replace Phase 3.1 or Phase 3.2 files.

## Existing files to check

If `python/dashboard_engine/__init__.py` explicitly exports subpackages, add
`aggregation`. Otherwise, no existing production file requires modification.

## Validation commands

Run the Phase 3.3 tests:

```bash
python3 -m unittest tests.test_repository_aggregation -v
```

Run the complete suite:

```bash
python3 -m unittest discover -s tests -v
```

Generate repository aggregation:

```bash
python3 scripts/build_repository_aggregation.py \
  --strict-discovery \
  --output data/repository_aggregation.json
```

## Acceptance criteria

1. Phase 3.2 `RepositoryIndex` is accepted as input.
2. Lifecycle totals are produced for Scenarios, Manual Tests, and Automation Tests.
3. Manual Scenario coverage is calculated.
4. Automation Scenario coverage is calculated.
5. Overall Test Definition coverage is calculated.
6. Scenario composition is mutually exclusive and complete.
7. Empty repositories are handled safely.
8. Upstream issue and ignored-asset totals are retained.
9. Output is immutable and JSON-compatible.
10. No execution, environment, readiness, or traffic-light KPI logic is included.
11. The complete repository test suite remains green.
