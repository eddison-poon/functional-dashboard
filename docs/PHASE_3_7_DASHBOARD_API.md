# Phase 3.7 — Dashboard API

## Objective

Phase 3.7 provides one stable public API over the complete Phase 3 pipeline.

Consumers such as the future GitHub Pages frontend, scheduled jobs, connectors,
or local scripts should call this API instead of importing the lower-level
discovery, indexing, aggregation, KPI, snapshot, or summary packages directly.

## Public API

```python
from dashboard_engine.api import DashboardEngine

engine = DashboardEngine("/path/to/repository")

snapshot = engine.generate_snapshot()
summary = engine.generate_executive_summary()
dashboard = engine.generate_dashboard()
```

## Full pipeline

```text
Repository
  -> Discovery
  -> Repository Index
  -> Aggregation
  -> KPI Engine
  -> Dashboard Snapshot
  -> Executive Summary
  -> DashboardOutput
```

## Configuration

`DashboardEngineConfig` supports:

- repository root
- optional asset roots
- strict discovery
- Green threshold
- Amber threshold
- source label
- current phase label

Example:

```python
from pathlib import Path
from dashboard_engine.api import DashboardEngine, DashboardEngineConfig

config = DashboardEngineConfig(
    repository_root=Path("."),
    asset_roots=(Path("test_cases"),),
    strict_discovery=True,
    green_minimum=80.0,
    amber_minimum=70.0,
    source="repository",
    current_phase="Test Design and Review",
)

dashboard = DashboardEngine(config=config).generate_dashboard()
```

## Public output

`DashboardOutput` contains:

- `snapshot`
- `executive_summary`
- `is_clean`
- JSON-compatible `to_dict()`

## CLI

Generate the complete output:

```bash
python3 scripts/generate_dashboard.py
```

Generate all three files:

```bash
python3 scripts/generate_dashboard.py \
  --strict-discovery \
  --output data/dashboard.json \
  --snapshot-output data/dashboard_snapshot.json \
  --summary-output data/executive_summary.json
```

## Exit codes

- `0`: dashboard generated and quality is clean
- `1`: dashboard generated with non-fatal quality issues
- `2`: dashboard generation failed

## Error handling

Filesystem and configuration errors are exposed as:

```text
DashboardEngineError
```

The original exception remains available as the chained cause.

## Architectural rule

From Phase 4 onward, presentation code must depend on:

```text
dashboard_engine.api
```

It should not import lower-level Phase 3 packages directly.

This keeps the UI isolated from internal implementation changes.
