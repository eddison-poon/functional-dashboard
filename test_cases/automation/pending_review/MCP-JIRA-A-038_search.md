---
automation_test_id: MCP-JIRA-A-038
business_scenario_id: MCP-JIRA-038
name: Search Jira Issues
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Issue Search
requirement_ids:
  - REQ-MCP-JIRA-038
tags:
  - regression
  - mcp
  - jira
  - search
script_path: automation/playwright/tests/mcp/jira/test_search.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Search Jira Issues

## Objective

Verify that an authorised caller can search Jira and retrieve an issue matching a known unique query.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-038 |
| Business Scenario Name | Search Jira Issues |
| Coverage | Primary successful path for `mcp-jira-jira-search` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation is repeatable, accepts controlled data or identifiers, and returns an observable result that can be verified through another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates a positive search using one stable supported query. Ranking, broad result sets, advanced syntax and restricted issues are excluded.

The implementation will use Playwright for Python with pytest. Exact request fields, MCP response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to search the target issue.
- A searchable issue containing a unique known marker exists.
- The Jira MCP server and search tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is provided by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Unique summary marker | Generate a unique value and create a disposable issue |
| Search query | Construct a supported exact-marker query |
| Expected issue key | Capture from setup |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Prepare a searchable issue with a unique marker. | The issue exists and is indexed. |
| 2 | Invoke Jira search with the generated query. | The invocation succeeds and returns results. |
| 3 | Inspect the result keys and summaries. | The setup issue is present and matches the query. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_search.py`
- Add traceability markers for `MCP-JIRA-A-038` and `MCP-JIRA-038`.
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
@pytest.mark.automation_id("MCP-JIRA-A-038")
@pytest.mark.business_scenario_id("MCP-JIRA-038")
def test_search(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    # Arrange
    page.goto(base_url)
    test_data = jira_test_data["search"]

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-search`.
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

- Delete the disposable searchable issue after verification.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-038`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-038` and `MCP-JIRA-A-038`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
