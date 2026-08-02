---
automation_test_id: ARK-SANDBOX-A-001
business_scenario_id: ARK-SANDBOX-001
name: Claim Available Sandbox from Pool
status: DRAFT
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
automation_framework: PLAYWRIGHT
automation_language: PYTHON
test_runner: PYTEST
capability: SANDBOX
business_module: Ark Sandbox
business_feature: Sandbox Allocation
requirement_ids:
  - REQ-ARK-SANDBOX-001
tags:
  - regression
  - sandbox
  - ark-sandbox
  - claim-sandbox-from-pool
script_path: automation/playwright/tests/sandbox/ark/test_claim_sandbox_from_pool.py
jira_id:
owner: Functional Test Automation Team
---

# Automation Test Definition: Claim Available Sandbox from Pool

## Objective

Verify that an authorised caller can claim an available warm sandbox from the configured pool.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | ARK-SANDBOX-001 |
| Business Scenario Name | Claim Available Sandbox from Pool |
| Coverage | Primary successful path for `ark-sandbox-claim-sandbox-from-pool` |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | SUITABLE |
| Rationale | The operation accepts controlled sandbox identifiers and data, produces observable lifecycle, command, log or file-transfer results, and can be verified through supporting Ark Sandbox tools. |

## Automation Scope

Automates the primary successful pool-claim path. Empty pools, expired claims, invalid pool references and permission failures are excluded.

The implementation will use Playwright for Python with pytest to drive the Agent interface. Exact tool request fields, response rendering and application locators must be confirmed against the deployed system.

## Preconditions

- The caller is authenticated and authorised to claim sandboxes.
- At least one eligible sandbox is available in the configured pool.
- The requested pool or sandbox class is valid.
- The claim-sandbox-from-pool tool is available.

- `BASE_URL`, sandbox namespace, pool, image and approved test paths are externalised.
- Authentication is supplied through a secure pytest fixture or stored browser state.
- The target Ark Sandbox tool is enabled for the configured test agent.
- State-changing tests use disposable sandboxes and files.

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| Pool reference | Read from environment-specific test configuration |
| Claim marker | Generate `ARK-SANDBOX-A-001-${timestamp}` |

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | Invoke claim-sandbox-from-pool with configured pool data. | The invocation succeeds and returns a sandbox reference. |
| 2 | Invoke get-sandbox-info for the returned reference. | The sandbox exists and is assigned. |
| 3 | Validate readiness. | The sandbox status is usable, ready or equivalent. |

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
- Script path: `automation/playwright/tests/sandbox/ark/test_claim_sandbox_from_pool.py`
- Add traceability markers for `ARK-SANDBOX-A-001` and `ARK-SANDBOX-001`.
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
@pytest.mark.automation_id("ARK-SANDBOX-A-001")
@pytest.mark.business_scenario_id("ARK-SANDBOX-001")
def test_claim_sandbox_from_pool(
    page: Page,
    ark_sandbox_test_data: dict[str, Any],
) -> None:
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("BASE_URL is required")

    run_id = f"ark-sandbox-a-001-{int(time.time())}"
    test_data = ark_sandbox_test_data["claim_sandbox_from_pool"]

    # Arrange
    page.goto(base_url)

    # Act
    # Open the configured agent.
    # Select or confirm `ark-sandbox-claim-sandbox-from-pool`.
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

- Delete or release the claimed sandbox according to the environment policy.

## Expected Execution Outputs

- pytest result associated with `ARK-SANDBOX-A-001`
- Playwright trace, screenshot or video according to failure-evidence policy
- JUnit XML or JSON output for dashboard ingestion
- Tool invocation response or sandbox UI evidence sufficient for diagnosis
- Created, claimed and cleaned sandbox identifiers
- Execution metadata associated with `ARK-SANDBOX-001` and `ARK-SANDBOX-A-001`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
