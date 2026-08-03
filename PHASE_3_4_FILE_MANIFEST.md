# Phase 3.4 File Manifest

## Create

```text
python/dashboard_engine/kpi/
├── __init__.py
├── calculator.py
├── enums.py
├── models.py
└── thresholds.py

scripts/
└── build_repository_kpis.py

tests/
└── test_repository_kpi.py

docs/
└── PHASE_3_4_KPI_ENGINE.md
```

## Existing dependencies

Phase 3.4 requires:

```text
python/dashboard_engine/discovery/
python/dashboard_engine/indexing/
python/dashboard_engine/aggregation/
```

Do not replace files from Phase 3.1, 3.2, or 3.3.

## Existing files to check

If `python/dashboard_engine/__init__.py` explicitly exports subpackages, add
`kpi`. Otherwise, no production file edit is required.

## Validation commands

Run Phase 3.4 tests:

```bash
python3 -m unittest tests.test_repository_kpi -v
```

Run the complete suite:

```bash
python3 -m unittest discover -s tests -v
```

Generate KPI output:

```bash
python3 scripts/build_repository_kpis.py \
  --strict-discovery \
  --output data/repository_kpis.json
```

## Acceptance criteria

1. Phase 3.3 `RepositoryAggregation` is accepted as input.
2. Manual, Automation, and Overall Coverage KPIs are produced.
3. Scenario and Test Definition review-completion KPIs are produced.
4. Repository Data Quality KPI is produced.
5. Default thresholds are Green >=80, Amber >=70, Red <70.
6. Thresholds are configurable.
7. Zero denominators return Not Applicable.
8. Every KPI exposes numerator, denominator, value, status, and thresholds.
9. Output is immutable and JSON-compatible.
10. No execution, environment, defect, or release-readiness logic is added.
11. The complete repository test suite remains green.
