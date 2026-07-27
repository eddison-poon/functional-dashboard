# Manual Testing Standards

## 1. Purpose

This document defines the governance and writing standards for Manual Test Definitions in the Functional Testing Dashboard repository.

A Manual Test Definition describes **how a tester verifies an approved Business Scenario**. It is reusable and must not contain execution results or evidence.

## 2. Canonical Relationship

```text
Requirement
    ↓
Business Scenario
    ↓
Manual Test Definition
    ↓
Execution
```

Rules:

- One Business Scenario may have one or more Manual Test Definitions.
- Every Manual Test Definition references exactly one approved parent Business Scenario.
- Traceability is maintained through `business_scenario_id` only.
- Business Step IDs and step-to-step mapping IDs are not required.
- The definition must preserve, not extend, the approved business behaviour.
- Actual result, evidence, tester, environment, build and execution status belong to Execution.

## 3. Locations

```text
test_cases/manual/pending_review/
test_cases/manual/reviewed/
test_cases/manual/published/
test_cases/templates/manual_test_definition_template.md
```

## 4. File Naming

```text
<manual_test_id>_<short_name>.md
```

Example:

```text
MCP-JIRA-M-001_create_jira_ticket_with_mandatory_fields.md
```

Use lowercase words separated by underscores after the ID. Do not include environment, build or execution date.

## 5. Manual Test Definition ID

```text
<CAPABILITY>-<MODULE>-M-<NNN>
```

Example:

```text
MCP-JIRA-M-001
```

Multiple definitions may share one parent scenario:

```text
Business Scenario: MCP-JIRA-001
- MCP-JIRA-M-001
- MCP-JIRA-M-002
- MCP-JIRA-M-003
```

IDs must be unique and must never be reused.

## 6. Mandatory Metadata

| Field | Required | Rule |
|---|---:|---|
| manual_test_id | Yes | Unique and compliant with the ID convention |
| business_scenario_id | Yes | References one approved Business Scenario |
| name | Yes | Concise verification purpose |
| status | Yes | Approved controlled value |
| priority | Yes | Normally inherited from the parent scenario |
| test_type | Yes | Normally `FUNCTIONAL` |
| test_level | Yes | One applicable approved level |
| capability | Yes | Inherited from the parent scenario |
| business_module | Yes | Inherited from the parent scenario |
| business_feature | Yes | Inherited from the parent scenario |
| objective | Yes | States what is verified |
| preconditions | Yes | `None` only when genuinely unnecessary |
| test_data | Yes | `None` only when genuinely unnecessary |
| postconditions | Yes | Expected end state or `None` |
| requirement_ids | Yes | Preserves parent requirement traceability |
| jira_id | No | Populated after publication when available |
| owner | No | Responsible person or team |

## 7. Controlled Values

### Status

```text
DRAFT
IN_REVIEW
APPROVED
RETIRED
```

New definitions use `DRAFT`.

### Priority

```text
CRITICAL
HIGH
MEDIUM
LOW
```

### Test Type

Normally:

```text
FUNCTIONAL
```

### Test Level

Use one applicable value, such as:

```text
COMPONENT
INTEGRATION
SYSTEM
ACCEPTANCE
```

## 8. Naming Standard

Preferred pattern:

```text
<Verify action or outcome> <under condition>
```

Good:

```text
Create Jira ticket with mandatory fields
Reject Jira ticket creation when summary is missing
Display validation message for an invalid project key
```

Avoid:

```text
Test Jira
Jira test case 1
Verify system works
```

## 9. Objective Standard

Good:

```text
Verify that an authorised user can create a Jira ticket using all mandatory fields and that the created ticket receives a unique Jira ID.
```

Avoid:

```text
Test Jira ticket creation.
```

## 10. Preconditions

Preconditions describe what must already be true before execution.

Good examples:

- The tester has access to the target Jira project.
- The tester is authenticated with create permission.
- Required reference data exists.

Do not put tester actions in Preconditions.

## 11. Test Data

State explicit values or clear selection rules.

| Data Item | Value or Rule |
|---|---|
| Project | An active project accessible to the tester |
| Issue Type | Task |
| Summary | `Phase 2.6 manual test validation` |

Do not include credentials, secrets or sensitive personal data. Do not hide essential data only inside the steps.

## 12. Test Steps

Use:

| Step | Action | Expected Result |
|---:|---|---|

Rules:

- Number sequentially from 1.
- Use one primary tester action per row.
- Start actions with a direct verb.
- Keep actions unambiguous and executable.
- Do not add step IDs for mapping.
- Do not include actual results, evidence or pass/fail status.

Preferred verbs:

```text
Open
Select
Enter
Choose
Click
Submit
Verify
Confirm
Refresh
Navigate
```

Avoid uncertain wording such as `Try to`, `Attempt to`, or `Check whether it works`.

## 13. Expected Results

Expected Results must be objective and observable.

Good:

```text
The ticket is created and a unique Jira ID is displayed.
```

Bad:

```text
The system works correctly.
```

The final Expected Result must prove the objective.

## 14. Positive and Negative Paths

Do not combine materially different behaviours into one oversized definition. Use separate definitions for paths such as:

- successful submission;
- missing mandatory data;
- invalid data;
- insufficient permission;
- downstream failure.

All may reference the same Business Scenario.

## 15. Environment Independence

Do not embed build numbers, releases, execution dates, actual URLs tied to one environment, or execution status. Use generic wording such as:

```text
Open the application in the target test environment.
```

## 16. Definition vs Execution

The following belong to Execution, not the Manual Test Definition:

- environment and build;
- execution cycle;
- actual result;
- evidence;
- executor and timestamp;
- pass, fail or blocked status;
- defect raised from an execution.

## 17. Traceability

Every definition must contain:

```text
business_scenario_id
requirement_ids
```

Phase 2.6 does not require Business Step IDs, Manual Step mapping IDs, or a separate mapping table.

## 18. Approval Quality Gate

A definition is ready for approval when:

- its parent Business Scenario is approved;
- the approved business intent is preserved;
- another tester can execute it without interpretation;
- preconditions and test data are complete;
- actions are sequential and clear;
- Expected Results are measurable;
- execution-specific information is absent;
- naming and ID standards are followed;
- it does not duplicate another active definition.

## 19. Simplicity Principle

Use the minimum structure required for an executable, maintainable and traceable Manual Test Definition. Add complexity only when a proven requirement justifies it.