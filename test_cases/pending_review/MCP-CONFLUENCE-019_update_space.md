---
scenario_id: MCP-CONFLUENCE-019
scenario_name: Update Existing Confluence Space
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

`mcp-confluence-update-space`

### Business Objective

Verify that an authorised caller can update supported details of an existing Confluence space.

### Preconditions

- The caller is authenticated and authorised to administer the space.
- A disposable or approved test space exists.
- The update-space tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Space reference | A disposable or approved test space |
| Updated name or description | A unique valid value |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the space reference and updated details. | The request is accepted. |
| 2 | Confirm the update operation. | The tool reports successful completion. |
| 3 | Retrieve the space. | The changed details are returned. |

### Overall Expected Result

The intended space is updated successfully with the submitted details.
