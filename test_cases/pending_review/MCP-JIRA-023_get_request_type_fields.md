---
scenario_id: MCP-JIRA-023
scenario_name: Retrieve Jira Service Request Type Fields
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

`mcp-jira-jira-get-request-type-fields`

### Business Objective

Verify that an authorised caller can retrieve the fields configured for a Jira Service Management request type.

### Preconditions

- The caller is authenticated and authorised to access the target service desk.
- A known request type exists and has configured fields.
- The Jira MCP server and get-request-type-fields tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Service desk reference | A valid service desk ID when required |
| Request type ID | A valid request type identifier |
| Expected field | A known field name or ID |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the service desk and request type references. | The request is accepted. |
| 2 | Retrieve the request-type fields. | A collection of configured fields is returned. |
| 3 | Inspect the field metadata. | The expected field is included with its required or optional state when supported. |

### Overall Expected Result

The configured fields for the intended request type are returned successfully and include the expected field.
