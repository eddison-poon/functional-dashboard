---
scenario_id: MCP-JIRA-011
scenario_name: Add Comment to Jira Service Request
business_feature: Service Request Comments
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

`mcp-jira-jira-create-service-desk-request-comment`

### Business Objective

Verify that an authorised caller can add a supported comment to an existing Jira Service Management request.

### Preconditions

- The caller is authenticated and authorised to comment on the target request.
- The target service request exists.
- The comment visibility option is valid when supported.
- The Jira MCP server and service-desk request comment tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Request reference | A valid service request key or ID |
| Comment body | A unique non-empty value |
| Visibility | A valid public or internal setting when applicable |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the request reference and valid comment details. | The request is accepted. |
| 2 | Confirm comment creation. | A new request comment is created and a success response or identifier is returned. |
| 3 | Retrieve or inspect request comments. | The comment is present with the submitted body and visibility. |

### Overall Expected Result

A new comment is added successfully to the intended Jira Service Management request.
