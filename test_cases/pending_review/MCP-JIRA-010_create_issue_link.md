---
scenario_id: MCP-JIRA-010
scenario_name: Create Link Between Jira Issues
business_feature: Issue Linking
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

`mcp-jira-jira-create-issue-link`

### Business Objective

Verify that an authorised caller can create a supported link between two existing Jira issues.

### Preconditions

- The caller is authenticated and authorised to link both issues.
- Two distinct existing issues are available.
- The selected issue-link type exists.
- The Jira MCP server and create-issue-link tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Source issue | A valid Jira issue key or ID |
| Target issue | A different valid Jira issue key or ID |
| Link type | A supported issue link type |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit source issue, target issue and valid link type. | The request is accepted. |
| 2 | Confirm issue-link creation. | The tool reports successful completion. |
| 3 | Retrieve or inspect the issue links. | The selected relationship is visible between the intended issues. |

### Overall Expected Result

A valid Jira issue link is created successfully between the two intended issues.
