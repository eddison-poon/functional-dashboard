---
automation_test_id: MCP-GITHUB-A-015
business_scenario_id: MCP-GITHUB-015
name: Retrieve GitHub Repository Contributors
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: GitHub
business_feature: Repository Metadata
requirement_ids:
  - REQ-MCP-GITHUB-015
tags:
  - regression
  - mcp
  - github
  - get-contributors
script_path: automation/playwright/tests/mcp/github/test_get_contributors.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Retrieve GitHub Repository Contributors

## Objective

Verify automatically that an authorised caller can retrieve contributor information for an existing repository with a known contributor, and that the expected contributor is included.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-GITHUB-015 |
| Business Scenario Name | Retrieve GitHub Repository Contributors |
| Coverage | Primary successful path for `mcp-github-get-contributors` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool accepts controlled identifiers and data, returns an observable GitHub result, and can be verified through a supporting GitHub MCP tool or GitHub resource view. |

## Automation Scope

Automates the primary successful path for `mcp-github-get-contributors`. Invalid identifiers, insufficient permissions, rate limits, concurrency conflicts and unsupported options are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated with a GitHub token or session that has the required read permission.
- The target an existing repository with a known contributor exists and is accessible.
- The `mcp-github-get-contributors` tool is available in the GitHub MCP server.

- `BASE_URL`, GitHub owner, repository, organization and user values are externalised.
- Authentication is supplied by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Repository or organization context | Read from environment-specific test configuration |
| Target identifier | A valid owner, repository, number, ID, branch, tag or path required by the tool |
| Expected marker | A known login, SHA, title, tag, path or identifier used for verification |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Submit the valid identifiers required to retrieve contributor information. | The request is accepted without validation or permission errors. |
| 2 | Retrieve the tool response. | A non-error object or collection is returned. |
| 3 | Inspect the returned data. | The expected contributor is included. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for owner, repository, branch, issue, pull request and content fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## GitHub Safety Rules

- Use read-only credentials when the tool does not require mutation.
- Keep expected repository, organization and user identifiers in external configuration.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/github/test_get_contributors.py`
- Add traceability markers for `MCP-GITHUB-A-015` and `MCP-GITHUB-015`.
- Use fixtures for authentication, Agent setup, disposable GitHub resources and cleanup.
- Store tokens and credentials only in secure environment or CI secret configuration.
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
@pytest.mark.github
@pytest.mark.automation_id("MCP-GITHUB-A-015")
@pytest.mark.business_scenario_id("MCP-GITHUB-015")
def test_get_contributors(
    page: Page,
    github_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"mcp-github-a-015-{int(time.time())}"
    test_data = github_test_data["get_contributors"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-github-get-contributors`.
    # Populate the exact MCP request using `test_data` and `run_id`.
    # Submit the invocation.

    # Assert
    # Verify invocation success.
    # Verify that the expected contributor is included.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's exact request schema or selectors.

## Cleanup

- None, unless disposable setup data was created specifically for the test.

## Expected Execution Outputs

- pytest result associated with `MCP-GITHUB-A-015`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or GitHub UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-GITHUB-015` and `MCP-GITHUB-A-015`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
