---
automation_test_id: MCP-JIRA-A-006
business_scenario_id: MCP-JIRA-006
name: Batch Create Jira Issues
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Issue Creation
requirement_ids:
  - REQ-MCP-JIRA-006
tags:
  - regression
  - mcp
  - jira
  - batch-create-issues
script_path: automation/playwright/tests/mcp/jira/test_batch_create_issues.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Batch Create Jira Issues

## Objective

Verify that an authorised caller can create multiple Jira issues in one batch using valid issue definitions.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-006 |
| Business Scenario Name | Batch Create Jira Issues |
| Coverage | Primary successful path for `mcp-jira-jira-batch-create-issues` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool operation is repeatable, accepts controlled data, and produces an observable response that can be verified through the Agent UI and a supporting Jira tool or Jira resource view. |

## Automation Scope

Automates successful batch creation of multiple valid issues. Partial failures, transactional behaviour and invalid payloads are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP request fields, response rendering and UI locators must be aligned with the deployed system's accessible labels or approved test IDs.

## Preconditions

- The caller is authenticated and authorised to create issues in the target project.
- The target project and selected issue types exist.
- All mandatory fields for each issue are known.
- The Jira MCP server and batch-create-issues tool are available.

- The Playwright base URL is supplied through configuration.
- Authentication is established using a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the test agent.
- Environment-specific resource identifiers are externalised.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Project key | Read from configuration |
| Issue payloads | Generate at least two unique summaries and valid mandatory fields |

Do not include credentials, tokens or secrets in source code or committed test data.

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Ensure the batch-create-issues tool is available. | The tool is listed and selectable. |
| 2 | Invoke the tool with multiple generated issue payloads. | The invocation succeeds and returns one result per payload. |
| 3 | Retrieve each returned issue. | Every issue exists and matches its submitted summary and issue type. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and result headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request controls.
- Use an approved stable `data-testid` with `page.get_by_test_id()` when accessible locators are not unique.
- Do not use generated CSS classes, positional selectors or deep XPath expressions.
- Confirm application-specific locators during implementation; do not infer them from the screenshot alone.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_batch_create_issues.py`
- Include markers or metadata for `MCP-JIRA-A-006` and `MCP-JIRA-006`.
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
@pytest.mark.automation_id("MCP-JIRA-A-006")
@pytest.mark.business_scenario_id("MCP-JIRA-006")
def test_batch_create_issues(page: Page) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    unique_value = f"MCP-JIRA-A-006-{int(time.time())}"

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent and invoke `mcp-jira-jira-batch-create-issues`.
    # Populate application-specific request fields using stable locators.

    # Assert
    # Verify the MCP invocation succeeds.
    # Verify the resulting Jira state through a supporting tool or Jira UI.
    expect(page).to_have_url(lambda url: bool(url))
```

The outline intentionally avoids inventing application-specific selectors or an unknown MCP request schema.

## Cleanup

- Delete all issues created by the batch after verification.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-006`
- Playwright trace, screenshot or video according to failure-evidence policy
- pytest-compatible JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-006` and `MCP-JIRA-A-006`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
