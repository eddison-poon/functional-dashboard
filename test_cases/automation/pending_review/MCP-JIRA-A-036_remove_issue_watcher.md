---
automation_test_id: MCP-JIRA-A-036
business_scenario_id: MCP-JIRA-036
name: Remove Watcher from Jira Issue
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
  - REQ-MCP-JIRA-036
tags:
  - regression
  - mcp
  - jira
  - remove-issue-watcher
script_path: automation/playwright/tests/mcp/jira/test_remove_issue_watcher.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Remove Watcher from Jira Issue

## Objective

Verify that an authorised caller can remove an existing watcher from a Jira issue.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-036 |
| Business Scenario Name | Remove Watcher from Jira Issue |
| Coverage | Primary successful path for `mcp-jira-jira-remove-issue-watcher` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation is repeatable, accepts controlled data or identifiers, and returns an observable result that can be verified through another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates removal of one existing watcher. Non-watchers, invalid users and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact request fields, MCP response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to manage issue watchers.
- The target issue exists.
- The target user is currently watching the issue.
- The Jira MCP server and remove-issue-watcher tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is provided by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Read from configuration or create during setup |
| Watcher reference | Add a known watcher during setup |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Ensure the expected user is watching the issue. | The watcher is present. |
| 2 | Invoke remove-issue-watcher. | The invocation succeeds. |
| 3 | Invoke get-issue-watchers. | The removed watcher is absent. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_remove_issue_watcher.py`
- Add traceability markers for `MCP-JIRA-A-036` and `MCP-JIRA-036`.
- Use fixtures for authentication, agent setup, disposable Jira resources and cleanup.
- Use Playwright `expect()` and observable state instead of fixed waits.
- Produce JUnit XML or JSON output for dashboard ingestion.

## Suggested Tool-Specific Python Skeleton

```python
from __future__ import annotations

import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.jira
@pytest.mark.automation_id("MCP-JIRA-A-036")
@pytest.mark.business_scenario_id("MCP-JIRA-036")
def test_remove_issue_watcher(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    # Arrange
    page.goto(base_url)
    test_data = jira_test_data["remove_issue_watcher"]

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-remove-issue-watcher`.
    # Populate the exact MCP request fields from `test_data`.
    # Submit the invocation.

    # Assert
    # Verify the invocation reports success.
    # Verify the tool-specific Jira state described in
    # 'Automated Flow and Assertions' above.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton avoids inventing the deployed application's exact MCP request schema or selectors.

## Cleanup

- None; removal is the expected final state, or restore watcher if required by shared data policy.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-036`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-036` and `MCP-JIRA-A-036`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
