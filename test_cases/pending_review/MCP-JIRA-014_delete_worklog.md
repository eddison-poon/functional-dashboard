---
scenario_id: MCP-JIRA-014
scenario_name: Delete Jira Issue Worklog
business_feature: Worklog Management
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

`mcp-jira-jira-delete-worklog`

### Business Objective

Verify that an authorised caller can delete a disposable worklog from an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to delete the target worklog.
- A disposable worklog exists and its identifier is known.
- The Jira MCP server and delete-worklog tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue containing the worklog |
| Worklog reference | A disposable worklog ID created during setup |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue and worklog references. | The request is accepted. |
| 2 | Confirm worklog deletion. | The tool reports successful completion. |
| 3 | Inspect the issue worklogs. | The deleted worklog is no longer returned. |

### Overall Expected Result

The intended Jira worklog is deleted successfully and is no longer retrievable.
