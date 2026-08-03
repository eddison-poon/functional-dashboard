# Phase 3.1 File Manifest

## Create

```text
python/dashboard_engine/discovery/
├── __init__.py
├── classifier.py
├── enums.py
├── models.py
├── parsers.py
└── scanner.py

scripts/
└── discover_test_assets.py

tests/
└── test_repository_discovery.py

docs/
└── PHASE_3_1_REPOSITORY_DISCOVERY.md
```

## Existing files to check

No existing production file must be edited for the isolated Phase 3.1 package.

If `python/dashboard_engine/__init__.py` exposes public subpackages explicitly,
add `discovery` there. Otherwise, leave it unchanged.

## Validation commands

```bash
python3 -m unittest tests.test_repository_discovery -v
python3 scripts/discover_test_assets.py --strict
python3 scripts/discover_test_assets.py \
  --strict \
  --output data/repository_discovery.json
```

## Acceptance criteria

1. Assets are discovered recursively without hardcoded filenames.
2. Business Scenario, Manual Test, and Automation Test assets are distinguished.
3. Pending Review, Reviewed, and Published states are derived from paths.
4. Markdown and JSON are supported.
5. README, `.gitkeep`, unsupported files, and common cache folders are ignored.
6. One malformed asset does not stop discovery of remaining assets.
7. Missing IDs and duplicate IDs are reported.
8. Discovery output is deterministic and JSON-compatible.
9. Discovery performs no KPI or dashboard calculations.
10. The included unit-test suite passes.
