---
automation_test_id: MCP-FILESYSTEM-A-007
business_scenario_id: MCP-FILESYSTEM-007
name: Retrieve Filesystem Path Information
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Filesystem
business_feature: Path Metadata
requirement_ids:
  - REQ-MCP-FILESYSTEM-007
tags:
  - regression
  - mcp
  - filesystem
  - get-file-info
script_path: automation/playwright/tests/mcp/filesystem/test_get_file_info.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Retrieve Filesystem Path Information

## Objective

Verify that an authorised caller can retrieve metadata for an existing file or directory within an allowed path.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-FILESYSTEM-007 |
| Business Scenario Name | Retrieve Filesystem Path Information |
| Coverage | Primary successful path for `mcp-filesystem-get-file-info` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation uses controlled filesystem paths and data, produces an observable filesystem result, and can be verified through a supporting filesystem MCP tool. |

## Automation Scope

Automates metadata retrieval for one controlled path. Platform-specific timestamps and permission-bit interpretation are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and UI locators must be confirmed against the deployed system.

## Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target file or directory exists inside an allowed location.
- Expected path metadata is known.
- The get-file-info tool is available.

- `BASE_URL` and allowed test-directory values are externalised.
- Authentication is supplied by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- All state-changing tests use disposable paths beneath an approved test root.
- Tests must never write to, move or delete uncontrolled paths.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Target file | Create a disposable text file with known content |
| Expected size | Calculate from the generated content |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Create a disposable file with known byte content. | The path and expected size are known. |
| 2 | Invoke get-file-info. | The invocation succeeds and returns metadata. |
| 3 | Validate metadata. | The object is identified as a file and its size matches the expected value where reported. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for path and content controls.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Filesystem Safety Rules

- Resolve every generated path beneath the configured disposable test root.
- Reject empty, relative-parent or root-level destructive paths.
- Never use production, home, shared or system directories for destructive tests.
- Use unique per-test directories to prevent parallel execution collisions.
- Cleanup only resources created by the same test execution.
- Record created paths in fixtures so cleanup remains reliable after assertion failure.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/filesystem/test_get_file_info.py`
- Add traceability markers for `MCP-FILESYSTEM-A-007` and `MCP-FILESYSTEM-007`.
- Use fixtures for authentication, agent setup, disposable workspace creation and cleanup.
- Use `pathlib.PurePosixPath` or the platform-approved path representation for generated MCP paths.
- Use Playwright `expect()` and observable response state instead of fixed waits.
- Produce JUnit XML or JSON output for dashboard ingestion.

## Suggested Python Skeleton

```python
from __future__ import annotations

import os
import time
from pathlib import PurePosixPath
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.filesystem
@pytest.mark.automation_id("MCP-FILESYSTEM-A-007")
@pytest.mark.business_scenario_id("MCP-FILESYSTEM-007")
def test_get_file_info(
    page: Page,
    filesystem_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    test_root = os.getenv("FILESYSTEM_TEST_ROOT")

    if not base_url:
        pytest.fail("BASE_URL is required")
    if not test_root:
        pytest.fail("FILESYSTEM_TEST_ROOT is required")

    run_id = f"mcp-filesystem-a-007-{int(time.time())}"
    disposable_path = PurePosixPath(test_root) / run_id
    test_data = filesystem_test_data["get_file_info"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-filesystem-get-file-info`.
    # Populate the exact MCP request using only paths beneath
    # `disposable_path` or the configured approved test root.
    # Submit the invocation.

    # Assert
    # Verify invocation success.
    # Verify the filesystem result described in
    # 'Automated Flow and Assertions' using a supporting MCP tool.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's request schema or selectors.

## Cleanup

- Delete the disposable file.

## Expected Execution Outputs

- pytest result associated with `MCP-FILESYSTEM-A-007`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Created and cleaned disposable filesystem paths
- Execution metadata associated with `MCP-FILESYSTEM-007` and `MCP-FILESYSTEM-A-007`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
