---
automation_test_id: MCP-JIRA-A-026
business_scenario_id: MCP-JIRA-026
name: Retrieve Jira Service Desk Request
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Service Request Retrieval
requirement_ids:
  - REQ-MCP-JIRA-026
tags:
  - regression
  - mcp
  - jira
  - get-service-desk-request
script_path: automation/playwright/tests/mcp/jira/test_get_service_desk_request.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Retrieve Jira Service Desk Request

## Objective

Verify that an authorised caller can retrieve a specific Jira Service Management request.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-026 |
| Business Scenario Name | Retrieve Jira Service Desk Request |
| Coverage | Primary successful path for `mcp-jira-jira-get-service-desk-request` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation is repeatable, accepts controlled data or identifiers, and returns an observable result that can be verified through another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates retrieval of one accessible service request. Expanded histories, comments and invalid references are excluded.

The implementation will use Playwright for Python with pytest. Exact request fields, MCP response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to view the request.
- The target request exists with known values.
- The Jira MCP server and get-service-desk-request tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is provided by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Request reference | Read from configuration or create during setup |
| Expected summary | Capture from setup or configuration |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Invoke get-service-desk-request using the configured reference. | The invocation succeeds. |
| 2 | Inspect the returned request identity. | It matches the requested key or ID. |
| 3 | Validate business fields. | The expected summary and request type are returned. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_get_service_desk_request.py`
- Add traceability markers for `MCP-JIRA-A-026` and `MCP-JIRA-026`.
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
@pytest.mark.automation_id("MCP-JIRA-A-026")
@pytest.mark.business_scenario_id("MCP-JIRA-026")
def test_get_service_desk_request(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    # Arrange
    page.goto(base_url)
    test_data = jira_test_data["get_service_desk_request"]

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-get-service-desk-request`.
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

- Delete or close setup data only when created by the test.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-026`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-026` and `MCP-JIRA-A-026`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
