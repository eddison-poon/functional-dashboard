---
scenario_id: MCP-GITHUB-002
scenario_name: Create GitHub Organization Repository
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

`mcp-github-create-org-repo`

### Business Objective

Verify that an authorised caller can create a repository for a target GitHub organization through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permissions required for the operation.
- The required parent a target GitHub organization exists and is accessible.
- Unique disposable test data is available.
- The `mcp-github-create-org-repo` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Owner and repository context | Read from secure non-secret test configuration |
| Unique generated value | Generate a value containing `MCP-GITHUB-A-002` and the execution timestamp |
| Operation-specific fields | Supply valid branch, title, body, path, content or settings required by the tool |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid generated data to create a repository. | The request is accepted without validation or permission errors. |
| 2 | Confirm the creation or upsert operation. | The tool reports successful completion and returns an identifier or updated resource. |
| 3 | Retrieve the resulting GitHub resource. | The repository exists under the organization with the submitted settings. |

### Overall Expected Result

The tool successfully performs the primary positive path to create a repository, and the repository exists under the organization with the submitted settings.
