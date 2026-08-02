---
scenario_id: MCP-JIRA-040
scenario_name: Update Existing Jira Issue Fields
business_feature: Issue Management
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

`mcp-jira-jira-update-issue`

### Business Objective

Verify that an authorised caller can update supported fields on an existing Jira issue using valid values.

### Preconditions

- The caller is authenticated and authorised to edit the target issue.
- A disposable existing Jira issue is available.
- The fields selected for update are editable in the issue's current context.
- Valid field values and any required field identifiers are known.
- The Jira MCP server and update-issue tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid disposable Jira issue key or ID |
| Updated summary or description | A unique valid value |
| Additional fields | Valid editable field values supported by the tool |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference and valid updated field values. | The request is accepted without validation or permission errors. |
| 2 | Confirm the update request. | The tool reports successful completion and returns updated issue information when supported. |
| 3 | Retrieve the updated issue. | The changed fields contain the submitted values. |
| 4 | Inspect fields not included in the update. | Unchanged fields retain their previous values. |

### Overall Expected Result

The intended Jira issue is updated successfully with the submitted field values while unrelated fields remain unchanged.
