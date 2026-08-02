---
scenario_id: MCP-JIRA-002
scenario_name: Add Watcher to Jira Issue
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

`mcp-jira-jira-add-issue-watcher`

### Business Objective

Verify that an authorised caller can add a valid user as a watcher of an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to manage issue watchers.
- The target issue exists.
- The target user exists and is not already watching the issue.
- The Jira MCP server and add-issue-watcher tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid Jira issue key or ID |
| User reference | A valid account identifier for a test user |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target issue and user reference. | The request is accepted. |
| 2 | Confirm the watcher addition. | The tool reports successful completion. |
| 3 | Inspect the issue watcher state through an approved verification method. | The target user is associated as a watcher of the issue. |

### Overall Expected Result

The intended user is added successfully as a watcher of the target Jira issue.
