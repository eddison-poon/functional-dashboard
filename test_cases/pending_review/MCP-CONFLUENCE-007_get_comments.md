---
scenario_id: MCP-CONFLUENCE-007
scenario_name: Retrieve Comments from Confluence Page
business_feature: Comment Management
business_module: Confluence
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

`mcp-confluence-get-comments`

### Business Objective

Verify that an authorised caller can retrieve comments from an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to view the page.
- The page exists and contains a known comment.
- The get-comments tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A valid page containing a known comment |
| Expected comment marker | A unique known value |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the page reference. | The request is accepted. |
| 2 | Retrieve the comment collection. | A collection of comments is returned. |
| 3 | Inspect the comments. | The expected marker is present. |

### Overall Expected Result

Comments for the intended page are returned successfully and include the known comment.
