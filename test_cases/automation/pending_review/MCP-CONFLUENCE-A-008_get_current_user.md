---
automation_test_id: MCP-CONFLUENCE-A-008
business_scenario_id: MCP-CONFLUENCE-008
name: Retrieve Current Authenticated Confluence User
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Confluence
business_feature: User Context
requirement_ids:
  - REQ-MCP-CONFLUENCE-008
tags:
  - regression
  - mcp
  - confluence
  - get-current-user
script_path: automation/playwright/tests/mcp/confluence/test_get_current_user.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Retrieve Current Authenticated Confluence User

## Objective

Verify that the tool returns the correct currently authenticated Confluence user.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-CONFLUENCE-008 |
| Business Scenario Name | Retrieve Current Authenticated Confluence User |
| Coverage | Primary successful path for `mcp-confluence-get-current-user` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled data, produces an observable Confluence result, and can be verified through another Confluence MCP tool or Confluence resource view. |

## Automation Scope

Automates identity retrieval for the configured test user. Anonymous sessions and disabled users are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and UI locators must be confirmed against the deployed system.

## Preconditions

- A valid authenticated Confluence context is configured.
- The expected test-user identity is known.
- The get-current-user tool is available.

- `BASE_URL`, Confluence space, page and user values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- State-changing tests use disposable pages, spaces, comments, labels and attachments where practical.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Expected user identifier | Read from secure non-secret configuration |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Ensure the authenticated test-user context is active. | The session is authenticated. |
| 2 | Invoke get-current-user. | The invocation succeeds. |
| 3 | Validate identity. | The returned identifier matches configuration. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for page, space, comment, label and attachment controls.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Confluence Safety Rules

- Use only spaces and pages explicitly approved for automation testing.
- Create disposable pages and spaces for destructive or state-changing operations.
- Never delete or modify uncontrolled production spaces, pages, comments or attachments.
- Use unique names and markers for every execution.
- Cleanup only resources created by the same test run.
- Capture created resource IDs in fixtures so cleanup still runs after assertion failure.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/confluence/test_get_current_user.py`
- Add traceability markers for `MCP-CONFLUENCE-A-008` and `MCP-CONFLUENCE-008`.
- Use fixtures for authentication, Agent setup, disposable Confluence resources and cleanup.
- Keep credentials and tokens in secure environment or CI secret storage.
- Use Playwright `expect()` and observable response state instead of fixed waits.
- Produce JUnit XML or JSON output for dashboard ingestion.

## Suggested Python Skeleton

```python
from __future__ import annotations

import os
import time
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.confluence
@pytest.mark.automation_id("MCP-CONFLUENCE-A-008")
@pytest.mark.business_scenario_id("MCP-CONFLUENCE-008")
def test_get_current_user(
    page: Page,
    confluence_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"mcp-confluence-a-008-{int(time.time())}"
    test_data = confluence_test_data["get_current_user"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-confluence-get-current-user`.
    # Populate the exact MCP request using `test_data` and `run_id`.
    # Submit the invocation.

    # Assert
    # Verify invocation success.
    # Verify the Confluence state described in
    # 'Automated Flow and Assertions' above.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's exact request schema or selectors.

## Cleanup

- None.

## Expected Execution Outputs

- pytest result associated with `MCP-CONFLUENCE-A-008`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Confluence UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-CONFLUENCE-008` and `MCP-CONFLUENCE-A-008`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
