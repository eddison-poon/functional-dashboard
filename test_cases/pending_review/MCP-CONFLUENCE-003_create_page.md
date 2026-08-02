---
scenario_id: MCP-CONFLUENCE-003
scenario_name: Create Confluence Page with Valid Content
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

`mcp-confluence-create-page`

### Business Objective

Verify that an authorised caller can create a Confluence page using valid mandatory information.

### Preconditions

- The caller is authenticated and has permission to create pages in the target space.
- The target space exists and is approved for automation.
- The create-page tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Space reference | A valid test space |
| Page title | A unique valid title |
| Page body | Valid non-empty content |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the space reference, unique title and valid body. | The request is accepted. |
| 2 | Confirm page creation. | A page identifier or URL is returned. |
| 3 | Retrieve the created page. | The title and body match the submitted values. |

### Overall Expected Result

A new Confluence page is created successfully in the intended space.
