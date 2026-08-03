# Phase 3.3 — Aggregation Engine

## Objective

Phase 3.3 converts the relationship-aware `RepositoryIndex` from Phase 3.2
into management-ready summary counts.

This is the first reporting layer, but it deliberately stops before KPI
health thresholds, execution status, environment readiness, and release
readiness.

## Input

```text
dashboard_engine.indexing.RepositoryIndex
```

## Output

```text
dashboard_engine.aggregation.RepositoryAggregation
```

## Aggregations produced

### Asset lifecycle totals

For each category:

- Business Scenarios
- Manual Test Definitions
- Automation Test Definitions
- All Test Definitions

The engine reports:

- total
- pending review
- reviewed
- published
- unknown

### Scenario coverage

The engine calculates:

- Manual coverage
- Automation coverage
- Overall test-definition coverage

Coverage is based on whether a Business Scenario has at least one linked
Test Definition of the relevant kind.

### Scenario composition

Each Scenario is classified into exactly one category:

- Manual only
- Automation only
- Manual and Automation
- No Test Definitions

### Upstream quality counts

The aggregation retains:

- Phase 3.2 indexing issue count
- ignored asset count

## Coverage calculation

```text
Coverage % = Covered Scenarios / Total Scenarios × 100
```

A repository containing zero Scenarios returns `0.0%` rather than raising a
division-by-zero error.

## Important interpretation

Coverage does not mean execution completion or test success.

For example:

- Manual coverage means at least one Manual Test Definition is linked.
- Automation coverage means at least one Automation Test Definition is linked.
- Overall coverage means at least one Manual or Automation Test Definition is linked.

Execution results are not part of Phase 3.3.

## Run

```bash
python3 scripts/build_repository_aggregation.py
```

Write JSON output:

```bash
python3 scripts/build_repository_aggregation.py \
  --strict-discovery \
  --output data/repository_aggregation.json
```

## Exit codes

- `0`: no upstream discovery or indexing issues;
- `1`: one or more upstream issues were reported.

Aggregation itself remains deterministic and will process all valid indexed
assets even when upstream non-fatal issues exist.

## Phase boundary

Phase 3.3 does not calculate:

- pass rate;
- fail rate;
- blocked rate;
- execution completion;
- environment health;
- release readiness;
- Green, Amber, or Red status;
- trends.

Those belong to Phase 3.4 and later.
