
# Requirement Model

## Purpose

The `requirement.py` module defines the canonical representation of a
business or technical requirement used by the Functional Testing
Dashboard data engine.

A requirement normally originates from Jira, but the model is not tied
to Jira. Requirements may also originate from CSV files, TestRail,
Zephyr, Xray, or manually governed input.

## Responsibilities

The module:

1. Defines the canonical Requirement structure.
2. Validates mandatory values.
3. Parses controlled vocabularies.
4. Normalizes optional text fields.
5. Normalizes and deduplicates labels.
6. Validates source URLs.
7. Produces JSON-compatible dictionaries.
8. Reconstructs Requirement objects from dictionaries.

## Non-Responsibilities

The module does not:

- Connect to Jira.
- Translate raw Jira statuses.
- Map components to capabilities.
- Build scenarios.
- Calculate testing health.
- Validate relationships with other entities.
- Write dashboard snapshots.

## Canonical Fields

| Field | Required | Description |
|---|---:|---|
| requirement_id | Yes | Stable requirement identifier |
| title | Yes | Requirement title |
| source_system | Yes | Originating source |
| requirement_type | Yes | Requirement classification |
| status | Yes | Canonical lifecycle status |
| priority | Yes | Canonical priority |
| description | No | Requirement description |
| source_project | No | Source project identifier |
| source_url | No | Link to the source record |
| component | No | Source component or area |
| labels | No | Unique normalized labels |
| release | No | Release identifier |
| sprint | No | Sprint identifier |
| owner | No | Requirement owner |
| active | Yes | Whether the record is active |

## Business Rules

### Requirement ID

`requirement_id` must:

- be present;
- be a string;
- contain at least one non-whitespace character;
- not exceed 100 characters.

The model does not force Jira formatting such as `AHP-1042`, because
future sources may use different identifier formats.

### Title

`title` must:

- be present;
- contain at least one non-whitespace character;
- not exceed 300 characters.

### Description

`description` is optional.

Blank descriptions are stored as `null`.

### Controlled Values

The following fields use canonical enums:

- source_system
- requirement_type
- status
- priority

Parsing is case-insensitive.

Source-specific aliases remain the responsibility of future mapping
modules.

### Labels

Labels are:

- trimmed;
- converted to lowercase;
- deduplicated;
- returned in their original first-seen order;
- limited to non-empty string values.

Example:

```json
["Regression", " mcp ", "regression", ""]
