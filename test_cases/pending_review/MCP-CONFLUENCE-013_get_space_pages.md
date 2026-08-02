---
scenario_id: MCP-CONFLUENCE-013
scenario_name: Retrieve Pages from Confluence Space
business_feature: Space Content
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

`mcp-confluence-get-space-pages`

### Business Objective

Verify that an authorised caller can retrieve pages contained in an existing Confluence space.

### Preconditions

- The caller is authenticated and authorised to view the target space.
- The space contains at least one known page.
- The get-space-pages tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Space reference | A valid key or ID |
| Expected page | Known page ID or title |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the space reference. | The request is accepted. |
| 2 | Retrieve the page collection. | A collection of pages is returned. |
| 3 | Inspect the collection. | The expected page is included. |

### Overall Expected Result

Pages from the intended space are returned successfully and include the expected page.
