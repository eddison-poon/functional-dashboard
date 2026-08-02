---
scenario_id: MCP-JIRA-034
scenario_name: Move Jira Issues to Backlog
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

`mcp-jira-jira-move-issues-to-backlog`

### Business Objective

Verify that an authorised caller can move one or more eligible Jira issues from a sprint to the backlog.

### Preconditions

- The caller is authenticated and authorised to manage the target board and issues.
- One or more disposable issues are assigned to a sprint.
- The issues are eligible to be moved to backlog.
- The Jira MCP server and move-issues-to-backlog tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue references | One or more disposable issue keys assigned to a sprint |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the eligible issue references. | The request is accepted. |
| 2 | Confirm the move-to-backlog operation. | The tool reports successful completion. |
| 3 | Retrieve sprint or backlog state. | The issues are no longer assigned to the original sprint and appear in backlog state. |

### Overall Expected Result

All submitted eligible Jira issues are moved successfully from the sprint to the backlog.
