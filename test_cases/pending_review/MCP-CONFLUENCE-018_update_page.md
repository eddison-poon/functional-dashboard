---
scenario_id: MCP-CONFLUENCE-018
scenario_name: Update Existing Confluence Page
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

`mcp-confluence-update-page`

### Business Objective

Verify that an authorised caller can update supported fields of an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to edit the page.
- A disposable page exists.
- Current version information is available when required.
- The update-page tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A disposable page |
| Updated title or body | A unique valid value |
| Version information | Current value when required |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the page reference and updated content. | The request is accepted. |
| 2 | Confirm the update operation. | The tool reports successful completion. |
| 3 | Retrieve the page. | The changed values are returned. |

### Overall Expected Result

The intended page is updated successfully with the submitted values.
