---
automation_test_id: MCP-CONFLUENCE-A-020
business_scenario_id: MCP-CONFLUENCE-020
name: Upload Attachment to Confluence Page
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Confluence
business_feature: Attachment Management
requirement_ids:
  - REQ-MCP-CONFLUENCE-020
tags:
  - regression
  - mcp
  - confluence
  - upload-attachment
script_path: automation/playwright/tests/mcp/confluence/test_upload_attachment.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Upload Attachment to Confluence Page

## Objective

Verify that an authorised caller can upload a valid file attachment to an existing Confluence page.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-CONFLUENCE-020 |
| Business Scenario Name | Upload Attachment to Confluence Page |
| Coverage | Primary successful path for `mcp-confluence-upload-attachment` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled data, produces an observable Confluence result, and can be verified through another Confluence MCP tool or Confluence resource view. |

## Automation Scope

Automates successful upload of a small permitted non-sensitive file. Invalid types, oversized files, malware scanning and permission failures are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact MCP request fields, response rendering and UI locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to add attachments to the target page.
- The target page exists inside an approved test space.
- The file type and size comply with Confluence configuration.
- A small non-sensitive test file is available.
- The upload-attachment tool is available.

- `BASE_URL`, Confluence space, page and user values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- State-changing tests use disposable pages, spaces, comments, labels and attachments where practical.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Page reference | Create a disposable page during setup |
| Filename | Generate `mcp-confluence-a-020-${timestamp}.txt` |
| File content | Generate a unique non-sensitive marker |
| MIME type | Use `text/plain` when required |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Create a disposable target page and test file. | The page and file are available. |
| 2 | Invoke upload-attachment. | The invocation succeeds. |
| 3 | Inspect the page attachment list or response. | The generated filename is present. |
| 4 | Retrieve the attachment when supported. | Its content matches the original marker. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for page, space, comment, label and attachment controls.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Confluence Safety Rules

- Use only spaces and pages explicitly approved for automation testing.
- Create disposable pages and spaces for destructive or state-changing operations.
- Never delete or modify uncontrolled production spaces, pages, comments or attachments.
- Use unique names and markers for every execution.
- Cleanup only resources created by the same test run.
- Capture created resource IDs in fixtures so cleanup still runs after assertion failure.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/confluence/test_upload_attachment.py`
- Add traceability markers for `MCP-CONFLUENCE-A-020` and `MCP-CONFLUENCE-020`.
- Use fixtures for authentication, Agent setup, disposable Confluence resources and cleanup.
- Keep credentials and tokens in secure environment or CI secret storage.
- Use Playwright `expect()` and observable response state instead of fixed waits.
- Produce JUnit XML or JSON output for dashboard ingestion.

## Suggested Python Skeleton

```python
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.confluence
@pytest.mark.automation_id("MCP-CONFLUENCE-A-020")
@pytest.mark.business_scenario_id("MCP-CONFLUENCE-020")
def test_upload_attachment(
    page: Page,
    confluence_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"mcp-confluence-a-020-{int(time.time())}"
    test_data = confluence_test_data["upload_attachment"]

    fixture_path = Path(test_data["fixture_path"])
    if not fixture_path.is_file():
        pytest.fail(f"Attachment fixture does not exist: {fixture_path}")

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-confluence-upload-attachment`.
    # Populate the exact MCP request using `test_data` and `run_id`.
    # Submit the invocation.

    # Assert
    # Verify invocation success.
    # Verify the Confluence state described in
    # 'Automated Flow and Assertions' above.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's exact request schema or selectors.

## Cleanup

- Delete the disposable page after verification; this removes the attachment.

## Expected Execution Outputs

- pytest result associated with `MCP-CONFLUENCE-A-020`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Confluence UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-CONFLUENCE-020` and `MCP-CONFLUENCE-A-020`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
