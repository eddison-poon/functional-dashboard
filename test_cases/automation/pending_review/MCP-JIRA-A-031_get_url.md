---
automation_test_id: MCP-JIRA-A-031
business_scenario_id: MCP-JIRA-031
name: Retrieve Jira Resource URL
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Resource Navigation
requirement_ids:
  - REQ-MCP-JIRA-031
tags:
  - regression
  - mcp
  - jira
  - get-url
script_path: automation/playwright/tests/mcp/jira/test_get_url.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Retrieve Jira Resource URL

## Objective

Verify that the MCP tool returns a valid Jira URL for a supported resource reference.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-031 |
| Business Scenario Name | Retrieve Jira Resource URL |
| Coverage | Primary successful path for `mcp-jira-jira-get-url` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation is repeatable, accepts controlled data or identifiers, and returns an observable result that can be verified through another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates URL generation and validation for one supported accessible resource. Anonymous access and expired links are excluded.

The implementation will use Playwright for Python with pytest. Exact request fields, MCP response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to view the target Jira resource.
- The target Jira issue or supported resource exists.
- The Jira MCP server and get-url tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is provided by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Resource reference | Read from test configuration or create during setup |
| Expected host | Read from `JIRA_BASE_URL` or equivalent configuration |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Invoke get-url with the configured resource. | The invocation succeeds and returns a URL. |
| 2 | Validate URL format. | The URL is well formed and uses the expected host. |
| 3 | Navigate to or inspect the URL when permitted. | It identifies or opens the intended Jira resource. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_get_url.py`
- Add traceability markers for `MCP-JIRA-A-031` and `MCP-JIRA-031`.
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
@pytest.mark.automation_id("MCP-JIRA-A-031")
@pytest.mark.business_scenario_id("MCP-JIRA-031")
def test_get_url(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    # Arrange
    page.goto(base_url)
    test_data = jira_test_data["get_url"]

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-get-url`.
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

- None.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-031`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-031` and `MCP-JIRA-A-031`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
