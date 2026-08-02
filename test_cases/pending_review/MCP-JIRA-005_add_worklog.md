---
scenario_id: MCP-JIRA-005
scenario_name: Add Worklog to Jira Issue
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

`mcp-jira-jira-add-worklog`

### Business Objective

Verify that an authorised caller can add a valid worklog entry to an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to log work.
- The target issue exists and time tracking is enabled where required.
- The Jira MCP server and add-worklog tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid Jira issue key or ID |
| Time spent | A valid duration such as `30m` |
| Work description | A unique non-empty description |
| Started time | A valid timestamp when required |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference and valid worklog details. | The request is accepted. |
| 2 | Confirm worklog creation. | A worklog is created and a worklog identifier or success response is returned. |
| 3 | Retrieve or inspect issue worklogs. | The new worklog appears with the submitted duration and description. |

### Overall Expected Result

A valid worklog is added successfully to the intended Jira issue.
