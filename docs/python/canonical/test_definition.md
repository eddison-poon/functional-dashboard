## Purpose

The `test_definition.py` module defines reusable manual and automated
tests covering canonical Scenarios.

A Test Definition describes how a business behaviour can be verified.
It does not represent a specific execution or result.

## Responsibilities

The module:

1. Defines a unified Test Definition model.
2. Supports Manual and Automation test types.
3. Links every Test Definition to one Scenario.
4. Defines structured manual test steps.
5. Validates automation framework and script information.
6. Validates Test Definition lifecycle status.
7. Supports Test Definition versioning.
8. Normalizes tags and preconditions.
9. Produces JSON-compatible dictionaries.
10. Reconstructs objects from dictionary input.
11. Prevents mutation after creation.

## Non-Responsibilities

The module does not:

- Confirm that the referenced Scenario exists.
- Execute manual or automated tests.
- Store execution results.
- Calculate pass rates.
- Calculate manual or automation coverage.
- Read source code repositories.
- Trigger automation pipelines.
- Build dashboard snapshots.

Cross-record references will be validated by the canonical validator.

## Unified Model

Manual and automated tests share one entity:

```text
Test Definition
    ├── MANUAL
    └── AUTOMATION
