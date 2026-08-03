# Phase 3.6 — Executive Summary Generator

## Objective

Phase 3.6 converts the Phase 3.5 dashboard snapshot into concise,
management-ready narrative.

The output is suitable for:

- executive dashboard summary;
- daily standup updates;
- QA governance meetings;
- release-readiness discussions.

## Input

```text
dashboard_engine.snapshot.DashboardSnapshot
```

## Output

```text
dashboard_engine.executive_summary.ExecutiveSummary
```

## Summary sections

- Current phase
- Overall health
- Headline
- Key achievements
- Major risks
- Readiness assessment
- Daily standup update

## Overall health rule

Overall health is evaluated from these core repository KPIs:

- Overall Test Coverage
- All Test Review Completion
- Repository Data Quality

Rule:

1. Any Red KPI makes the overall health Red.
2. Otherwise, any Amber KPI makes the overall health Amber.
3. Otherwise, the result is Green.
4. If no applicable KPI exists, the result is Not Applicable.

## Standup format

The generated standup text follows:

```text
Yesterday:
Today:
Blockers:
Testing Health:
```

## Run

```bash
python3 scripts/build_executive_summary.py
```

Write output:

```bash
python3 scripts/build_executive_summary.py \
  --strict-discovery \
  --output data/executive_summary.json
```

Override the phase label:

```bash
python3 scripts/build_executive_summary.py \
  --current-phase "Test Design Review"
```

## Interpretation

Phase 3.6 currently describes repository preparation and review health.

It does not yet include:

- execution pass/fail/blocked results;
- environment readiness;
- defect impact;
- trend movement;
- release decision logic.

Those inputs can be added later without changing the executive-summary contract.
