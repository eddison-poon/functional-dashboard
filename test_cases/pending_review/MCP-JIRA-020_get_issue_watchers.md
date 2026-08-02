---
scenario_id: MCP-JIRA-020
scenario_name: Retrieve Jira Issue Watchers
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

`mcp-jira-jira-get-issue-watchers`

### Business Objective

Verify that an authorised caller can retrieve the watchers associated with an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to browse the target issue.
- The target issue exists and has at least one known watcher.
- The Jira MCP server and get-issue-watchers tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid Jira issue key or ID |
| Expected watcher | A known watcher account identifier |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference to the get-issue-watchers tool. | The request is accepted. |
| 2 | Retrieve the watcher collection. | A collection of issue watchers is returned. |
| 3 | Inspect the returned watchers. | The expected watcher is included. |

### Overall Expected Result

The watcher list for the intended Jira issue is returned successfully and includes the expected user.
