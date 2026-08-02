---
scenario_id: MCP-JIRA-039
scenario_name: Transition Jira Issue to Available Workflow Status
business_feature: Workflow Management
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

`mcp-jira-jira-transition-issue`

### Business Objective

Verify that an authorised caller can transition an existing Jira issue using an available workflow transition.

### Preconditions

- The caller is authenticated and authorised to transition the target issue.
- The target issue exists in a known workflow status.
- The intended transition is available from the issue's current status.
- All mandatory transition fields are known and can be supplied.
- The Jira MCP server and transition-issue tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid disposable Jira issue key or ID |
| Transition reference | A valid transition ID or name available from the current issue status |
| Transition fields | Valid values for any mandatory transition fields |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Retrieve the transitions available for the target issue. | The intended transition is returned as available. |
| 2 | Submit the issue reference, transition reference and any mandatory fields to the transition-issue tool. | The request is accepted without validation or permission errors. |
| 3 | Confirm the transition request. | The tool reports successful completion. |
| 4 | Retrieve the updated issue. | The issue status matches the destination status associated with the selected transition. |

### Overall Expected Result

The intended Jira issue is transitioned successfully to the expected workflow status.
