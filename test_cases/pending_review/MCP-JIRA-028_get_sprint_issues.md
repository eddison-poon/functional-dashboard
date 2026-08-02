---
scenario_id: MCP-JIRA-028
scenario_name: Retrieve Issues from Jira Sprint
business_feature: Sprint Management
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

`mcp-jira-jira-get-sprint-issues`

### Business Objective

Verify that an authorised caller can retrieve issues assigned to a known Jira sprint.

### Preconditions

- The caller is authenticated and authorised to browse the project and board.
- A known sprint exists and contains at least one known issue.
- The Jira MCP server and get-sprint-issues tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sprint ID | A valid sprint identifier |
| Expected issue | A known issue key assigned to the sprint |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the sprint ID. | The request is accepted. |
| 2 | Retrieve the sprint-issue collection. | A collection of issues assigned to the sprint is returned. |
| 3 | Inspect the results. | The expected issue is included. |

### Overall Expected Result

Issues assigned to the intended sprint are returned successfully and include the expected issue.
