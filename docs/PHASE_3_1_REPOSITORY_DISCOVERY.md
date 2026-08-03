# Phase 3.1 — Repository Discovery Engine

## Objective

Phase 3.1 discovers test assets stored in the repository and reports:

- where each asset is located;
- whether it is pending review, reviewed, or published;
- whether it is a Business Scenario, Manual Test Definition, or Automation Test Definition;
- its canonical ID and title where available;
- malformed files, missing IDs, and duplicate IDs.

It does **not** build parent/child relationships, validate complete canonical
objects, calculate KPIs, or produce dashboard metrics. Those responsibilities
belong to later Phase 3 packages.

## Default asset roots

The scanner automatically checks these repository-root directories:

1. `test_cases/`
2. `test-assets/`
3. `test_assets/`

A different directory can be supplied through `asset_roots` or the command line.

## Recognised lifecycle folders

| Folder | State |
|---|---|
| `pending_review`, `pending-review`, `pending` | `pending_review` |
| `reviewed`, `approved` | `reviewed` |
| `published` | `published` |

## Recognised asset folders

| Folder examples | Asset kind |
|---|---|
| `business_scenarios`, `scenarios` | Business Scenario |
| `manual`, `manual_tests`, `manual_test_definitions` | Manual Test |
| `automation`, `automation_tests`, `automation_test_definitions` | Automation Test |

When folders are not conclusive, metadata and document content are used as
fallback classification signals.

## Supported formats

- Markdown: `.md`, `.markdown`
- JSON: `.json`

Markdown discovery supports:

- simple YAML-like front matter;
- two-column field/value tables;
- first-level heading as a title fallback.

No external YAML package is required.

## Run

From the repository root:

```bash
python3 scripts/discover_test_assets.py
```

Write a machine-readable report:

```bash
python3 scripts/discover_test_assets.py \
  --output data/repository_discovery.json
```

Use strict classification:

```bash
python3 scripts/discover_test_assets.py --strict
```

Specify a non-standard asset root:

```bash
python3 scripts/discover_test_assets.py \
  --asset-root test_cases/pending_review
```

## Exit codes

- `0`: discovery completed without issues;
- `1`: assets were discovered but one or more issues were reported;
- uncaught filesystem errors indicate an invalid repository path.

## Integration boundary

Phase 3.2 should consume `DiscoveryReport.assets` and create a relationship-aware
repository index. Phase 3.1 must remain independent from KPI, UI, connector, and
Jira publishing logic.
