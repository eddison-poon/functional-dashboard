---
automation_test_id: MCP-JIRA-A-040
business_scenario_id: MCP-JIRA-040
name: Update Existing Jira Issue Fields
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Issue Management
requirement_ids:
  - REQ-MCP-JIRA-040
tags:
  - regression
  - mcp
  - jira
  - update-issue
script_path: automation/playwright/tests/mcp/jira/test_update_issue.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Update Existing Jira Issue Fields

## Objective

Verify that an authorised caller can update supported fields on an existing Jira issue using valid values.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-040 |
| Business Scenario Name | Update Existing Jira Issue Fields |
| Coverage | Primary successful path for `mcp-jira-jira-update-issue` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled test data, produces an observable Jira state change, and can be verified using another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates successful update of supported editable fields on a disposable issue. Invalid field values, restricted fields, concurrent modification and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP input fields, response presentation and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to edit the target issue.
- A disposable existing Jira issue is available.
- The fields selected for update are editable in the issue's current context.
- Valid field values and any required field identifiers are known.
- The Jira MCP server and update-issue tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- Disposable test data is used for state-changing operations.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Create a disposable issue during setup |
| Updated summary | Generate `MCP-JIRA-A-040 ${timestamp}` |
| Updated description | Generate stable automation content |
| Original values | Capture during setup for comparison and cleanup |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Create or retrieve a disposable issue and capture its current values. | The issue key and original values are available. |
| 2 | Invoke update-issue with generated valid updates. | The invocation succeeds. |
| 3 | Invoke get-issue for the same issue. | The updated fields match the generated values. |
| 4 | Compare untouched fields. | Fields not included in the request retain their original values. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_update_issue.py`
- Add traceability markers for `MCP-JIRA-A-040` and `MCP-JIRA-040`.
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
@pytest.mark.automation_id("MCP-JIRA-A-040")
@pytest.mark.business_scenario_id("MCP-JIRA-040")
def test_update_issue(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    test_data = jira_test_data["update_issue"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-update-issue`.
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

- Delete the disposable issue or restore its original values after verification.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-040`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Jira UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-040` and `MCP-JIRA-A-040`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
