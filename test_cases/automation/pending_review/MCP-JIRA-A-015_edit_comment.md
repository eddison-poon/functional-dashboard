---
automation_test_id: MCP-JIRA-A-015
business_scenario_id: MCP-JIRA-015
name: Edit Jira Issue Comment
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Comment Management
requirement_ids:
  - REQ-MCP-JIRA-015
tags:
  - regression
  - mcp
  - jira
  - edit-comment
script_path: automation/playwright/tests/mcp/jira/test_edit_comment.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Edit Jira Issue Comment

## Objective

Verify that an authorised caller can edit an existing Jira issue comment with valid updated content.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-015 |
| Business Scenario Name | Edit Jira Issue Comment |
| Coverage | Primary successful path for `mcp-jira-jira-edit-comment` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool operation is repeatable, accepts controlled data, and produces an observable response that can be verified through the Agent UI and a supporting Jira tool or Jira resource view. |

## Automation Scope

Automates successful comment editing. Empty content, comments owned by other users and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP request fields, response rendering and UI locators must be aligned with the deployed system's accessible labels or approved test IDs.

## Preconditions

- The caller is authenticated and authorised to edit the target comment.
- A disposable comment exists and its identifier is known.
- The Jira MCP server and edit-comment tool are available.

- The Playwright base URL is supplied through configuration.
- Authentication is established using a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the test agent.
- Environment-specific resource identifiers are externalised.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Read from configuration or create during setup |
| Comment ID | Create a disposable comment during setup |
| Updated body | Generate `Updated MCP-JIRA-A-015 ${timestamp}` |

Do not include credentials, tokens or secrets in source code or committed test data.

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Prepare a disposable comment. | The comment ID and original body are available. |
| 2 | Invoke edit-comment with generated updated content. | The invocation succeeds. |
| 3 | Invoke get-comments for the issue. | The target comment contains the updated content. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and result headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request controls.
- Use an approved stable `data-testid` with `page.get_by_test_id()` when accessible locators are not unique.
- Do not use generated CSS classes, positional selectors or deep XPath expressions.
- Confirm application-specific locators during implementation; do not infer them from the screenshot alone.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_edit_comment.py`
- Include markers or metadata for `MCP-JIRA-A-015` and `MCP-JIRA-015`.
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
@pytest.mark.automation_id("MCP-JIRA-A-015")
@pytest.mark.business_scenario_id("MCP-JIRA-015")
def test_edit_comment(page: Page) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    unique_value = f"MCP-JIRA-A-015-{int(time.time())}"

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent and invoke `mcp-jira-jira-edit-comment`.
    # Populate application-specific request fields using stable locators.

    # Assert
    # Verify the MCP invocation succeeds.
    # Verify the resulting Jira state through a supporting tool or Jira UI.
    expect(page).to_have_url(lambda url: bool(url))
```

The outline intentionally avoids inventing application-specific selectors or an unknown MCP request schema.

## Cleanup

- Delete the disposable comment after verification.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-015`
- Playwright trace, screenshot or video according to failure-evidence policy
- pytest-compatible JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-015` and `MCP-JIRA-A-015`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
