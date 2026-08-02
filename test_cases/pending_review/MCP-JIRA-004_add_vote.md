---
scenario_id: MCP-JIRA-004
scenario_name: Add Vote to Jira Issue
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

`mcp-jira-jira-add-vote`

### Business Objective

Verify that the authenticated user can add a vote to an existing Jira issue through the MCP tool.

### Preconditions

- The caller is authenticated and allowed to vote on issues.
- The target issue exists and voting is enabled.
- The authenticated user has not already voted on the issue.
- The Jira MCP server and add-vote tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid existing Jira issue key or ID |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target issue reference to the add-vote tool. | The request is accepted. |
| 2 | Confirm the vote request. | The tool reports successful completion. |
| 3 | Inspect the issue voting state. | The issue vote count or voter state reflects the authenticated user's vote. |

### Overall Expected Result

The authenticated user successfully votes on the intended Jira issue.
