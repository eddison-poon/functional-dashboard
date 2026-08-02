---
scenario_id: MCP-JIRA-013
scenario_name: Delete Existing Jira Issue
business_feature: Issue Management
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

`mcp-jira-jira-delete-issue`

### Business Objective

Verify that an authorised caller can delete a disposable Jira issue.

### Preconditions

- The caller is authenticated and authorised to delete issues.
- A disposable issue exists and may safely be removed.
- The Jira MCP server and delete-issue tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A disposable Jira issue key or ID |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable issue reference to the delete-issue tool. | The request is accepted. |
| 2 | Confirm issue deletion. | The tool reports successful completion. |
| 3 | Attempt to retrieve the deleted issue. | The issue is not returned as an active accessible issue. |

### Overall Expected Result

The intended disposable Jira issue is deleted successfully and is no longer retrievable.
