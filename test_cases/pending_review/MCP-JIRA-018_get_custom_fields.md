---
scenario_id: MCP-JIRA-018
scenario_name: Retrieve Jira Custom Fields
business_feature: Field Metadata
business_module: Jira
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

`mcp-jira-jira-get-custom-fields`

### Business Objective

Verify that an authorised caller can retrieve Jira custom field metadata through the MCP tool.

### Preconditions

- The caller is authenticated and authorised to access field metadata.
- At least one known custom field exists in the Jira instance.
- The Jira MCP server and get-custom-fields tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Expected custom field | A known field ID or name configured for verification |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Invoke the get-custom-fields tool. | The request is accepted. |
| 2 | Retrieve the custom-field collection. | A collection of available custom fields is returned. |
| 3 | Inspect the field metadata. | The known custom field is included with its expected identifier or name. |

### Overall Expected Result

Jira custom field metadata is returned successfully and includes the configured known field.
