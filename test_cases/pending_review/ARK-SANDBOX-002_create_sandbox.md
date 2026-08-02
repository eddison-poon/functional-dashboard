---
scenario_id: ARK-SANDBOX-002
scenario_name: Create New Sandbox
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

`ark-sandbox-create-sandbox`

### Business Objective

Verify that an authorised caller can create a new isolated sandbox using valid configuration.

### Preconditions

- The caller is authenticated and authorised to create sandboxes.
- The requested image, namespace and resource configuration are valid.
- Capacity is available.
- The create-sandbox tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox name | A unique valid name |
| Namespace | A valid approved namespace |
| Image | A permitted sandbox image |
| TTL or lifecycle settings | Valid values when supported |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid sandbox creation details. | The request is accepted. |
| 2 | Confirm sandbox creation. | A sandbox identifier and initial lifecycle state are returned. |
| 3 | Retrieve sandbox information. | The sandbox exists with the submitted name, namespace and image. |
| 4 | Wait for the usable state. | The sandbox reaches ready, running or equivalent status within the allowed time. |

### Overall Expected Result

A new sandbox is created successfully with the submitted configuration and becomes usable.
