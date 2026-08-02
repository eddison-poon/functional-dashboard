---
scenario_id: MCP-CONFLUENCE-015
scenario_name: Move Confluence Page to New Parent
business_feature: Page Hierarchy
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

`mcp-confluence-move-page`

### Business Objective

Verify that an authorised caller can move an existing Confluence page beneath a different valid parent.

### Preconditions

- The caller is authenticated and authorised to move the target page.
- A disposable source page and valid destination parent exist.
- The move will not create an invalid hierarchy.
- The move-page tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Source page | A disposable page |
| Destination parent | A valid parent page |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the source and destination references. | The request is accepted. |
| 2 | Confirm the move operation. | The tool reports successful completion. |
| 3 | Retrieve destination children. | The moved page is present under the new parent. |

### Overall Expected Result

The target page is moved successfully to the intended parent.
