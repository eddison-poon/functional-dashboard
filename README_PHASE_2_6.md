# Phase 2.6 — Manual Test Definition Package

Repository-ready governance material for Manual Test Definitions.

## Files

```text
docs/
├── Manual_Testing_Standards.md
├── Approved_Manual_Test_Definition_Example.md
├── Manual_Test_Review_Checklist.md
├── Manual_Test_Workflow.md
└── BusinessScenario_to_Manual_Mapping.md

prompts/
└── Manual_Test_Definition_Generator.md

test_cases/
├── templates/
│   └── manual_test_definition_template.md
└── manual/
    ├── pending_review/
    ├── reviewed/
    └── published/
```

## Governance Decision

Phase 2.6 uses parent-level traceability only:

```text
Business Scenario ID → Manual Test Definition
```

No Business Step IDs or step-level mapping IDs are required.
