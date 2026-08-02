---
automation_test_id: MCP-JIRA-A-029
business_scenario_id: MCP-JIRA-029
name: Retrieve Sprints from Jira Board
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Sprint Management
requirement_ids:
  - REQ-MCP-JIRA-029
tags:
  - regression
  - mcp
  - jira
  - get-sprints-from-board
script_path: automation/playwright/tests/mcp/jira/test_get_sprints_from_board.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Retrieve Sprints from Jira Board

## Objective

Verify that an authorised caller can retrieve sprints associated with a Jira board.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-029 |
| Business Scenario Name | Retrieve Sprints from Jira Board |
| Coverage | Primary successful path for `mcp-jira-jira-get-sprints-from-board` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation is repeatable, accepts controlled data or identifiers, and returns an observable result that can be verified through another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates positive retrieval of board sprints. Pagination, board administration and inaccessible sprints are excluded.

The implementation will use Playwright for Python with pytest. Exact request fields, MCP response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to view the target board.
- The board exists and contains at least one known sprint.
- The Jira MCP server and get-sprints-from-board tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is provided by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Board ID | Read from test configuration |
| Expected sprint | Read from test configuration |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Invoke get-sprints-from-board with the configured board ID. | The invocation succeeds and returns sprints. |
| 2 | Inspect sprint identities. | The expected sprint is present. |
| 3 | Validate board association. | Returned data corresponds to the configured board. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_get_sprints_from_board.py`
- Add traceability markers for `MCP-JIRA-A-029` and `MCP-JIRA-029`.
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
@pytest.mark.automation_id("MCP-JIRA-A-029")
@pytest.mark.business_scenario_id("MCP-JIRA-029")
def test_get_sprints_from_board(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    # Arrange
    page.goto(base_url)
    test_data = jira_test_data["get_sprints_from_board"]

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-get-sprints-from-board`.
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

- pytest result associated with `MCP-JIRA-A-029`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-029` and `MCP-JIRA-A-029`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
