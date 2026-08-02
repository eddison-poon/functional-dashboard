---
scenario_id: MCP-JIRA-017
scenario_name: Retrieve Current Authenticated Jira User
business_feature: User Context
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

`mcp-jira-jira-get-current-authenticated-user`

### Business Objective

Verify that the MCP tool returns the correct currently authenticated Jira user.

### Preconditions

- A valid authenticated Jira credential or session context is configured.
- The expected test-user identifier is known.
- The Jira MCP server and get-current-authenticated-user tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Expected user identity | Configured account ID, username or safe identifier |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Invoke the get-current-authenticated-user tool. | The request is accepted. |
| 2 | Retrieve the user response. | A Jira user object is returned. |
| 3 | Compare returned identity. | The account identity matches the configured authenticated test user. |

### Overall Expected Result

The tool returns the correct currently authenticated Jira user and available profile information.
