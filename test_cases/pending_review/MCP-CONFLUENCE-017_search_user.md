---
scenario_id: MCP-CONFLUENCE-017
scenario_name: Search Confluence User
business_feature: User Search
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

`mcp-confluence-search-user`

### Business Objective

Verify that an authorised caller can search for a known Confluence user.

### Preconditions

- The caller is authenticated and authorised to search users.
- A known active test user exists.
- The search-user tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| User query | A supported unique name or identifier |
| Expected user identity | Known account ID or safe identifier |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the user query. | The request is accepted. |
| 2 | Retrieve user results. | A collection of users is returned. |
| 3 | Inspect the results. | The expected user is included. |

### Overall Expected Result

The expected active Confluence user is returned successfully.
