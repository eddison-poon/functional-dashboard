---
automation_test_id: MCP-JIRA-A-041
business_scenario_id: MCP-JIRA-041
name: Update Existing Jira Worklog
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
  - REQ-MCP-JIRA-041
tags:
  - regression
  - mcp
  - jira
  - update-worklog
script_path: automation/playwright/tests/mcp/jira/test_update_worklog.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Update Existing Jira Worklog

## Objective

Verify that an authorised caller can update an existing Jira worklog using valid revised values.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-041 |
| Business Scenario Name | Update Existing Jira Worklog |
| Coverage | Primary successful path for `mcp-jira-jira-update-worklog` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled test data, produces an observable Jira state change, and can be verified using another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates successful update of a disposable worklog. Invalid durations, restricted authorship, closed issue limitations and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP input fields, response presentation and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to edit the target worklog.
- A disposable Jira issue exists.
- A disposable worklog exists on the issue and its identifier is known.
- The updated duration, description and timestamp values are valid.
- The Jira MCP server and update-worklog tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- Disposable test data is used for state-changing operations.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Create or configure a disposable Jira issue |
| Worklog ID | Create a worklog during setup using add-worklog |
| Updated duration | Use a configurable valid duration different from the original |
| Updated description | Generate `MCP-JIRA-A-041 ${timestamp}` |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Prepare a disposable worklog and capture its original values. | A valid worklog ID and original data are available. |
| 2 | Invoke update-worklog with generated revised values. | The invocation succeeds. |
| 3 | Invoke get-worklog for the issue. | The target worklog is returned with the revised duration and description. |
| 4 | Validate worklog identity. | The returned worklog reference matches the original worklog ID. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_update_worklog.py`
- Add traceability markers for `MCP-JIRA-A-041` and `MCP-JIRA-041`.
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
@pytest.mark.automation_id("MCP-JIRA-A-041")
@pytest.mark.business_scenario_id("MCP-JIRA-041")
def test_update_worklog(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    test_data = jira_test_data["update_worklog"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-update-worklog`.
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

- Delete the disposable worklog and issue after verification.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-041`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Jira UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-041` and `MCP-JIRA-A-041`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
