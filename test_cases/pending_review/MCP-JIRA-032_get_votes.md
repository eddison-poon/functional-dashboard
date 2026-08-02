---
scenario_id: MCP-JIRA-032
scenario_name: Retrieve Votes from Jira Issue
business_feature: Issue Voting
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

`mcp-jira-jira-get-votes`

### Business Objective

Verify that an authorised caller can retrieve vote information for an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to browse the target issue.
- The target issue exists and voting is enabled.
- The issue has a known vote state.
- The Jira MCP server and get-votes tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue key or ID |
| Expected vote state | Known vote count or watcher identity where returned |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference. | The request is accepted. |
| 2 | Retrieve vote information. | Vote count and supported voter information are returned. |
| 3 | Inspect the returned state. | The returned vote data matches the configured known state. |

### Overall Expected Result

Vote information for the intended Jira issue is returned successfully and matches the known state.
