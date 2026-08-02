---
scenario_id: MCP-JIRA-031
scenario_name: Retrieve Jira Resource URL
business_feature: Resource Navigation
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

`mcp-jira-jira-get-url`

### Business Objective

Verify that the MCP tool returns a valid Jira URL for a supported resource reference.

### Preconditions

- The caller is authenticated and authorised to view the target Jira resource.
- The target Jira issue or supported resource exists.
- The Jira MCP server and get-url tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Resource reference | A supported Jira issue or resource identifier |
| Expected host | The configured Jira base host |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the resource reference. | The request is accepted. |
| 2 | Retrieve the URL. | A non-empty URL is returned. |
| 3 | Validate the URL. | The URL uses an approved scheme, contains the expected host and identifies the intended resource. |

### Overall Expected Result

A valid URL for the intended Jira resource is returned and resolves to the configured Jira host and target.
