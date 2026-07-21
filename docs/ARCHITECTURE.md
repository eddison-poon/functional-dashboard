# Architecture Specification v1.0

## Purpose

The platform transforms operational functional-testing data into a governed,
read-only engineering intelligence experience.

## Processing flow

```text
Jira / execution sources
        ↓
Connector layer
        ↓
Mapping and canonicalisation
        ↓
Reusable requirements and test definitions
        ↓
Immutable execution records
        ↓
Snapshot and metrics engine
        ↓
data/snapshot.json
        ↓
GitHub Pages dashboard
```

## Product hierarchy

```text
Agent Hub Platform
    ↓
Capability Group
    ↓
Capability
    ↓
Feature
    ↓
Scenario
    ↓
Jira Requirement
    ↓
Test Definition
    ↓
Execution History
```

The left navigator deliberately stops at two levels:

1. Capability Group
2. Capability

Feature, Scenario, and Execution investigation occurs in the right workspace.

## Canonical identity rules

- Jira ID: stable business requirement reference, for example `AHP-1042`.
- Manual Test ID: reusable manual test definition, for example `MCP-JIRA-M-001`.
- Automation Test ID: reusable automation definition, for example `MCP-JIRA-A-001`.
- Execution ID: immutable run record, for example `EXE-20260722-175841-0002`.

## Release hierarchy

```text
Release → Sprint → Build
```

## Environments

DEV, SIT, UAT, PPD, PROD.

## Health thresholds

- Green: score >= 80
- Amber: score >= 70 and < 80
- Red: score < 70

The implementation is configuration-driven through `config/health_rules.json`.

## Snapshot schedule

Scheduled publication occurs at 12:00 and 18:00. Manual GitHub Actions
`workflow_dispatch` publication is also supported.

## Jira governance

All tickets use the fixed Jira component:

```text
AI Platform - AgentHub
```

Classification dimensions are derived from governed Jira labels and
`config/label_mapping.json`.
