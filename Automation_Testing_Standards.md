# Automation Testing Standards

## 1. Purpose

This document defines the minimum governance, design and implementation standards for Playwright-based Automation Test Definitions.

An Automation Test Definition describes what automated behaviour will be verified and how the Playwright implementation should be structured. The Playwright script is the executable implementation of the approved definition.

## 2. Relationship

```text
Requirement
    ↓
Business Scenario
    ├── Manual Test Definition
    └── Automation Test Definition
             ↓
       Playwright Script
             ↓
          Execution
```

Rules:

- One Business Scenario may have zero, one or multiple Automation Test Definitions.
- Every Automation Test Definition references exactly one approved Business Scenario.
- Manual and Automation Test Definitions are sibling artefacts.
- Parent traceability uses `business_scenario_id`.
- Script traceability uses `script_path` plus tags.
- Execution results and evidence belong to Execution records.

## 3. ID and File Naming

Automation Test Definition ID:

```text
<CAPABILITY>-<MODULE>-A-<NNN>
```

Example:

```text
MCP-JIRA-A-001
```

Definition file:

```text
MCP-JIRA-A-001_create_jira_ticket_with_mandatory_fields.md
```

Playwright script:

```text
create_jira_ticket.spec.ts
```

Recommended path:

```text
automation/playwright/tests/<capability>/<module>/<name>.spec.ts
```

## 4. Mandatory Metadata

| Field | Required | Rule |
|---|---:|---|
| automation_test_id | Yes | Unique and compliant with the ID convention |
| business_scenario_id | Yes | Approved parent Business Scenario |
| name | Yes | Clear automated verification purpose |
| status | Yes | Controlled value |
| priority | Yes | Normally inherited |
| test_type | Yes | Normally `FUNCTIONAL` |
| test_level | Yes | Appropriate level |
| automation_framework | Yes | `PLAYWRIGHT` |
| automation_language | Yes | `TYPESCRIPT` unless approved otherwise |
| capability | Yes | Inherit from parent |
| business_module | Yes | Inherit from parent |
| business_feature | Yes | Inherit from parent |
| objective | Yes | Automated verification goal |
| automation_scope | Yes | Included and excluded coverage |
| preconditions | Yes | Reliable setup conditions |
| test_data | Yes | Data values or generation rules |
| requirement_ids | Yes | Preserve traceability |
| tags | Yes | Stable reporting and selection tags |
| script_path | After implementation | Repository-relative path |
| owner | No | Maintaining team or person |

## 5. Status Values

```text
DRAFT
IN_REVIEW
APPROVED
IMPLEMENTED
RETIRED
```

Use `IMPLEMENTED` only when the approved Playwright script exists, passes review, and completes at least one controlled execution successfully.

## 6. Automation Suitability

A path is suitable when it is repeatable, valuable, deterministic enough for reliable assertions, supported by stable data, and feasible in the target environment.

Record one of:

```text
SUITABLE
PARTIALLY_SUITABLE
NOT_CURRENTLY_SUITABLE
```

## 7. Playwright Standards

### Isolation

Each test must run independently and must not depend on another test's execution order.

### Locators

Preferred order:

1. `getByRole`
2. `getByLabel`
3. `getByPlaceholder`
4. stable `getByText`
5. `getByTestId`
6. CSS or XPath only when necessary

Avoid generated classes, deep DOM paths and positional selectors.

### Waiting

Use Playwright auto-waiting and observable state. Avoid fixed `waitForTimeout` sleeps.

### Assertions

Assert business outcomes, not merely successful clicks.

### Test data

Generate unique values where collisions are possible. Keep secrets outside source control.

### Authentication

Use secure environment configuration or storage state. Never commit credentials, tokens or cookies.

### Abstraction

Use page objects, fixtures and helpers only when they provide real reuse.

### Cleanup

Clean persistent data when required. Cleanup failure must not hide the primary test outcome.

## 8. Traceability in Code

Every test must include both IDs in the title, tags or annotations:

```typescript
test(
  'MCP-JIRA-A-001 create Jira ticket with mandatory fields',
  { tag: ['@MCP-JIRA-A-001', '@MCP-JIRA-001', '@regression'] },
  async ({ page }) => {
    // implementation
  },
);
```

Do not create IDs for individual code steps.

## 9. Environment Independence

Externalise base URLs, credentials, project keys and environment-specific data. Do not hard-code build numbers or environment outcomes.

## 10. Evidence

HTML reports, traces, screenshots, videos and logs belong to Automation Execution records or CI artefact storage, not the reusable definition.

## 11. Simplicity Principle

Use the minimum metadata and abstraction required for reliable automation. Do not introduce step-level mapping, custom framework layers or excessive page-object structures without a proven need.
