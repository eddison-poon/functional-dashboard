---
automation_test_id: MCP-JIRA-A-002
business_scenario_id: MCP-JIRA-002
name: Add Watcher to Jira Issue
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Issue Watchers
requirement_ids:
  - REQ-MCP-JIRA-002
tags:
  - regression
  - mcp
  - jira
  - add-issue-watcher
script_path: automation/playwright/tests/mcp/jira/test_add_issue_watcher.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Add Watcher to Jira Issue

## Objective

Verify that an authorised caller can add a valid user as a watcher of an existing Jira issue.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-002 |
| Business Scenario Name | Add Watcher to Jira Issue |
| Coverage | Primary successful path for `mcp-jira-jira-add-issue-watcher` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool operation is repeatable, accepts controlled data, and produces an observable response that can be verified through the Agent UI and a supporting Jira tool or Jira resource view. |

## Automation Scope

Automates the primary successful path for adding one valid watcher. Duplicate watcher requests, invalid users and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP request fields, response rendering and UI locators must be aligned with the deployed system's accessible labels or approved test IDs.

## Preconditions

- The caller is authenticated and authorised to manage issue watchers.
- The target issue exists.
- The target user exists and is not already watching the issue.
- The Jira MCP server and add-issue-watcher tool are available.

- The Playwright base URL is supplied through configuration.
- Authentication is established using a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the test agent.
- Environment-specific resource identifiers are externalised.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Read from test configuration or create during setup |
| Watcher account ID | Read from secure non-secret test configuration |

Do not include credentials, tokens or secrets in source code or committed test data.

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Ensure the add-issue-watcher tool is available. | The tool is listed and selectable. |
| 2 | Invoke the tool with the issue and watcher references. | The invocation succeeds. |
| 3 | Inspect the issue or watcher response through a supported tool or UI. | The expected user is shown as a watcher. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and result headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request controls.
- Use an approved stable `data-testid` with `page.get_by_test_id()` when accessible locators are not unique.
- Do not use generated CSS classes, positional selectors or deep XPath expressions.
- Confirm application-specific locators during implementation; do not infer them from the screenshot alone.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_add_issue_watcher.py`
- Include markers or metadata for `MCP-JIRA-A-002` and `MCP-JIRA-002`.
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
@pytest.mark.automation_id("MCP-JIRA-A-002")
@pytest.mark.business_scenario_id("MCP-JIRA-002")
def test_add_issue_watcher(page: Page) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    unique_value = f"MCP-JIRA-A-002-{int(time.time())}"

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent and invoke `mcp-jira-jira-add-issue-watcher`.
    # Populate application-specific request fields using stable locators.

    # Assert
    # Verify the MCP invocation succeeds.
    # Verify the resulting Jira state through a supporting tool or Jira UI.
    expect(page).to_have_url(lambda url: bool(url))
```

The outline intentionally avoids inventing application-specific selectors or an unknown MCP request schema.

## Cleanup

- Remove the watcher through an approved cleanup mechanism when available, or use a disposable issue.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-002`
- Playwright trace, screenshot or video according to failure-evidence policy
- pytest-compatible JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-002` and `MCP-JIRA-A-002`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
