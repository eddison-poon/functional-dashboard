---
scenario_id: MCP-CONFLUENCE-006
scenario_name: Delete Existing Confluence Space
business_feature: Space Management
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

`mcp-confluence-delete-space`

### Business Objective

Verify that an authorised caller can delete a disposable Confluence space.

### Preconditions

- The caller is authenticated and authorised to delete spaces.
- A disposable test space exists and may safely be removed.
- The delete-space tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Space reference | A disposable space created specifically for the test |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable space reference. | The request is accepted. |
| 2 | Confirm space deletion. | The tool reports successful completion. |
| 3 | Attempt to retrieve the deleted space. | The space is not returned as active. |

### Overall Expected Result

The intended disposable space is deleted successfully and is no longer retrievable.
