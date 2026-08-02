---
scenario_id: MCP-JIRA-008
scenario_name: Create Jira Service Customer Request
business_feature: Service Request Creation
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

`mcp-jira-jira-create-customer-request`

### Business Objective

Verify that an authorised customer can create a Jira Service Management request using valid request details.

### Preconditions

- The caller is authenticated as an eligible customer or authorised agent.
- The target service desk and request type exist.
- Mandatory request fields are known.
- The Jira MCP server and create-customer-request tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Service desk reference | A valid service desk ID or key |
| Request type | A valid customer request type |
| Summary and details | Unique valid request content |
| Additional required fields | Valid values according to the request type |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the service desk, request type and valid required fields. | The request is accepted. |
| 2 | Confirm customer request creation. | A service request is created and a request key or ID is returned. |
| 3 | Retrieve or inspect the created request. | The request contains the submitted request type, summary and details. |

### Overall Expected Result

A new Jira Service Management customer request is created successfully with the submitted values.
