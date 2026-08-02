---
scenario_id: MCP-JIRA-019
scenario_name: Retrieve Existing Jira Issue
business_feature: Issue Retrieval
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

`mcp-jira-jira-get-issue`

### Business Objective

Verify that an authorised caller can retrieve an existing Jira issue by a supported issue reference.

### Preconditions

- The caller is authenticated and authorised to browse the target issue.
- The target issue exists with known values.
- The Jira MCP server and get-issue tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid Jira issue key or ID |
| Expected summary | Known issue summary |
| Expected issue type | Known issue type |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the valid issue reference to the get-issue tool. | The request is accepted. |
| 2 | Retrieve the issue response. | The requested issue and supported fields are returned. |
| 3 | Inspect the returned issue. | The key or ID, summary and issue type match the intended issue. |

### Overall Expected Result

The intended Jira issue is retrieved successfully with the expected identity and field values.
