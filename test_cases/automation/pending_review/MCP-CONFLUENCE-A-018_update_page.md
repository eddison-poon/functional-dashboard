---
automation_test_id: MCP-CONFLUENCE-A-018
business_scenario_id: MCP-CONFLUENCE-018
name: Update Existing Confluence Page
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Confluence
business_feature: Page Management
requirement_ids:
  - REQ-MCP-CONFLUENCE-018
tags:
  - regression
  - mcp
  - confluence
  - update-page
script_path: automation/playwright/tests/mcp/confluence/test_update_page.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Update Existing Confluence Page

## Objective

Verify that an authorised caller can update supported fields of an existing Confluence page.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-CONFLUENCE-018 |
| Business Scenario Name | Update Existing Confluence Page |
| Coverage | Primary successful path for `mcp-confluence-update-page` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled data, produces an observable Confluence result, and can be verified through another Confluence MCP tool or Confluence resource view. |

## Automation Scope

Automates one successful update. Version conflicts, invalid content and permission failures are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and UI locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to edit the page.
- A disposable page exists.
- Current version information is available when required.
- The update-page tool is available.

- `BASE_URL`, Confluence space, page and user values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- State-changing tests use disposable pages, spaces, comments, labels and attachments where practical.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Page reference | Create during setup |
| Updated content | Generate `MCP-CONFLUENCE-A-018 ${timestamp}` |
| Version | Retrieve during setup when required |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Prepare a disposable page. | The page exists. |
| 2 | Invoke update-page. | The invocation succeeds. |
| 3 | Invoke get-page. | The generated updated content is returned. |

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
- Script path: `automation/playwright/tests/mcp/confluence/test_update_page.py`
- Add traceability markers for `MCP-CONFLUENCE-A-018` and `MCP-CONFLUENCE-018`.
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
@pytest.mark.automation_id("MCP-CONFLUENCE-A-018")
@pytest.mark.business_scenario_id("MCP-CONFLUENCE-018")
def test_update_page(
    page: Page,
    confluence_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"mcp-confluence-a-018-{int(time.time())}"
    test_data = confluence_test_data["update_page"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-confluence-update-page`.
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

- Delete the disposable page.

## Expected Execution Outputs

- pytest result associated with `MCP-CONFLUENCE-A-018`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Confluence UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-CONFLUENCE-018` and `MCP-CONFLUENCE-A-018`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
