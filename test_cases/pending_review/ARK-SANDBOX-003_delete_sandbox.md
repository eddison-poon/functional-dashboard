---
scenario_id: ARK-SANDBOX-003
scenario_name: Delete Existing Sandbox
business_feature: Sandbox Lifecycle
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

`ark-sandbox-delete-sandbox`

### Business Objective

Verify that an authorised caller can permanently delete a disposable sandbox.

### Preconditions

- The caller is authenticated and authorised to delete sandboxes.
- A disposable sandbox exists and may safely be removed.
- The sandbox reference is known.
- The delete-sandbox tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox reference | A disposable sandbox ID, name or namespace reference |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable sandbox reference. | The request is accepted. |
| 2 | Confirm sandbox deletion. | The tool reports successful deletion or a terminal deleted state. |
| 3 | Attempt to retrieve the sandbox information. | The sandbox is not returned as active or usable. |

### Overall Expected Result

The intended disposable sandbox is deleted successfully and is no longer available.
