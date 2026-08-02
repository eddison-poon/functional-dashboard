---
scenario_id: MCP-GITHUB-010
scenario_name: Delete GitHub Repository
business_feature: Repository Management
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

`mcp-github-delete-repo`

### Business Objective

Verify that an authorised caller can delete a disposable repository for an authenticated user or organization through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub delete permission required for the target resource.
- A disposable an authenticated user or organization exists and may safely be removed.
- The target identifier is known.
- The `mcp-github-delete-repo` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Disposable target | Create during test setup and retain its identifier |
| Owner and repository context | Read from test configuration when required |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable target identifiers to delete a disposable repository. | The request is accepted. |
| 2 | Confirm the deletion operation. | The tool reports successful completion. |
| 3 | Attempt to retrieve the deleted resource. | The repository is no longer retrievable. |

### Overall Expected Result

The tool successfully performs the primary positive path to delete a disposable repository, and the repository is no longer retrievable.
