---
scenario_id: MCP-JIRA-024
scenario_name: Retrieve Request Types for Jira Service Desk
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

`mcp-jira-jira-get-request-types-by-service-desk-id`

### Business Objective

Verify that an authorised caller can retrieve request types configured for a Jira Service Management service desk.

### Preconditions

- The caller is authenticated and authorised to access the target service desk.
- The service desk exists and contains at least one known request type.
- The Jira MCP server and get-request-types-by-service-desk-id tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Service desk ID | A valid service desk identifier |
| Expected request type | A known request type ID or name |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the service desk ID. | The request is accepted. |
| 2 | Retrieve the request-type collection. | A collection of request types is returned. |
| 3 | Inspect the collection. | The expected request type is included and associated with the intended service desk. |

### Overall Expected Result

Request types for the intended service desk are returned successfully and include the expected request type.
