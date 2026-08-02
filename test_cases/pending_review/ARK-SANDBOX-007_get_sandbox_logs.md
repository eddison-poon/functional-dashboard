---
scenario_id: ARK-SANDBOX-007
scenario_name: Retrieve Sandbox Logs
business_feature: Sandbox Observability
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

`ark-sandbox-get-sandbox-logs`

### Business Objective

Verify that an authorised caller can retrieve logs from an existing sandbox.

### Preconditions

- The caller is authenticated and authorised to view sandbox logs.
- The target sandbox exists and has generated a known log marker.
- The get-sandbox-logs tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox reference | A valid running sandbox |
| Expected log marker | A unique value emitted during setup |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the sandbox reference and supported log options. | The request is accepted. |
| 2 | Retrieve sandbox logs. | A log response is returned. |
| 3 | Inspect the logs. | The expected marker is present with supported timestamp or stream metadata. |

### Overall Expected Result

Logs for the intended sandbox are returned successfully and include the known marker.
