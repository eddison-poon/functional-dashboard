---
scenario_id: MCP-GITHUB-004
scenario_name: Create Git Reference
business_feature: Branch and Reference Management
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

`mcp-github-create-reference`

### Business Objective

Verify that an authorised caller can create a Git reference for an existing repository and source commit through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permissions required for the operation.
- The required parent an existing repository and source commit exists and is accessible.
- Unique disposable test data is available.
- The `mcp-github-create-reference` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Owner and repository context | Read from secure non-secret test configuration |
| Unique generated value | Generate a value containing `MCP-GITHUB-A-004` and the execution timestamp |
| Operation-specific fields | Supply valid branch, title, body, path, content or settings required by the tool |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid generated data to create a Git reference. | The request is accepted without validation or permission errors. |
| 2 | Confirm the creation or upsert operation. | The tool reports successful completion and returns an identifier or updated resource. |
| 3 | Retrieve the resulting GitHub resource. | The new reference resolves to the intended commit. |

### Overall Expected Result

The tool successfully performs the primary positive path to create a Git reference, and the new reference resolves to the intended commit.
