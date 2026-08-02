---
scenario_id: MCP-GITHUB-001
scenario_name: Create GitHub Issue or Pull Request Comment
business_feature: Comment Management
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

`mcp-github-create-issue-or-pr-comment`

### Business Objective

Verify that an authorised caller can create a new comment for an existing issue or pull request through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permissions required for the operation.
- The required parent an existing issue or pull request exists and is accessible.
- Unique disposable test data is available.
- The `mcp-github-create-issue-or-pr-comment` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Owner and repository context | Read from secure non-secret test configuration |
| Unique generated value | Generate a value containing `MCP-GITHUB-A-001` and the execution timestamp |
| Operation-specific fields | Supply valid branch, title, body, path, content or settings required by the tool |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid generated data to create a new comment. | The request is accepted without validation or permission errors. |
| 2 | Confirm the creation or upsert operation. | The tool reports successful completion and returns an identifier or updated resource. |
| 3 | Retrieve the resulting GitHub resource. | The new comment is returned with the submitted body. |

### Overall Expected Result

The tool successfully performs the primary positive path to create a new comment, and the new comment is returned with the submitted body.
