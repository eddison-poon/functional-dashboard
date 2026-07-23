# Functional Testing Dashboard — Test Authoring Standards

Version: 1.0  
Status: Phase 2.5 baseline

## 1. Purpose

This standard defines how contributors create test cases for review, Jira publication, registry generation, and dashboard reporting.

## 2. Core model

```text
Business Scenario
├── Manual definition (optional)
├── Automation definition (optional)
└── Many execution records
```

A test definition describes **what must be verified**. Environment, build, tester, date, and result belong to execution records and must not be embedded in the reusable definition.

## 3. File and identifier conventions

| Item | Convention | Example |
|---|---|---|
| File name | Must equal the Scenario ID plus `.md` | `MCP-JIRA-001.md` |
| Scenario ID | Uppercase groups separated by hyphens | `MCP-JIRA-001` |
| Scenario name | Verb + business object/outcome | `Create Jira Issue with Mandatory Fields` |
| Manual ID | Reserved future form | `M-MCP-JIRA-001` |
| Automation ID | Reserved future form | `A-MCP-JIRA-001` |
| Jira ID | Assigned only after successful publication | `QA-1842` |

Scenario IDs are permanent, unique, and must never be reused.

## 4. Required authoring fields

| Field | Required | Rule |
|---|:---:|---|
| `scenario_id` | Yes | Unique canonical ID; must match file name |
| `scenario_name` | Yes | Clear, testable business behaviour |
| `business_feature` | Yes | Functional capability, not an action sentence |
| `business_module` | Yes | Application, product area, or domain |
| `priority` | Yes | `Critical`, `High`, `Medium`, or `Low` |
| `test_type` | Yes | Controlled value listed below |
| `category` | Yes | Reporting grouping such as `MCP Integration` |
| `manual_exists` | Yes | Boolean `true` or `false` |
| `automation_exists` | Yes | Boolean `true` or `false` |
| `review_status` | Yes | Controlled lifecycle status |
| Business Objective | Yes | Purpose and business behaviour |
| Preconditions | Yes | Minimum setup and access conditions |
| Test Steps | Yes | Ordered actions with expected outcomes |
| Overall Expected Result | Yes | Final measurable outcome |

At least one of `manual_exists` or `automation_exists` must be `true`.

## 5. Controlled vocabularies

### Priority

- `Critical`
- `High`
- `Medium`
- `Low`

### Test type

- `Functional`
- `Smoke`
- `Sanity`
- `Regression`
- `Integration`
- `End-to-End`
- `API`
- `UI`

Use one primary test type. Additional classification can be added later through tags or the deferred scenario-pattern enhancement.

### Review status

| Folder | Required status | Meaning |
|---|---|---|
| `pending_review/` | `Pending` | Submitted and awaiting review |
| `reviewed/` | `Approved` | Approved and eligible for Jira publication |
| `published/` | `Published` | Jira ticket created and ID recorded |
| `rejected/` | `Rejected` | Not approved or requires substantial rework |

## 6. Naming rules

Use a specific behaviour and input condition where useful.

Good:

- `Create Jira Issue with Mandatory Fields`
- `Reject Jira Issue Without Summary`
- `Prevent Read-Only User from Creating Jira Issue`

Avoid:

- `Jira Test`
- `Test Case 1`
- `SIT Create Ticket`
- `Automation Login`

Do not include environments, build numbers, dates, pass/fail outcomes, tester names, or temporary campaign labels in scenario names.

## 7. Preconditions

Preconditions describe state, permissions, dependencies, and required data. They should not repeat the execution procedure.

Good:

- The user is authenticated.
- The user has permission to create issues in the target Jira project.
- Jira and the MCP service are available.

Avoid:

- Open Jira and click Create.
- Test in SIT build 102.

## 8. Test steps

Use a table with one action and one observable expected outcome per row.

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid mandatory issue fields through the supported interface. | The request is accepted without validation errors. |
| 2 | Confirm issue creation. | A unique Jira issue key is returned. |

Keep the definition reusable. Interface-specific manual detail and automation implementation detail may be separated later when dedicated Manual and Automation definitions are introduced.

## 9. Expected results

Expected results must be measurable and observable.

Good:

> A new Jira issue is created, a unique issue key is returned, and the issue is visible in the target project.

Avoid:

> Works successfully.

## 10. Manual and automation indicators

- `manual_exists: true` means a manual implementation exists or is intended.
- `automation_exists: true` means an automation implementation exists or is intended.
- These fields do not indicate that execution has occurred.
- Script paths, framework information, automation status, and run results will be handled by later model layers.

## 11. Scenario pattern enhancement

`scenario_pattern` is optional and currently not validated. It is reserved for a later enhancement such as Happy Path, Validation, Boundary, Permission, Integration, Security, Error Handling, or Recovery.

## 12. Submission rules

1. Copy `test_cases/templates/test_case_template.md`.
2. Rename it to the Scenario ID.
3. Complete all mandatory fields and sections.
4. Place it in `test_cases/pending_review/`.
5. Submit through a pull request.
6. Do not assign a Jira ID.
7. Do not move it directly to `published/`.
