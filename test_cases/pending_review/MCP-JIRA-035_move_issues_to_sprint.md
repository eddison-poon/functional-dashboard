---
scenario_id: MCP-JIRA-035
scenario_name: Move Jira Issues to Sprint
business_feature: Sprint Management
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

`mcp-jira-jira-move-issues-to-sprint`

### Business Objective

Verify that an authorised caller can move one or more eligible Jira issues into a target sprint.

### Preconditions

- The caller is authenticated and authorised to manage the board and issues.
- A valid target sprint exists.
- One or more disposable issues exist in backlog or another eligible state.
- The Jira MCP server and move-issues-to-sprint tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sprint ID | A valid target sprint identifier |
| Issue references | One or more eligible disposable issue keys |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target sprint and issue references. | The request is accepted. |
| 2 | Confirm the move-to-sprint operation. | The tool reports successful completion. |
| 3 | Retrieve target sprint issues. | All submitted issues are included in the target sprint. |

### Overall Expected Result

All submitted eligible Jira issues are moved successfully into the intended sprint.
