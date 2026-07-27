---
automation_test_id: MCP-JIRA-A-001
business_scenario_id: MCP-JIRA-001
name: Create Jira ticket with mandatory fields
status: APPROVED
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: TYPESCRIPT
capability: MCP
business_module: JIRA
business_feature: CREATE_TICKET
requirement_ids:
  - REQ-MCP-JIRA-001
tags:
  - regression
  - mcp
  - jira
  - create-ticket
script_path: automation/playwright/tests/mcp/jira/create_jira_ticket.spec.ts
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Create Jira Ticket with Mandatory Fields

## Objective

Verify automatically that an authorised user can create a Jira ticket using all mandatory fields and that the created ticket displays a unique Jira ID and the submitted values.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-001 |
| Business Scenario Name | Create Jira ticket |
| Coverage | Successful UI path using valid mandatory data |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The path is repeatable, has observable outcomes and is valuable for regression. |

## Automation Scope

Automates the successful Jira ticket creation path through the UI. It verifies dialog availability, mandatory field entry, successful submission, Jira ID creation and submitted values. Validation, permission and downstream failure paths are excluded.

## Preconditions

- The target environment is available.
- The Playwright base URL is configured externally.
- A secure authenticated session or supported login method is available.
- The test account can create issues in the target project.
- The target project supports the selected issue type.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Project | Read from secure environment configuration |
| Issue Type | `Task` |
| Summary | Generate from Automation Test ID and timestamp |
| Description | `Created by MCP-JIRA-A-001 Playwright automation.` |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Open Jira with authenticated state. | Jira is displayed and the user is authenticated. |
| 2 | Open the Create Issue dialog. | The dialog and mandatory controls are visible. |
| 3 | Select project and issue type. | Selected values are displayed. |
| 4 | Enter mandatory data. | Controls contain accepted values without validation errors. |
| 5 | Submit the form. | Creation succeeds through confirmation or navigation. |
| 6 | Inspect the created ticket. | A unique Jira ID and submitted values are displayed. |

## Locator Strategy

Prefer `getByRole`, `getByLabel` and approved test IDs. Do not use generated CSS classes or deep XPath expressions.

## Playwright Implementation Outline

```typescript
import { test, expect } from '@playwright/test';

test(
  'MCP-JIRA-A-001 create Jira ticket with mandatory fields',
  { tag: ['@MCP-JIRA-A-001', '@MCP-JIRA-001', '@regression'] },
  async ({ page }) => {
    const projectKey = process.env.JIRA_PROJECT_KEY;
    if (!projectKey) throw new Error('JIRA_PROJECT_KEY is required');

    const summary = `MCP-JIRA-A-001-${Date.now()}`;

    await page.goto('/');

    await test.step('Open Create Issue', async () => {
      await page.getByRole('button', { name: /create/i }).click();
      await expect(page.getByRole('dialog', { name: /create issue/i })).toBeVisible();
    });

    await test.step('Populate mandatory fields', async () => {
      await page.getByLabel(/project/i).fill(projectKey);
      await page.getByLabel(/issue type/i).selectOption({ label: 'Task' });
      await page.getByLabel(/summary/i).fill(summary);
      await page.getByLabel(/description/i).fill(
        'Created by MCP-JIRA-A-001 Playwright automation.',
      );
    });

    await test.step('Submit and verify', async () => {
      await page.getByRole('button', { name: /^create$/i }).click();
      await expect(page.getByText(summary)).toBeVisible();
    });
  },
);
```

The locators are illustrative and must be aligned to the actual application.

## Cleanup

Delete or transition created test data when project policy requires it.

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | Example Automation Engineer | YYYY-MM-DD | Submitted |
| Reviewer | Example Reviewer | YYYY-MM-DD | Approved |
