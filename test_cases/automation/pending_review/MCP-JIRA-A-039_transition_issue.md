---
automation_test_id: MCP-JIRA-A-039
business_scenario_id: MCP-JIRA-039
name: Transition Jira Issue to Available Workflow Status
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Workflow Management
requirement_ids:
  - REQ-MCP-JIRA-039
tags:
  - regression
  - mcp
  - jira
  - transition-issue
script_path: automation/playwright/tests/mcp/jira/test_transition_issue.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Transition Jira Issue to Available Workflow Status

## Objective

Verify that an authorised caller can transition an existing Jira issue using an available workflow transition.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-039 |
| Business Scenario Name | Transition Jira Issue to Available Workflow Status |
| Coverage | Primary successful path for `mcp-jira-jira-transition-issue` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled test data, produces an observable Jira state change, and can be verified using another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates one successful workflow transition for a disposable issue. Invalid transitions, missing transition fields, workflow conditions and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP input fields, response presentation and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to transition the target issue.
- The target issue exists in a known workflow status.
- The intended transition is available from the issue's current status.
- All mandatory transition fields are known and can be supplied.
- The Jira MCP server and transition-issue tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- Disposable test data is used for state-changing operations.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Create a disposable issue during setup or read from test configuration |
| Transition ID or name | Retrieve through `mcp-jira-jira-get-transitions` during setup |
| Expected destination status | Read from workflow-specific test configuration |
| Transition fields | Supply from configuration when required |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Prepare an issue in the configured source status. | The issue exists and its current status is confirmed. |
| 2 | Invoke get-transitions and identify the intended transition. | The configured transition is present and selectable. |
| 3 | Invoke transition-issue with the selected transition and required fields. | The invocation succeeds. |
| 4 | Invoke get-issue for the same issue. | The returned issue status matches the expected destination status. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_transition_issue.py`
- Add traceability markers for `MCP-JIRA-A-039` and `MCP-JIRA-039`.
- Use fixtures for authentication, agent setup, disposable Jira resources and cleanup.
- Use Playwright `expect()` assertions and observable state instead of fixed waits.
- State-changing tests must include reliable cleanup.
- Produce JUnit XML or JSON output for dashboard ingestion.

## Suggested Tool-Specific Python Skeleton

```python
from __future__ import annotations

import os
import time
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.jira
@pytest.mark.automation_id("MCP-JIRA-A-039")
@pytest.mark.business_scenario_id("MCP-JIRA-039")
def test_transition_issue(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    test_data = jira_test_data["transition_issue"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-transition-issue`.
    # Populate exact MCP request fields from `test_data`.
    # Submit the invocation.

    # Assert
    # Verify the MCP invocation reports success.
    # Verify the Jira state described in
    # 'Automated Flow and Assertions' above.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's request schema or selectors.

## Cleanup

- Return the issue to its original status when a supported reverse transition exists, or delete the disposable issue.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-039`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Jira UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-039` and `MCP-JIRA-A-039`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
