---
scenario_id: ARK-SANDBOX-006
scenario_name: Retrieve Sandbox Information
business_feature: Sandbox Inspection
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

`ark-sandbox-get-sandbox-info`

### Business Objective

Verify that an authorised caller can retrieve metadata and lifecycle information for an existing sandbox.

### Preconditions

- The caller is authenticated and authorised to view the sandbox.
- The target sandbox exists.
- Expected sandbox metadata is known.
- The get-sandbox-info tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox reference | A valid sandbox ID, name or namespace |
| Expected metadata | Known name, namespace, image or lifecycle state |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the sandbox reference. | The request is accepted. |
| 2 | Retrieve sandbox information. | A sandbox information object is returned. |
| 3 | Inspect the metadata. | The returned identifier, name, namespace and status match the target sandbox. |

### Overall Expected Result

Information for the intended sandbox is returned successfully and matches its known state.
