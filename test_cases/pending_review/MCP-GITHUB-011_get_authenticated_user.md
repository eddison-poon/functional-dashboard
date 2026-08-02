---
scenario_id: MCP-GITHUB-011
scenario_name: Retrieve Authenticated GitHub User
business_feature: User Context
business_module: GitHub
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

`mcp-github-get-authenticated-user`

### Business Objective

Verify that an authorised caller can retrieve user information for the current authenticated GitHub session through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with a GitHub token or session that has the required read permission.
- The target the current authenticated GitHub session exists and is accessible.
- The `mcp-github-get-authenticated-user` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Repository or organization context | Read from environment-specific test configuration |
| Target identifier | A valid owner, repository, number, ID, branch, tag or path required by the tool |
| Expected marker | A known login, SHA, title, tag, path or identifier used for verification |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the valid identifiers required to retrieve user information. | The request is accepted without validation or permission errors. |
| 2 | Retrieve the tool response. | A non-error object or collection is returned. |
| 3 | Inspect the returned data. | The returned login or account identifier matches configured expectations. |

### Overall Expected Result

The tool successfully performs the primary positive path to retrieve user information, and the returned login or account identifier matches configured expectations.
