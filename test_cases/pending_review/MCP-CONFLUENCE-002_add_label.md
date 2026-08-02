---
scenario_id: MCP-CONFLUENCE-002
scenario_name: Add Label to Confluence Page
business_feature: Label Management
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

`mcp-confluence-add-label`

### Business Objective

Verify that an authorised caller can add a valid label to an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to edit page metadata.
- The target page exists and does not already contain the generated label.
- The add-label tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A valid test page |
| Label | A unique valid Confluence label |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the page reference and valid label. | The request is accepted. |
| 2 | Confirm label addition. | The tool reports successful completion. |
| 3 | Retrieve page labels. | The submitted label is included. |

### Overall Expected Result

The requested label is associated successfully with the intended page.
