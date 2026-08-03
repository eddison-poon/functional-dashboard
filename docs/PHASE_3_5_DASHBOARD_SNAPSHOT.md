# Phase 3.5 — Dashboard Snapshot

## Objective

Phase 3.5 combines the outputs of Phase 3.1 through Phase 3.4 into one stable,
JSON-compatible dashboard contract.

The snapshot becomes the only file the future GitHub Pages user interface needs
to read.

## Input

- `DiscoveryReport`
- `RepositoryIndex`
- `RepositoryAggregation`
- `RepositoryKpiSet`

## Output

- `DashboardSnapshot`
- default file: `data/dashboard_snapshot.json`

## Snapshot structure

```json
{
  "metadata": {},
  "quality": {},
  "summary": {},
  "kpis": {},
  "repository": {}
}
```

## Sections

### metadata

Contains:

- schema version
- generation timestamp
- source label

### quality

Contains:

- discovery issue count
- indexing issue count
- ignored asset count
- combined issue count
- clean/not-clean flag

### summary

Contains the Phase 3.3 asset, lifecycle, coverage, composition, and quality
aggregations.

### kpis

Contains the Phase 3.4 management-ready KPI set.

### repository

Contains the Scenario-level hierarchy required by future dashboard views:

- Business Scenario
- linked Manual Test Definitions
- linked Automation Test Definitions
- lifecycle state
- asset paths
- relationship counts

## Schema version

Phase 3.5 starts with:

```text
1.0
```

Any future breaking change to the JSON contract must increment the schema
version.

## Run

```bash
python3 scripts/build_dashboard_snapshot.py
```

Explicit output:

```bash
python3 scripts/build_dashboard_snapshot.py \
  --strict-discovery \
  --output data/dashboard_snapshot.json
```

Custom thresholds:

```bash
python3 scripts/build_dashboard_snapshot.py \
  --green-minimum 85 \
  --amber-minimum 70
```

## Exit codes

- `0`: snapshot generated with no quality issues
- `1`: snapshot generated, but quality issues exist

The JSON file is still generated when non-fatal quality issues are present.

## Phase boundary

Phase 3.5 is a data-contract package. It does not:

- render HTML;
- create charts;
- calculate execution results;
- evaluate environments;
- process defects;
- generate executive narrative;
- retain trend history.

Those concerns belong to later phases.
