---
scenario_id: MCP-JIRA-041
scenario_name: Update Existing Jira Worklog
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

`mcp-jira-jira-update-worklog`

### Business Objective

Verify that an authorised caller can update an existing Jira worklog using valid revised values.

### Preconditions

- The caller is authenticated and authorised to edit the target worklog.
- A disposable Jira issue exists.
- A disposable worklog exists on the issue and its identifier is known.
- The updated duration, description and timestamp values are valid.
- The Jira MCP server and update-worklog tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid Jira issue key or ID |
| Worklog reference | A valid disposable worklog ID |
| Updated time spent | A valid duration such as `45m` |
| Updated description | A unique valid worklog description |
| Updated started time | A valid timestamp when supported |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference, worklog reference and valid updated worklog values. | The request is accepted without validation or permission errors. |
| 2 | Confirm the worklog update. | The tool reports successful completion and returns updated worklog information when supported. |
| 3 | Retrieve the issue worklogs. | The target worklog contains the updated duration and description. |
| 4 | Verify worklog identity. | The original worklog identifier is retained unless the tool contract explicitly states otherwise. |

### Overall Expected Result

The intended Jira worklog is updated successfully with the submitted values.
