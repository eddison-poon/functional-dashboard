---
automation_test_id: MCP-GITHUB-A-005
business_scenario_id: MCP-GITHUB-005
name: Create GitHub User Repository
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: GitHub
business_feature: Repository Management
requirement_ids:
  - REQ-MCP-GITHUB-005
tags:
  - regression
  - mcp
  - github
  - create-user-repo
script_path: automation/playwright/tests/mcp/github/test_create_user_repo.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Create GitHub User Repository

## Objective

Verify automatically that an authorised caller can create a repository for the authenticated GitHub user account, and that the repository exists under the authenticated user with the submitted settings.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-GITHUB-005 |
| Business Scenario Name | Create GitHub User Repository |
| Coverage | Primary successful path for `mcp-github-create-user-repo` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The tool accepts controlled identifiers and data, returns an observable GitHub result, and can be verified through a supporting GitHub MCP tool or GitHub resource view. |

## Automation Scope

Automates the primary successful path for `mcp-github-create-user-repo`. Invalid identifiers, insufficient permissions, rate limits, concurrency conflicts and unsupported options are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated with the GitHub permissions required for the operation.
- The required parent the authenticated GitHub user account exists and is accessible.
- Unique disposable test data is available.
- The `mcp-github-create-user-repo` tool is available in the GitHub MCP server.

- `BASE_URL`, GitHub owner, repository, organization and user values are externalised.
- Authentication is supplied by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Owner and repository context | Read from secure non-secret test configuration |
| Unique generated value | Generate a value containing `MCP-GITHUB-A-005` and the execution timestamp |
| Operation-specific fields | Supply valid branch, title, body, path, content or settings required by the tool |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Submit valid generated data to create a repository. | The request is accepted without validation or permission errors. |
| 2 | Confirm the creation or upsert operation. | The tool reports successful completion and returns an identifier or updated resource. |
| 3 | Retrieve the resulting GitHub resource. | The repository exists under the authenticated user with the submitted settings. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for owner, repository, branch, issue, pull request and content fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## GitHub Safety Rules

- Use only repositories, branches, pull requests, issues, comments and organizations explicitly approved for automation testing.
- Every state-changing test must use disposable resources or reliably restore the original state.
- Never delete or mutate uncontrolled production repositories, default branches, releases or organizations.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/github/test_create_user_repo.py`
- Add traceability markers for `MCP-GITHUB-A-005` and `MCP-GITHUB-005`.
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
@pytest.mark.automation_id("MCP-GITHUB-A-005")
@pytest.mark.business_scenario_id("MCP-GITHUB-005")
def test_create_user_repo(
    page: Page,
    github_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"mcp-github-a-005-{int(time.time())}"
    test_data = github_test_data["create_user_repo"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-github-create-user-repo`.
    # Populate the exact MCP request using `test_data` and `run_id`.
    # Submit the invocation.

    # Assert
    # Verify invocation success.
    # Verify that the repository exists under the authenticated user with the submitted settings.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's exact request schema or selectors.

## Cleanup

- Delete or restore all disposable resources created by the test using an approved cleanup tool or fixture.

## Expected Execution Outputs

- pytest result associated with `MCP-GITHUB-A-005`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or GitHub UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-GITHUB-005` and `MCP-GITHUB-A-005`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
