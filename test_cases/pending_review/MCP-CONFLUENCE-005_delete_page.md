---
scenario_id: MCP-CONFLUENCE-005
scenario_name: Delete Existing Confluence Page
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

`mcp-confluence-delete-page`

### Business Objective

Verify that an authorised caller can delete a disposable Confluence page.

### Preconditions

- The caller is authenticated and authorised to delete the target page.
- A disposable page exists and may safely be removed.
- The delete-page tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A disposable page created specifically for the test |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable page reference. | The request is accepted. |
| 2 | Confirm page deletion. | The tool reports successful completion. |
| 3 | Attempt to retrieve the deleted page. | The page is not returned as an active page. |

### Overall Expected Result

The intended disposable page is deleted successfully and is no longer retrievable.
