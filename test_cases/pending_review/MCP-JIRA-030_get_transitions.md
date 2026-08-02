---
scenario_id: MCP-JIRA-030
scenario_name: Retrieve Available Jira Issue Transitions
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

`mcp-jira-jira-get-transitions`

### Business Objective

Verify that an authorised caller can retrieve workflow transitions currently available for an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to browse and transition the target issue.
- The target issue exists in a known workflow state.
- At least one expected transition is available.
- The Jira MCP server and get-transitions tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue key or ID |
| Expected transition | A known transition name or ID available from the issue state |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference. | The request is accepted. |
| 2 | Retrieve available transitions. | A collection of currently available transitions is returned. |
| 3 | Inspect the transition data. | The expected transition is included. |

### Overall Expected Result

Available workflow transitions for the intended Jira issue are returned successfully and include the expected transition.
