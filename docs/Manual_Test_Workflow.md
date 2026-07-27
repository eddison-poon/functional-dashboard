# Manual Test Definition Workflow

## 1. Purpose

This workflow governs creation, review and optional publication of Manual Test Definitions derived from approved Business Scenarios. Phase 2.6 uses a simple file-based process.

## 2. Flow

```text
Approved Business Scenario
          ↓
Generate Manual Test Definition
          ↓
test_cases/manual/pending_review/
          ↓
Manual review
          ↓
test_cases/manual/reviewed/
          ↓
Optional external publication
          ↓
test_cases/manual/published/
```

## 3. Prerequisite

The parent Business Scenario must exist and be approved. The relationship is recorded through `business_scenario_id`. No step-level mapping is required.

## 4. Generate

Inputs:

```text
docs/Manual_Testing_Standards.md
docs/Approved_Manual_Test_Definition_Example.md
test_cases/templates/manual_test_definition_template.md
prompts/Manual_Test_Definition_Generator.md
Approved Business Scenario Markdown file
```

Output:

```text
test_cases/manual/pending_review/<manual_test_id>_<short_name>.md
```

New definitions use `status: DRAFT`.

## 5. Review

Review with `docs/Manual_Test_Review_Checklist.md`.

### Approved

1. Change status to `APPROVED`.
2. Complete the Approval Record.
3. Move the file to `test_cases/manual/reviewed/`.

### Returned for Update

Keep the same ID and file in `pending_review`, apply comments, and resubmit.

### Rejected

Reject when the definition duplicates an existing test, lies outside the parent scenario, adds unsupported behaviour, or requires complete redesign.

## 6. Publish

Publication is optional until Jira or another test-management integration exists.

When published:

- create or update the external artefact;
- record its `jira_id` or equivalent reference;
- retain `manual_test_id`;
- move the file to `test_cases/manual/published/`.

A publication failure must not remove the approved source from `reviewed`.

## 7. Change Handling

### Minor Correction

Retain the ID. Repeat review when the meaning may be affected.

### Parent Scenario Change

1. Find definitions with the matching `business_scenario_id`.
2. Review each for impact.
3. Update affected files.
4. Return changed files to `pending_review`.
5. Retain IDs unless an old definition is retired and replaced by a materially different one.

Parent-level traceability is sufficient; no exact step mapping is required.

### Retirement

Use `status: RETIRED`. Never reuse the ID.

## 8. Execution

An approved definition may have many Executions:

```text
Manual Test Definition
        ├── Execution 1
        ├── Execution 2
        └── Execution 3
```

Environment, build, cycle, status, actual result, evidence, defects, executor and time belong to Execution.

## 9. Directory Structure

```text
test_cases/
├── templates/
│   └── manual_test_definition_template.md
└── manual/
    ├── pending_review/
    ├── reviewed/
    └── published/
```

## 10. Phase 2.6 Completion Criteria

```text
Approved Business Scenario
        ↓
Generated Manual Test Definition
        ↓
Review completed
        ↓
Approved file moved to reviewed
        ↓
Definition available for execution
```