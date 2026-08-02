---
scenario_id: MCP-JIRA-016
scenario_name: Retrieve Comments from Jira Issue
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

`mcp-jira-jira-get-comments`

### Business Objective

Verify that an authorised caller can retrieve comments from an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to browse the target issue.
- The issue exists and contains at least one known comment.
- The Jira MCP server and get-comments tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue with a known comment |
| Expected comment marker | A unique marker created during setup |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference to the get-comments tool. | The request is accepted. |
| 2 | Retrieve the comment collection. | A collection of comments is returned. |
| 3 | Inspect the comments. | The known comment marker is included. |

### Overall Expected Result

The comments for the intended Jira issue are returned successfully and include the known comment.
