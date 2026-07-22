# Scenario Model

## Purpose

The `scenario.py` module defines the canonical representation of one
independently verifiable business behaviour.

A Scenario translates one or more requirements into a behaviour that
can later be covered by manual tests, automated tests, or both.

## Responsibilities

The module:

1. Defines the canonical Scenario structure.
2. Requires a stable Scenario ID.
3. Links each Scenario to exactly one Feature.
4. Links each Scenario to one or more Requirements.
5. Validates controlled values.
6. Normalizes tags, preconditions, and reference IDs.
7. Produces JSON-compatible dictionaries.
8. Reconstructs Scenario objects from dictionaries.
9. Prevents mutation after creation.

## Non-Responsibilities

The module does not:

- Create or validate Feature records.
- Create or validate Requirement records.
- Confirm that referenced IDs exist.
- Create Manual Test Definitions.
- Create Automation Test Definitions.
- Store execution results.
- Calculate manual or automation status.
- Calculate coverage, health, or readiness.
- Build dashboard snapshots.

Cross-record reference validation will be performed later by the
canonical validation module.

## Scenario Definition

A Scenario represents:

> One independently verifiable business behaviour.

A Scenario is not:

- A Jira story.
- A test case.
- A test execution.
- A defect.
- An acceptance test result.

## Relationships

```text
Feature
    1
    |
    | owns
    |
    many
Scenario
    many
    |
    | validates
    |
    many
Requirement
