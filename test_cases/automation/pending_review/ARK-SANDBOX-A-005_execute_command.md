---
automation_test_id: ARK-SANDBOX-A-005
business_scenario_id: ARK-SANDBOX-005
name: Execute Shell Command in Sandbox
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: SANDBOX
business_module: Ark Sandbox
business_feature: Sandbox Command Execution
requirement_ids:
  - REQ-ARK-SANDBOX-005
tags:
  - regression
  - sandbox
  - ark-sandbox
  - execute-command
script_path: automation/playwright/tests/sandbox/ark/test_execute_command.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Execute Shell Command in Sandbox

## Objective

Verify that an authorised caller can execute an approved shell command inside a running sandbox and retrieve its output.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | ARK-SANDBOX-005 |
| Business Scenario Name | Execute Shell Command in Sandbox |
| Coverage | Primary successful path for `ark-sandbox-execute-command` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled sandbox identifiers and data, produces observable lifecycle, command, log or file-transfer results, and can be verified through supporting Ark Sandbox tools. |

## Automation Scope

Automates one safe deterministic command. Privileged commands, long-running processes, destructive commands and interactive sessions are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact tool request fields, response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to execute commands.
- The target sandbox is running and usable.
- The command is permitted by the sandbox execution policy.
- The execute-command tool is available.

- `BASE_URL`, sandbox namespace, pool, image and approved test paths are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target Ark Sandbox tool is enabled for the configured test agent.
- State-changing tests use disposable sandboxes and files.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Sandbox reference | Create or claim a disposable sandbox |
| Command | Generate a safe command that prints `ARK-SANDBOX-A-005-${timestamp}` |
| Expected output | The generated marker |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Ensure the sandbox is ready. | The sandbox reports a usable state. |
| 2 | Invoke execute-command with the safe generated command. | The invocation succeeds. |
| 3 | Validate command result. | Exit status is successful and stdout contains the expected marker. |

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
- Script path: `automation/playwright/tests/sandbox/ark/test_execute_command.py`
- Add traceability markers for `ARK-SANDBOX-A-005` and `ARK-SANDBOX-005`.
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
@pytest.mark.automation_id("ARK-SANDBOX-A-005")
@pytest.mark.business_scenario_id("ARK-SANDBOX-005")
def test_execute_command(
    page: Page,
    ark_sandbox_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"ark-sandbox-a-005-{int(time.time())}"
    test_data = ark_sandbox_test_data["execute_command"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `ark-sandbox-execute-command`.
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

- pytest result associated with `ARK-SANDBOX-A-005`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- Tool invocation response or sandbox UI evidence sufficient for diagnosis
- Created, claimed and cleaned sandbox identifiers
- Execution metadata associated with `ARK-SANDBOX-005` and `ARK-SANDBOX-A-005`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
