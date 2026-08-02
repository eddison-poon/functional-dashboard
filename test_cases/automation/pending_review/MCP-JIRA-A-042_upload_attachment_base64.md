---
automation_test_id: MCP-JIRA-A-042
business_scenario_id: MCP-JIRA-042
name: Upload Base64 Attachment to Jira Issue
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: MCP
business_module: Jira
business_feature: Attachment Management
requirement_ids:
  - REQ-MCP-JIRA-042
tags:
  - regression
  - mcp
  - jira
  - upload-attachment-base64
script_path: automation/playwright/tests/mcp/jira/test_upload_attachment_base64.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Upload Base64 Attachment to Jira Issue

## Objective

Verify that an authorised caller can upload a valid Base64-encoded file attachment to an existing Jira issue.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-042 |
| Business Scenario Name | Upload Base64 Attachment to Jira Issue |
| Coverage | Primary successful path for `mcp-jira-jira-upload-attachment-base64` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled test data, produces an observable Jira state change, and can be verified using another Jira MCP tool or the Jira user interface. |

## Automation Scope

Automates successful upload of a small permitted non-sensitive file. Invalid Base64, prohibited file types, oversized files, malware scanning and permission failures are excluded.

The implementation will use Playwright for Python with pytest. Exact MCP input fields, response presentation and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to add attachments to the target issue.
- The target Jira issue exists and attachments are enabled.
- The file type and size are permitted by Jira configuration.
- A valid Base64-encoded test file and matching filename are available.
- The Jira MCP server and upload-attachment-base64 tool are available.

- `BASE_URL` and Jira environment values are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target MCP tool is enabled for the configured test agent.
- Disposable test data is used for state-changing operations.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Issue reference | Create a disposable issue during setup |
| Filename | Generate `mcp-jira-a-042-${timestamp}.txt` |
| File content | Generate a unique non-sensitive text marker |
| Base64 payload | Encode the generated content in Python at runtime |
| Expected MIME type | Use `text/plain` when required by the tool contract |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Create a disposable issue and generate unique text content. | The issue key and original text are available. |
| 2 | Encode the text content as Base64 in Python. | A non-empty valid Base64 string is produced. |
| 3 | Invoke upload-attachment-base64 with issue, filename and encoded content. | The invocation succeeds and returns attachment confirmation or metadata. |
| 4 | Inspect the target issue attachments. | The generated filename is present with expected metadata. |
| 5 | Retrieve the attachment when supported. | Decoded content matches the generated original text. |

## Locator Strategy

- Prefer `page.get_by_role()` for tool dialogs, rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for request fields.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/mcp/jira/test_upload_attachment_base64.py`
- Add traceability markers for `MCP-JIRA-A-042` and `MCP-JIRA-042`.
- Use fixtures for authentication, agent setup, disposable Jira resources and cleanup.
- Use Playwright `expect()` assertions and observable state instead of fixed waits.
- State-changing tests must include reliable cleanup.
- Produce JUnit XML or JSON output for dashboard ingestion.

## Suggested Tool-Specific Python Skeleton

```python
from __future__ import annotations

import os
import time
import base64
from typing import Any

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.regression
@pytest.mark.mcp
@pytest.mark.jira
@pytest.mark.automation_id("MCP-JIRA-A-042")
@pytest.mark.business_scenario_id("MCP-JIRA-042")
def test_upload_attachment_base64(
    page: Page,
    jira_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    test_data = jira_test_data["upload_attachment_base64"]

    original_content = f"{automation_id}-{int(time.time())}"
    encoded_content = base64.b64encode(
        original_content.encode("utf-8")
    ).decode("ascii")

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `mcp-jira-jira-upload-attachment-base64`.
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

- Delete the disposable issue after verification; this removes the uploaded attachment.

## Expected Execution Outputs

- pytest result associated with `MCP-JIRA-A-042`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- MCP invocation response or Jira UI evidence sufficient for diagnosis
- Execution metadata associated with `MCP-JIRA-042` and `MCP-JIRA-A-042`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
