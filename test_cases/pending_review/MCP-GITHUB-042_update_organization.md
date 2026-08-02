---
scenario_id: MCP-GITHUB-042
scenario_name: Update GitHub Organization
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

`mcp-github-update-organization`

### Business Objective

Verify that an authorised caller can update supported organization details for a disposable or approved test organization through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permission required for the state-changing operation.
- A disposable or approved test a disposable or approved test organization exists.
- The current state and intended updated state are known.
- The `mcp-github-update-organization` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target identifier | Read from setup output or test configuration |
| Updated value | Generate a valid value containing `MCP-GITHUB-A-042` and the execution timestamp |
| Original value | Capture before the operation for comparison or restoration |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid identifiers and updated values to update supported organization details. | The request is accepted. |
| 2 | Confirm the state-changing operation. | The tool reports successful completion. |
| 3 | Retrieve the updated GitHub resource. | The changed organization fields match the submitted values. |

### Overall Expected Result

The tool successfully performs the primary positive path to update supported organization details, and the changed organization fields match the submitted values.
