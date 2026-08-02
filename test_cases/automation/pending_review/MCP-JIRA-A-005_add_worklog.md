---
automation_test_id: MCP-JIRA-A-005
business_scenario_id: MCP-JIRA-005
name: Add Worklog to Jira Issue
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Worklog Management
requirement_ids:
  - REQ-MCP-JIRA-005
tags:
  - regression
  - mcp
  - jira
  - add-worklog
script_path: automation/playwright/tests/mcp/jira/test_add_worklog.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Add Worklog to Jira Issue

## Objective

Verify that an authorised caller can add a valid worklog entry to an existing Jira issue.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-005 |
| Business Scenario Name | Add Worklog to Jira Issue |
| Coverage | Primary successful path for `mcp-jira-jira-add-worklog` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool operation is repeatable, accepts controlled data, and produces an observable response that can be verified through the Agent UI and a supporting Jira tool or Jira resource view. |

## Automation Scope

Automates successful creation of a worklog. Invalid durations, closed issue restrictions and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP request fields, response rendering and UI locators must be aligned with the deployed system's accessible labels or approved test IDs.

## Preconditions

- The caller is authenticated and authorised to log work.
- The target issue exists and time tracking is enabled where required.
- The Jira MCP server and add-worklog tool are available.

- The Playwright base URL is supplied through configuration.
- Authentication is established using a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the test agent.
- Environment-specific resource identifiers are externalised.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Read from configuration or create during setup |
| Time spent | Use a configurable valid duration |
| Description | Generate `MCP-JIRA-A-005-${timestamp}` |

Do not include credentials, tokens or secrets in source code or committed test data.

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Ensure the add-worklog tool is available. | The tool is listed and selectable. |
| 2 | Invoke the tool with valid generated worklog details. | The invocation succeeds and returns a worklog reference. |
| 3 | Inspect issue worklog information through a supported method. | The generated worklog is present with expected values. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and result headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request controls.
- Use an approved stable `data-testid` with `page.get_by_test_id()` when accessible locators are not unique.
- Do not use generated CSS classes, positional selectors or deep XPath expressions.
- Confirm application-specific locators during implementation; do not infer them from the screenshot alone.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_add_worklog.py`
- Include markers or metadata for `MCP-JIRA-A-005` and `MCP-JIRA-005`.
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
@pytest.mark.automation_id("MCP-JIRA-A-005")
@pytest.mark.business_scenario_id("MCP-JIRA-005")
def test_add_worklog(page: Page) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    unique_value = f"MCP-JIRA-A-005-{int(time.time())}"

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent and invoke `mcp-jira-jira-add-worklog`.
    # Populate application-specific request fields using stable locators.

    # Assert
    # Verify the MCP invocation succeeds.
    # Verify the resulting Jira state through a supporting tool or Jira UI.
    expect(page).to_have_url(lambda url: bool(url))
```

The outline intentionally avoids inventing application-specific selectors or an unknown MCP request schema.

## Cleanup

- Delete the generated worklog using the delete-worklog tool.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-005`
- Playwright trace, screenshot or video according to failure-evidence policy
- pytest-compatible JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-005` and `MCP-JIRA-A-005`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
