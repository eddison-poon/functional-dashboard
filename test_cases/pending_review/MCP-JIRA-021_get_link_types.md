---
scenario_id: MCP-JIRA-021
scenario_name: Retrieve Jira Issue Link Types
business_feature: Issue Linking
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

`mcp-jira-jira-get-link-types`

### Business Objective

Verify that an authorised caller can retrieve the configured Jira issue link types.

### Preconditions

- The caller is authenticated.
- At least one known issue link type is configured.
- The Jira MCP server and get-link-types tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Expected link type | A known configured issue link type such as Blocks or Relates |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Invoke the get-link-types tool. | The request is accepted. |
| 2 | Retrieve the link-type collection. | A collection of configured issue link types is returned. |
| 3 | Inspect the returned values. | The expected link type is present with supported inward and outward descriptions. |

### Overall Expected Result

Configured Jira issue link types are returned successfully and include the expected type.
