---
scenario_id: MCP-GITHUB-035
scenario_name: List GitHub Repository Tags
business_feature: Tag Management
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

`mcp-github-list-repo-tags`

### Business Objective

Verify that an authorised caller can list tags for an existing repository with a known tag through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with a GitHub token or session that has the required read permission.
- The target an existing repository with a known tag exists and is accessible.
- The `mcp-github-list-repo-tags` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Repository or organization context | Read from environment-specific test configuration |
| Target identifier | A valid owner, repository, number, ID, branch, tag or path required by the tool |
| Expected marker | A known login, SHA, title, tag, path or identifier used for verification |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the valid identifiers required to list tags. | The request is accepted without validation or permission errors. |
| 2 | Retrieve the tool response. | A non-error object or collection is returned. |
| 3 | Inspect the returned data. | The expected tag is included. |

### Overall Expected Result

The tool successfully performs the primary positive path to list tags, and the expected tag is included.
