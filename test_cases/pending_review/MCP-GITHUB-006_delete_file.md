---
scenario_id: MCP-GITHUB-006
scenario_name: Delete File from GitHub Repository
business_feature: Repository Content Management
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

`mcp-github-delete-file`

### Business Objective

Verify that an authorised caller can delete a file for an existing file in a disposable repository branch through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub delete permission required for the target resource.
- A disposable an existing file in a disposable repository branch exists and may safely be removed.
- The target identifier is known.
- The `mcp-github-delete-file` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Disposable target | Create during test setup and retain its identifier |
| Owner and repository context | Read from test configuration when required |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable target identifiers to delete a file. | The request is accepted. |
| 2 | Confirm the deletion operation. | The tool reports successful completion. |
| 3 | Attempt to retrieve the deleted resource. | The file is no longer returned at the target path. |

### Overall Expected Result

The tool successfully performs the primary positive path to delete a file, and the file is no longer returned at the target path.
