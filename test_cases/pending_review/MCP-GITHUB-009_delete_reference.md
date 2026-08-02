---
scenario_id: MCP-GITHUB-009
scenario_name: Delete Git Reference
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

`mcp-github-delete-reference`

### Business Objective

Verify that an authorised caller can delete a disposable Git reference for an existing repository through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub delete permission required for the target resource.
- A disposable an existing repository exists and may safely be removed.
- The target identifier is known.
- The `mcp-github-delete-reference` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Disposable target | Create during test setup and retain its identifier |
| Owner and repository context | Read from test configuration when required |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable target identifiers to delete a disposable Git reference. | The request is accepted. |
| 2 | Confirm the deletion operation. | The tool reports successful completion. |
| 3 | Attempt to retrieve the deleted resource. | The reference is no longer returned. |

### Overall Expected Result

The tool successfully performs the primary positive path to delete a disposable Git reference, and the reference is no longer returned.
