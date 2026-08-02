---
scenario_id: MCP-GITHUB-024
scenario_name: List Authenticated User GitHub Organizations
business_feature: Organization Management
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

`mcp-github-list-authenticated-user-orgs`

### Business Objective

Verify that an authorised caller can list organizations for the authenticated GitHub user through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with a GitHub token or session that has the required read permission.
- The target the authenticated GitHub user exists and is accessible.
- The `mcp-github-list-authenticated-user-orgs` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Repository or organization context | Read from environment-specific test configuration |
| Target identifier | A valid owner, repository, number, ID, branch, tag or path required by the tool |
| Expected marker | A known login, SHA, title, tag, path or identifier used for verification |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the valid identifiers required to list organizations. | The request is accepted without validation or permission errors. |
| 2 | Retrieve the tool response. | A non-error object or collection is returned. |
| 3 | Inspect the returned data. | The expected organization is included. |

### Overall Expected Result

The tool successfully performs the primary positive path to list organizations, and the expected organization is included.
