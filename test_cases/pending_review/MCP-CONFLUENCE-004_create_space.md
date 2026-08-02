---
scenario_id: MCP-CONFLUENCE-004
scenario_name: Create Confluence Space with Valid Details
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

`mcp-confluence-create-space`

### Business Objective

Verify that an authorised caller can create a Confluence space using valid mandatory details.

### Preconditions

- The caller is authenticated and authorised to create spaces.
- The generated space key and name are unique.
- The create-space tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Space key | A unique valid key |
| Space name | A unique valid name |
| Description | Valid optional description |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit a unique space key, name and supported description. | The request is accepted. |
| 2 | Confirm space creation. | A space identifier or URL is returned. |
| 3 | Retrieve the created space. | The returned key, name and description match. |

### Overall Expected Result

A new Confluence space is created successfully with the submitted details.
