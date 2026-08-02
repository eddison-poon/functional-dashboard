---
automation_test_id: MCP-FILESYSTEM-A-014
business_scenario_id: MCP-FILESYSTEM-014
name: Read Multiple Files in One Request
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Filesystem
business_feature: File Reading
requirement_ids:
  - REQ-MCP-FILESYSTEM-014
tags:
  - regression
  - mcp
  - filesystem
  - read-multiple-files
script_path: automation/playwright/tests/mcp/filesystem/test_read_multiple_files.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Read Multiple Files in One Request

## Objective

Verify that an authorised caller can read multiple existing files from allowed filesystem paths in one request.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-FILESYSTEM-014 |
| Business Scenario Name | Read Multiple Files in One Request |
| Coverage | Primary successful path for `mcp-filesystem-read-multiple-files` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation uses controlled filesystem paths and data, produces an observable filesystem result, and can be verified through a supporting filesystem MCP tool. |

## Automation Scope

Automates successful reading of multiple small controlled files. Mixed failures, unsupported formats and very large batches are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and UI locators must be confirmed against the deployed system.

## Preconditions

- The caller is authorised to use the filesystem MCP server.
- Two or more supported files exist within allowed directories.
- Each file contains known content.
- The read-multiple-files tool is available.

- `BASE_URL` and allowed test-directory values are externalised.
- Authentication is supplied by a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- All state-changing tests use disposable paths beneath an approved test root.
- Tests must never write to, move or delete uncontrolled paths.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| File paths | Create at least two disposable text files |
| Expected markers | Generate distinct content for each file |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Create multiple files with distinct content markers. | All files exist. |
| 2 | Invoke read-multiple-files with all paths. | The invocation succeeds and returns one result per path. |
| 3 | Map results to paths. | Every requested path has a corresponding result. |
| 4 | Validate content. | Each result contains the marker generated for that file. |

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
- Script path: `automation/playwright/tests/mcp/filesystem/test_read_multiple_files.py`
- Add traceability markers for `MCP-FILESYSTEM-A-014` and `MCP-FILESYSTEM-014`.
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
@pytest.mark.automation_id("MCP-FILESYSTEM-A-014")
@pytest.mark.business_scenario_id("MCP-FILESYSTEM-014")
def test_read_multiple_files(
    page: Page,
    filesystem_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    test_root = os.getenv("FILESYSTEM_TEST_ROOT")

    if not base_url:
        pytest.fail("BASE_URL is required")
    if not test_root:
        pytest.fail("FILESYSTEM_TEST_ROOT is required")

    run_id = f"mcp-filesystem-a-014-{int(time.time())}"
    disposable_path = PurePosixPath(test_root) / run_id
    test_data = filesystem_test_data["read_multiple_files"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-filesystem-read-multiple-files`.
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

- Delete all disposable files.

## Expected Execution Outputs

- pytest result associated with `MCP-FILESYSTEM-A-014`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or UI evidence sufficient for diagnosis
- Created and cleaned disposable filesystem paths
- Execution metadata associated with `MCP-FILESYSTEM-014` and `MCP-FILESYSTEM-A-014`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
