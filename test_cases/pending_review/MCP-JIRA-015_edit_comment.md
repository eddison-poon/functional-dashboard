---
scenario_id: MCP-JIRA-015
scenario_name: Edit Jira Issue Comment
business_feature: Comment Management
business_module: Jira
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

`mcp-jira-jira-edit-comment`

### Business Objective

Verify that an authorised caller can edit an existing Jira issue comment with valid updated content.

### Preconditions

- The caller is authenticated and authorised to edit the target comment.
- A disposable comment exists and its identifier is known.
- The Jira MCP server and edit-comment tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid issue containing the comment |
| Comment reference | A disposable comment ID |
| Updated body | A unique valid updated comment value |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue, comment and updated body. | The request is accepted. |
| 2 | Confirm the comment update. | The tool reports successful completion and returns updated comment information. |
| 3 | Retrieve the issue comments. | The target comment contains the updated body. |

### Overall Expected Result

The intended Jira comment is updated successfully with the submitted content.
