---
scenario_id: MCP-JIRA-033
scenario_name: Retrieve Jira Issue Worklogs
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

`mcp-jira-jira-get-worklog`

### Business Objective

Verify that an authorised caller can retrieve worklogs from an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to view worklogs.
- The target issue exists and contains a known worklog.
- The Jira MCP server and get-worklog tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue key or ID |
| Expected worklog marker | A known worklog ID or description |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference. | The request is accepted. |
| 2 | Retrieve worklog data. | A collection of issue worklogs is returned. |
| 3 | Inspect the worklogs. | The expected worklog is included with the correct duration or description. |

### Overall Expected Result

Worklogs for the intended Jira issue are returned successfully and include the known worklog.
