---
scenario_id: MCP-JIRA-036
scenario_name: Remove Watcher from Jira Issue
business_feature: Issue Watchers
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

`mcp-jira-jira-remove-issue-watcher`

### Business Objective

Verify that an authorised caller can remove an existing watcher from a Jira issue.

### Preconditions

- The caller is authenticated and authorised to manage issue watchers.
- The target issue exists.
- The target user is currently watching the issue.
- The Jira MCP server and remove-issue-watcher tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue key or ID |
| Watcher reference | A valid watcher account identifier |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue and watcher references. | The request is accepted. |
| 2 | Confirm watcher removal. | The tool reports successful completion. |
| 3 | Retrieve or inspect issue watchers. | The removed watcher is no longer associated with the issue. |

### Overall Expected Result

The intended watcher is removed successfully from the target Jira issue.
