---
scenario_id: MCP-GITHUB-003
scenario_name: Create GitHub Pull Request
business_feature: Pull Request Management
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

`mcp-github-create-pull-request`

### Business Objective

Verify that an authorised caller can create a pull request for a repository with distinct source and target branches through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permissions required for the operation.
- The required parent a repository with distinct source and target branches exists and is accessible.
- Unique disposable test data is available.
- The `mcp-github-create-pull-request` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Owner and repository context | Read from secure non-secret test configuration |
| Unique generated value | Generate a value containing `MCP-GITHUB-A-003` and the execution timestamp |
| Operation-specific fields | Supply valid branch, title, body, path, content or settings required by the tool |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid generated data to create a pull request. | The request is accepted without validation or permission errors. |
| 2 | Confirm the creation or upsert operation. | The tool reports successful completion and returns an identifier or updated resource. |
| 3 | Retrieve the resulting GitHub resource. | The pull request is returned with the expected title, branches and open state. |

### Overall Expected Result

The tool successfully performs the primary positive path to create a pull request, and the pull request is returned with the expected title, branches and open state.
