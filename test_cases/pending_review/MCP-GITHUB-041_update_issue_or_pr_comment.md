---
scenario_id: MCP-GITHUB-041
scenario_name: Update GitHub Issue or Pull Request Comment
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

`mcp-github-update-issue-or-pr-comment`

### Business Objective

Verify that an authorised caller can update a disposable comment for an existing issue or pull request through the GitHub MCP tool.

### Preconditions

- The caller is authenticated with the GitHub permission required for the state-changing operation.
- A disposable or approved test an existing issue or pull request exists.
- The current state and intended updated state are known.
- The `mcp-github-update-issue-or-pr-comment` tool is available in the GitHub MCP server.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target identifier | Read from setup output or test configuration |
| Updated value | Generate a valid value containing `MCP-GITHUB-A-041` and the execution timestamp |
| Original value | Capture before the operation for comparison or restoration |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid identifiers and updated values to update a disposable comment. | The request is accepted. |
| 2 | Confirm the state-changing operation. | The tool reports successful completion. |
| 3 | Retrieve the updated GitHub resource. | The comment body contains the submitted updated value. |

### Overall Expected Result

The tool successfully performs the primary positive path to update a disposable comment, and the comment body contains the submitted updated value.
