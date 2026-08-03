# Phase 3.4 — KPI Engine

## Objective

Phase 3.4 converts Phase 3.3 repository aggregations into reusable,
management-ready KPI results with Green, Amber, Red, or Not Applicable status.

## Input

```text
dashboard_engine.aggregation.RepositoryAggregation
```

## Output

```text
dashboard_engine.kpi.RepositoryKpiSet
```

## Default traffic-light thresholds

The project-standard defaults are:

| Status | Percentage |
|---|---:|
| Green | 80% or above |
| Amber | 70% to below 80% |
| Red | Below 70% |
| Not Applicable | Denominator is zero |

Thresholds are configurable and are embedded in each KPI result.

## KPIs produced

### Coverage KPIs

- Manual Coverage
- Automation Coverage
- Overall Test Coverage

### Review completion KPIs

- Scenario Review Completion
- Manual Test Review Completion
- Automation Test Review Completion
- All Test Review Completion

A lifecycle asset is considered review-complete when its state is either:

- `reviewed`
- `published`

### Repository quality KPI

Repository Data Quality measures the proportion of repository assets that were
indexed without indexing or ignored-asset quality issues.

This is a repository-governance KPI, not a functional test execution KPI.

## KPI output fields

Every KPI contains:

- stable key
- management title
- percentage value
- unit
- health status
- direction
- numerator
- denominator
- threshold values
- description

## Run

```bash
python3 scripts/build_repository_kpis.py
```

Write KPI JSON:

```bash
python3 scripts/build_repository_kpis.py \
  --strict-discovery \
  --output data/repository_kpis.json
```

Use custom thresholds:

```bash
python3 scripts/build_repository_kpis.py \
  --green-minimum 85 \
  --amber-minimum 70 \
  --output data/repository_kpis.json
```

## Important interpretation

Phase 3.4 KPIs describe repository preparation and traceability health.

They do not describe:

- execution progress;
- test pass rate;
- failed or blocked executions;
- environment readiness;
- defect health;
- release readiness.

Those require Execution and Defect aggregation in later packages.
