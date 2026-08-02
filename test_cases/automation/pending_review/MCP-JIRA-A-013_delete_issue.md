---
automation_test_id: MCP-JIRA-A-013
business_scenario_id: MCP-JIRA-013
name: Delete Existing Jira Issue
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Issue Management
requirement_ids:
  - REQ-MCP-JIRA-013
tags:
  - regression
  - mcp
  - jira
  - delete-issue
script_path: automation/playwright/tests/mcp/jira/test_delete_issue.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Delete Existing Jira Issue

## Objective

Verify that an authorised caller can delete a disposable Jira issue.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-013 |
| Business Scenario Name | Delete Existing Jira Issue |
| Coverage | Primary successful path for `mcp-jira-jira-delete-issue` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool operation is repeatable, accepts controlled data, and produces an observable response that can be verified through the Agent UI and a supporting Jira tool or Jira resource view. |

## Automation Scope

Automates deletion of a disposable issue. Subtask handling, protected projects and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP request fields, response rendering and UI locators must be aligned with the deployed system's accessible labels or approved test IDs.

## Preconditions

- The caller is authenticated and authorised to delete issues.
- A disposable issue exists and may safely be removed.
- The Jira MCP server and delete-issue tool are available.

- The Playwright base URL is supplied through configuration.
- Authentication is established using a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the test agent.
- Environment-specific resource identifiers are externalised.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Create a disposable issue during setup and retain its key |

Do not include credentials, tokens or secrets in source code or committed test data.

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Create a disposable Jira issue. | A valid issue key is available. |
| 2 | Invoke delete-issue with the disposable issue key. | The invocation succeeds. |
| 3 | Invoke get-issue using the deleted key. | The result indicates not found, deleted or inaccessible. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and result headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request controls.
- Use an approved stable `data-testid` with `page.get_by_test_id()` when accessible locators are not unique.
- Do not use generated CSS classes, positional selectors or deep XPath expressions.
- Confirm application-specific locators during implementation; do not infer them from the screenshot alone.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_delete_issue.py`
- Include markers or metadata for `MCP-JIRA-A-013` and `MCP-JIRA-013`.
- Use fixtures for browser context, authentication, test agent setup and disposable Jira data.
- Use `expect()` assertions and observable state instead of `page.wait_for_timeout()`.
- Use environment variables or pytest configuration for URLs, credentials, project keys and user identifiers.
- Add type hints to helpers and fixtures where practical.
- Execution results and evidence belong to the Execution record.

## Suggested Python Test Outline

```python
from __future__ import annotations

import os
import time

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.jira
@pytest.mark.automation_id("MCP-JIRA-A-013")
@pytest.mark.business_scenario_id("MCP-JIRA-013")
def test_delete_issue(page: Page) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    unique_value = f"MCP-JIRA-A-013-{int(time.time())}"

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent and invoke `mcp-jira-jira-delete-issue`.
    # Populate application-specific request fields using stable locators.

    # Assert
    # Verify the MCP invocation succeeds.
    # Verify the resulting Jira state through a supporting tool or Jira UI.
    expect(page).to_have_url(lambda url: bool(url))
```

The outline intentionally avoids inventing application-specific selectors or an unknown MCP request schema.

## Cleanup

- None; deletion is the expected final state.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-013`
- Playwright trace, screenshot or video according to failure-evidence policy
- pytest-compatible JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-013` and `MCP-JIRA-A-013`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
