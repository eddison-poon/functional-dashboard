---
scenario_id: MCP-CONFLUENCE-008
scenario_name: Retrieve Current Authenticated Confluence User
business_feature: User Context
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

`mcp-confluence-get-current-user`

### Business Objective

Verify that the tool returns the correct currently authenticated Confluence user.

### Preconditions

- A valid authenticated Confluence context is configured.
- The expected test-user identity is known.
- The get-current-user tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Expected user identity | Configured account ID, username or safe identifier |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Invoke get-current-user. | The request is accepted. |
| 2 | Retrieve the user response. | A user object is returned. |
| 3 | Compare the identity. | The returned identity matches the configured user. |

### Overall Expected Result

The tool returns the correct authenticated Confluence user.
