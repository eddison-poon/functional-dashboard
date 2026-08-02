---
scenario_id: MCP-JIRA-037
scenario_name: Remove Participants from Jira Service Request
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

`mcp-jira-jira-remove-request-participants`

### Business Objective

Verify that an authorised caller can remove existing participants from a Jira Service Management request.

### Preconditions

- The caller is authenticated and authorised to manage request participants.
- The target service request exists.
- The target users are currently request participants.
- The Jira MCP server and remove-request-participants tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Request reference | A valid service request key or ID |
| Participant references | One or more current participant account identifiers |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the request and participant references. | The request is accepted. |
| 2 | Confirm participant removal. | The tool reports successful completion. |
| 3 | Retrieve or inspect participants. | The removed users are no longer associated with the request. |

### Overall Expected Result

The intended users are removed successfully from the target service request.
