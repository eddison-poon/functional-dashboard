# Controlled Vocabularies

## Purpose

The `enums.py` module defines the controlled values used throughout the
Functional Testing Dashboard canonical data model.

Its purpose is to prevent different source systems from introducing
inconsistent values such as:

- Pass
- PASS
- Passed
- Successful
- Success

All external values must eventually be normalized into one governed
canonical value, such as:

- PASSED

## Responsibilities

This module:

1. Defines approved canonical values.
2. Rejects unsupported values.
3. Supports case-insensitive parsing.
4. Supports clean JSON serialization.
5. Keeps source-system mappings separate from canonical definitions.

## Non-Responsibilities

This module does not:

- Connect to Jira.
- Map Jira statuses.
- Calculate test metrics.
- Build dashboard snapshots.
- Validate relationships between canonical entities.

## Controlled Vocabularies

The first version contains:

- RequirementStatus
- TestDefinitionStatus
- ExecutionStatus
- TestType
- Environment
- Priority
- Severity
- ScenarioType
- EvidenceType
- SourceSystem

## Design Rules

### Canonical values use uppercase strings

Example:

```text
PASSED
FAILED
BLOCKED
