---
scenario_id: MCP-GITHUB-018
scenario_name: Retrieve GitHub Organization Details
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

`mcp-github-get-org-details`

### Business Objective

Verify that an authorised caller can retrieve organization metadata for an accessible GitHub organization through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with a GitHub token or session that has the required read permission.
- The target an accessible GitHub organization exists and is accessible.
- The `mcp-github-get-org-details` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Repository or organization context | Read from environment-specific test configuration |
| Target identifier | A valid owner, repository, number, ID, branch, tag or path required by the tool |
| Expected marker | A known login, SHA, title, tag, path or identifier used for verification |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the valid identifiers required to retrieve organization metadata. | The request is accepted without validation or permission errors. |
| 2 | Retrieve the tool response. | A non-error object or collection is returned. |
| 3 | Inspect the returned data. | The returned login or name matches the target organization. |

### Overall Expected Result

The tool successfully performs the primary positive path to retrieve organization metadata, and the returned login or name matches the target organization.
