---
scenario_id: MCP-JIRA-003
scenario_name: Add Participants to Jira Service Request
business_feature: Service Request Participants
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

`mcp-jira-jira-add-request-participants`

### Business Objective

Verify that an authorised caller can add valid participants to an existing Jira Service Management request.

### Preconditions

- The caller is authenticated and authorised to manage request participants.
- The target service request exists.
- The participant users exist and are eligible to be added.
- The Jira MCP server and add-request-participants tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Request reference | A valid service request key or ID |
| Participant references | One or more valid user account identifiers |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target request and participant references. | The request is accepted. |
| 2 | Confirm participant addition. | The tool reports successful completion. |
| 3 | Retrieve or inspect the request participants. | The submitted users are associated with the request. |

### Overall Expected Result

The intended users are added successfully as participants of the target service request.
