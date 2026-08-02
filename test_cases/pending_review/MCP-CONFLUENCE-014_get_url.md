---
scenario_id: MCP-CONFLUENCE-014
scenario_name: Retrieve Confluence Resource URL
business_feature: Resource Navigation
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

`mcp-confluence-get-url`

### Business Objective

Verify that the tool returns a valid URL for a supported Confluence resource.

### Preconditions

- The caller is authenticated and authorised to view the target resource.
- The resource exists.
- The get-url tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Resource reference | A supported page or space reference |
| Expected host | The configured Confluence host |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the resource reference. | The request is accepted. |
| 2 | Retrieve the URL. | A non-empty URL is returned. |
| 3 | Validate the URL. | It uses an approved scheme and identifies the expected host and resource. |

### Overall Expected Result

A valid URL for the intended Confluence resource is returned.
