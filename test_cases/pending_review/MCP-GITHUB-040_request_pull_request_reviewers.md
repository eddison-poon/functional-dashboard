---
scenario_id: MCP-GITHUB-040
scenario_name: Request GitHub Pull Request Reviewers
business_feature: Pull Request Review Management
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

`mcp-github-request-pull-request-reviewers`

### Business Objective

Verify that an authorised caller can request reviewers for an open pull request and valid reviewer accounts through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permission required for the state-changing operation.
- A disposable or approved test an open pull request and valid reviewer accounts exists.
- The current state and intended updated state are known.
- The `mcp-github-request-pull-request-reviewers` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target identifier | Read from setup output or test configuration |
| Updated value | Generate a valid value containing `MCP-GITHUB-A-040` and the execution timestamp |
| Original value | Capture before the operation for comparison or restoration |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid identifiers and updated values to request reviewers. | The request is accepted. |
| 2 | Confirm the state-changing operation. | The tool reports successful completion. |
| 3 | Retrieve the updated GitHub resource. | The requested reviewers are associated with the pull request. |

### Overall Expected Result

The tool successfully performs the primary positive path to request reviewers, and the requested reviewers are associated with the pull request.
