---
scenario_id: ARK-SANDBOX-001
scenario_name: Claim Available Sandbox from Pool
business_feature: Sandbox Allocation
business_module: Ark Sandbox
priority: High
test_type: Functional
category: Sandbox Integration
manual_exists: true
automation_exists: true
review_status: Pending
jira_id: null
scenario_pattern: null
owner: null
created_by: null
created_date: 2026-07-31
reviewed_by: null
reviewed_date: null
published_date: null
---

### Tool

`ark-sandbox-claim-sandbox-from-pool`

### Business Objective

Verify that an authorised caller can claim an available warm sandbox from the configured pool.

### Preconditions

- The caller is authenticated and authorised to claim sandboxes.
- At least one eligible sandbox is available in the configured pool.
- The requested pool or sandbox class is valid.
- The claim-sandbox-from-pool tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Pool reference | A valid configured sandbox pool |
| Claim metadata | Valid optional labels, namespace or purpose when supported |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit a valid pool reference and supported claim metadata. | The request is accepted. |
| 2 | Confirm the sandbox claim. | A sandbox identifier, namespace and successful claim status are returned. |
| 3 | Retrieve the claimed sandbox information. | The sandbox is assigned to the caller and reports a usable state. |

### Overall Expected Result

An available sandbox is claimed successfully from the intended pool and is ready for use.
