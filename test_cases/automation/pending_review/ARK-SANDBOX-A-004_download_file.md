---
automation_test_id: ARK-SANDBOX-A-004
business_scenario_id: ARK-SANDBOX-004
name: Download File from Sandbox
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: SANDBOX
business_module: Ark Sandbox
business_feature: Sandbox File Transfer
requirement_ids:
  - REQ-ARK-SANDBOX-004
tags:
  - regression
  - sandbox
  - ark-sandbox
  - download-file
script_path: automation/playwright/tests/sandbox/ark/test_download_file.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Download File from Sandbox

## Objective

Verify that an authorised caller can download an existing file from a sandbox.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | ARK-SANDBOX-004 |
| Business Scenario Name | Download File from Sandbox |
| Coverage | Primary successful path for `ark-sandbox-download-file` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled sandbox identifiers and data, produces observable lifecycle, command, log or file-transfer results, and can be verified through supporting Ark Sandbox tools. |

## Automation Scope

Automates download of one small controlled file. Large files, restricted paths, directories and interrupted transfer are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact tool request fields, response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to access the sandbox.
- The target sandbox is running and usable.
- A known file exists at an allowed path inside the sandbox.
- The download-file tool is available.

- `BASE_URL`, sandbox namespace, pool, image and approved test paths are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target Ark Sandbox tool is enabled for the configured test agent.
- State-changing tests use disposable sandboxes and files.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Sandbox reference | Create or claim a disposable sandbox |
| Remote path | Create a unique test file using execute-command or upload-file |
| Expected marker | Generate `ARK-SANDBOX-A-004-${timestamp}` |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Prepare a known file in the sandbox. | The remote file exists. |
| 2 | Invoke download-file. | The invocation succeeds and returns file data. |
| 3 | Validate returned content. | The expected marker or checksum matches. |

## Locator Strategy

- Prefer `page.get_by_role()` for dialogs, tool rows, buttons and response headings.
- Prefer `page.get_by_label()` or `page.get_by_placeholder()` for sandbox, pool, command and file controls.
- Use `page.get_by_test_id()` only for approved stable test IDs.
- Avoid generated CSS classes, positional selectors and deep XPath expressions.
- Confirm application-specific locators during implementation.

## Sandbox Safety Rules

- Use only disposable or explicitly approved test sandboxes.
- Never execute destructive, privileged, persistence, network-scanning or security-bypass commands.
- Use short TTL values for test-created sandboxes where supported.
- Upload and download only non-sensitive fixture files.
- Use unique sandbox names, file paths and markers for every execution.
- Cleanup only resources created or claimed by the same test run.
- Capture sandbox IDs and namespaces in fixtures so cleanup runs after assertion failure.
- Never delete shared, production or manually managed sandboxes.

## Python Implementation Notes

- Framework: Playwright for Python
- Test runner: pytest
- Script path: `automation/playwright/tests/sandbox/ark/test_download_file.py`
- Add traceability markers for `ARK-SANDBOX-A-004` and `ARK-SANDBOX-004`.
- Use fixtures for authentication, Agent setup, sandbox allocation and cleanup.
- Keep credentials, pool names, namespaces and image names in secure configuration.
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
@pytest.mark.sandbox
@pytest.mark.ark_sandbox
@pytest.mark.automation_id("ARK-SANDBOX-A-004")
@pytest.mark.business_scenario_id("ARK-SANDBOX-004")
def test_download_file(
    page: Page,
    ark_sandbox_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"ark-sandbox-a-004-{int(time.time())}"
    test_data = ark_sandbox_test_data["download_file"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `ark-sandbox-download-file`.
    # Populate the exact request using `test_data` and `run_id`.
    # Submit the invocation.

    # Assert
    # Verify invocation success.
    # Verify the sandbox result described in
    # 'Automated Flow and Assertions' above.
    expect(page).to_have_url(lambda value: bool(value))
```

The skeleton intentionally avoids inventing the deployed application's exact request schema or selectors.

## Cleanup

- Delete the disposable sandbox after verification.

## Expected Execution Outputs

- pytest result associated with `ARK-SANDBOX-A-004`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- Tool invocation response or sandbox UI evidence sufficient for diagnosis
- Created, claimed and cleaned sandbox identifiers
- Execution metadata associated with `ARK-SANDBOX-004` and `ARK-SANDBOX-A-004`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
