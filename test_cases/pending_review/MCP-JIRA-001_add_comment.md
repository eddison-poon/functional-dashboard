---
scenario_id: MCP-JIRA-001
scenario_name: Add Comment to Jira Issue
business_feature: Comment Management
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

`mcp-jira-jira-add-comment`

### Business Objective

Verify that an authorised caller can add a valid comment to an existing Jira issue through the MCP tool.

### Preconditions

- The caller is authenticated and authorised to browse and comment on the target issue.
- The target Jira issue exists and is available.
- The Jira MCP server and add-comment tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid existing Jira issue key or ID |
| Comment body | A unique non-empty comment generated for the test |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target issue reference and valid comment body. | The request is accepted without validation or permission errors. |
| 2 | Confirm the comment creation request. | A new comment is created and a comment identifier or success response is returned. |
| 3 | Retrieve the issue comments. | The generated comment is present and matches the submitted value. |

### Overall Expected Result

A new comment is added successfully to the intended Jira issue and can be retrieved with the submitted content.
