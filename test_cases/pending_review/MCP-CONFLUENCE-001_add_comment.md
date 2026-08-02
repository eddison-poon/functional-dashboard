---
scenario_id: MCP-CONFLUENCE-001
scenario_name: Add Comment to Confluence Page
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

`mcp-confluence-add-comment`

### Business Objective

Verify that an authorised caller can add a valid comment to an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to view and comment on the target page.
- The target page exists inside an approved test space.
- The add-comment tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A valid disposable or approved test page |
| Comment body | A unique non-empty value |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target page reference and valid comment body. | The request is accepted. |
| 2 | Confirm comment creation. | A comment identifier or success response is returned. |
| 3 | Retrieve the page comments. | The generated comment is present and matches the submitted body. |

### Overall Expected Result

A new comment is added successfully to the intended page and is retrievable.
