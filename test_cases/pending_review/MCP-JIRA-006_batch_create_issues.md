---
scenario_id: MCP-JIRA-006
scenario_name: Batch Create Jira Issues
business_feature: Issue Creation
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

`mcp-jira-jira-batch-create-issues`

### Business Objective

Verify that an authorised caller can create multiple Jira issues in one batch using valid issue definitions.

### Preconditions

- The caller is authenticated and authorised to create issues in the target project.
- The target project and selected issue types exist.
- All mandatory fields for each issue are known.
- The Jira MCP server and batch-create-issues tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Project reference | A valid project key or ID |
| Issue definitions | Two or more valid issue payloads with unique summaries |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit multiple valid issue definitions in one batch request. | The batch request is accepted. |
| 2 | Confirm batch creation. | The tool returns a successful result for each submitted issue. |
| 3 | Retrieve the created issues. | Each created issue exists with a unique key and the submitted values. |

### Overall Expected Result

All valid issues in the batch are created successfully and returned with unique Jira identifiers.
