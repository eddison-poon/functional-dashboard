# Agent Hub Functional Testing Dashboard

Production-ready Version 1 foundation for a GitHub Pages engineering intelligence
dashboard.

## Finalized layout

- Top KPI strip for executive release health
- Two-level Capability Explorer:
  - Capability Group
  - Capability
- Dynamic right workspace:
  - capability summary
  - environment health
  - feature readiness
  - horizontal scenario results
  - manual / automation / latest execution indicators
  - execution history
  - direct Jira links

## Quick start

```bash
python3 validate_data.py
python3 -m unittest discover -s tests -v
python3 build_snapshot.py
python3 -m http.server 8000
```

Open `http://localhost:8000`.

Do not open `index.html` directly from the filesystem because browsers normally
block JSON `fetch()` requests under the `file://` protocol.

## Repository structure

```text
.
├── index.html
├── build_snapshot.py
├── validate_data.py
├── assets/
│   ├── css/dashboard.css
│   └── js/dashboard.js
├── config/
│   ├── dashboard.json
│   ├── environments.json
│   ├── health_rules.json
│   ├── label_mapping.json
│   └── status_mapping.json
├── data/
│   └── snapshot.json
├── sample_data/
│   └── canonical_input.json
├── python/dashboard_engine/
│   ├── builder.py
│   ├── jira_connector.py
│   ├── metrics.py
│   ├── models.py
│   └── validation.py
├── tests/
├── docs/
└── .github/workflows/
```

## What `build_snapshot.py` does

It does **not** generate HTML.

It:

1. reads canonical testing data
2. validates IDs and statuses
3. finds the latest execution per scenario
4. calculates scenario, feature, capability, group, environment, and KPI metrics
5. applies configured health thresholds
6. builds Jira links
7. writes `data/snapshot.json`

`index.html` and `assets/js/dashboard.js` load this generated snapshot.

## Current data source

Version 1 uses `sample_data/canonical_input.json` so the repository works
immediately. `python/dashboard_engine/jira_connector.py` defines the future Jira
connector boundary without pretending that authentication and field mapping are
already implemented.

See `docs/NEXT_PHASE.md` for the planned Python programs.
