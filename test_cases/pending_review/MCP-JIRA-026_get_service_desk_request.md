---
scenario_id: MCP-JIRA-026
scenario_name: Retrieve Jira Service Desk Request
business_feature: Service Request Retrieval
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

`mcp-jira-jira-get-service-desk-request`

### Business Objective

Verify that an authorised caller can retrieve a specific Jira Service Management request.

### Preconditions

- The caller is authenticated and authorised to view the request.
- The target request exists with known values.
- The Jira MCP server and get-service-desk-request tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Request reference | A valid customer request key or ID |
| Expected summary | Known request summary |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the request reference. | The request is accepted. |
| 2 | Retrieve the request response. | The intended service request is returned. |
| 3 | Inspect the returned values. | The request key or ID and expected summary match. |

### Overall Expected Result

The intended service request is returned successfully with the expected identity and content.
