---
scenario_id: MCP-CONFLUENCE-012
scenario_name: Retrieve Existing Confluence Space
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

`mcp-confluence-get-space`

### Business Objective

Verify that an authorised caller can retrieve an existing Confluence space.

### Preconditions

- The caller is authenticated and authorised to view the target space.
- The space exists with known metadata.
- The get-space tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Space reference | A valid key or ID |
| Expected space name | Known space name |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the space reference. | The request is accepted. |
| 2 | Retrieve the space. | The requested space is returned. |
| 3 | Inspect metadata. | The key or ID and expected name match. |

### Overall Expected Result

The intended space is retrieved successfully with the expected metadata.
