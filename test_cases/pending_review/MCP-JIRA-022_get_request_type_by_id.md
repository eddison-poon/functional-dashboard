---
scenario_id: MCP-JIRA-022
scenario_name: Retrieve Jira Service Request Type by ID
business_feature: Service Request Metadata
business_module: Jira
priority: High
test_type: Functional
category: MCP Integration
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

### MCP Tool

`mcp-jira-jira-get-request-type-by-id`

### Business Objective

Verify that an authorised caller can retrieve a Jira Service Management request type using its identifier.

### Preconditions

- The caller is authenticated and authorised to access the target service desk.
- A known request type exists.
- The Jira MCP server and get-request-type-by-id tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Request type ID | A valid request type identifier |
| Expected name | Known request type name |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the request type ID. | The request is accepted. |
| 2 | Retrieve the request-type response. | The requested request type is returned. |
| 3 | Inspect returned metadata. | The identifier and expected name match the configured request type. |

### Overall Expected Result

The intended Jira Service Management request type is returned successfully with the expected identity and name.
