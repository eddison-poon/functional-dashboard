---
scenario_id: MCP-JIRA-029
scenario_name: Retrieve Sprints from Jira Board
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

`mcp-jira-jira-get-sprints-from-board`

### Business Objective

Verify that an authorised caller can retrieve sprints associated with a Jira board.

### Preconditions

- The caller is authenticated and authorised to view the target board.
- The board exists and contains at least one known sprint.
- The Jira MCP server and get-sprints-from-board tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Board ID | A valid Jira board identifier |
| Expected sprint | A known sprint ID or name |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the board ID. | The request is accepted. |
| 2 | Retrieve the sprint collection. | A collection of board sprints is returned. |
| 3 | Inspect the results. | The expected sprint is included and associated with the board. |

### Overall Expected Result

Sprints associated with the intended Jira board are returned successfully and include the expected sprint.
