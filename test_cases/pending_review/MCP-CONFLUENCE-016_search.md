---
scenario_id: MCP-CONFLUENCE-016
scenario_name: Search Confluence Content
business_feature: Content Search
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

`mcp-confluence-search`

### Business Objective

Verify that an authorised caller can search Confluence and retrieve content matching a known unique query.

### Preconditions

- The caller is authenticated and authorised to search the target content.
- A searchable page with a unique marker exists.
- Search indexing has completed.
- The search tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Search query | A unique marker |
| Expected result | Known page ID or title |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the unique query. | The request is accepted. |
| 2 | Retrieve search results. | A result collection is returned. |
| 3 | Inspect the results. | The known page is included. |

### Overall Expected Result

Confluence search returns the expected accessible content for the submitted query.
