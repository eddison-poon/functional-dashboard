---
scenario_id: ARK-SANDBOX-008
scenario_name: List Available Sandboxes
business_feature: Sandbox Inventory
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

`ark-sandbox-list-sandboxes`

### Business Objective

Verify that an authorised caller can list sandboxes visible within the configured scope.

### Preconditions

- The caller is authenticated and authorised to list sandboxes.
- At least one known test sandbox exists.
- The list-sandboxes tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Filter criteria | Supported namespace, status or owner filter when applicable |
| Expected sandbox | A known sandbox identifier or name |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit supported listing or filter criteria. | The request is accepted. |
| 2 | Retrieve the sandbox collection. | A collection of visible sandboxes is returned. |
| 3 | Inspect the results. | The expected sandbox is included and satisfies the filter. |

### Overall Expected Result

Visible sandboxes are returned successfully and include the expected sandbox.
