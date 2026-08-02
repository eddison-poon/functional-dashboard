---
scenario_id: MCP-CONFLUENCE-011
scenario_name: Retrieve Child Pages of Confluence Page
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

`mcp-confluence-get-page-children`

### Business Objective

Verify that an authorised caller can retrieve direct child pages of an existing Confluence parent page.

### Preconditions

- The caller is authenticated and authorised to view the parent and child pages.
- A parent page exists with a known direct child.
- The get-page-children tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Parent page reference | A valid page with a known child |
| Expected child | Known child page ID or title |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the parent page reference. | The request is accepted. |
| 2 | Retrieve direct children. | A collection of child pages is returned. |
| 3 | Inspect the collection. | The expected child is included. |

### Overall Expected Result

Direct child pages of the intended parent are returned successfully.
