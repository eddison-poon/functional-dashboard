# Phase 3.2 File Manifest

## Create

```text
python/dashboard_engine/indexing/
├── __init__.py
├── builder.py
├── metadata.py
└── models.py

scripts/
└── build_repository_index.py

tests/
└── test_repository_index.py

docs/
└── PHASE_3_2_REPOSITORY_INDEX.md
```

## Existing dependency

Phase 3.2 requires the committed Phase 3.1 package:

```text
python/dashboard_engine/discovery/
```

Do not duplicate or replace the Phase 3.1 files.

## Existing files to check

If `python/dashboard_engine/__init__.py` explicitly exports subpackages, add
`indexing`. Otherwise, no existing production file requires modification.

## Validation commands

Run the Phase 3.2 tests:

```bash
python3 -m unittest tests.test_repository_index -v
```

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

Build the repository index:

```bash
python3 scripts/build_repository_index.py \
  --strict-discovery \
  --output data/repository_index.json
```

## Acceptance criteria

1. Phase 3.1 `DiscoveryReport` is accepted as input.
2. Business Scenarios are indexed by canonical ID.
3. Multiple Manual Test Definitions may link to one Scenario.
4. Multiple Automation Test Definitions may link to one Scenario.
5. A Scenario may contain Manual only, Automation only, both, or neither.
6. Missing parent Scenario references are reported.
7. Orphan Test Definitions are reported and excluded.
8. Duplicate IDs are reported deterministically.
9. Direct Scenario and Test Definition lookup is supported.
10. Output is immutable and JSON-compatible.
11. No KPI or dashboard calculation is performed.
12. The complete existing test suite remains green.
