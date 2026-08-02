---
scenario_id: MCP-CONFLUENCE-009
scenario_name: Retrieve Labels from Confluence Page
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

`mcp-confluence-get-labels`

### Business Objective

Verify that an authorised caller can retrieve labels assigned to an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to view the page.
- The target page contains a known label.
- The get-labels tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A valid page with a known label |
| Expected label | A known unique label |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the page reference. | The request is accepted. |
| 2 | Retrieve the label collection. | A collection of labels is returned. |
| 3 | Inspect the labels. | The expected label is included. |

### Overall Expected Result

Labels for the intended page are returned successfully and include the expected label.
