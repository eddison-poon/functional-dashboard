---
scenario_id: MCP-CONFLUENCE-010
scenario_name: Retrieve Existing Confluence Page
business_feature: Page Management
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

`mcp-confluence-get-page`

### Business Objective

Verify that an authorised caller can retrieve an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to view the page.
- The page exists with known title and content.
- The get-page tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A valid page ID, URL or supported identifier |
| Expected title | Known title |
| Expected content marker | Known body text |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the page reference. | The request is accepted. |
| 2 | Retrieve the page. | The requested page is returned. |
| 3 | Inspect page details. | The identifier, title and content marker match. |

### Overall Expected Result

The intended page is retrieved successfully with the expected content.
