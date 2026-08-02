---
scenario_id: MCP-JIRA-025
scenario_name: Retrieve Jira Service Desk by ID
business_feature: Service Desk Metadata
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

`mcp-jira-jira-get-service-desk-by-id`

### Business Objective

Verify that an authorised caller can retrieve a Jira Service Management service desk using its identifier.

### Preconditions

- The caller is authenticated and authorised to access the target service desk.
- A known service desk exists.
- The Jira MCP server and get-service-desk-by-id tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Service desk ID | A valid service desk identifier |
| Expected project key or name | Known service desk metadata |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the service desk ID. | The request is accepted. |
| 2 | Retrieve the service-desk response. | The requested service desk is returned. |
| 3 | Inspect the metadata. | The identifier and expected project key or name match. |

### Overall Expected Result

The intended Jira Service Management service desk is returned successfully with the expected identity and metadata.
