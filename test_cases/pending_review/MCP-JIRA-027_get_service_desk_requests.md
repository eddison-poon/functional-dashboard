---
scenario_id: MCP-JIRA-027
scenario_name: Retrieve Jira Service Desk Requests
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

`mcp-jira-jira-get-service-desk-requests`

### Business Objective

Verify that an authorised caller can retrieve Jira Service Management requests matching supported filters.

### Preconditions

- The caller is authenticated and authorised to view service requests.
- At least one known request exists that matches the configured filter.
- The Jira MCP server and get-service-desk-requests tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Filter criteria | Supported service desk, status or participant filter |
| Expected request | A known request key or ID |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit supported request filter criteria. | The request is accepted. |
| 2 | Retrieve the request collection. | A collection of matching service requests is returned. |
| 3 | Inspect the results. | The expected request is included and satisfies the filter. |

### Overall Expected Result

Matching Jira Service Management requests are returned successfully and include the expected request.
