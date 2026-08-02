---
scenario_id: MCP-JIRA-038
scenario_name: Search Jira Issues
business_feature: Issue Search
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

`mcp-jira-jira-search`

### Business Objective

Verify that an authorised caller can search Jira and retrieve an issue matching a known unique query.

### Preconditions

- The caller is authenticated and authorised to search the target issue.
- A searchable issue containing a unique known marker exists.
- The Jira MCP server and search tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Search query | A supported query or unique marker |
| Expected issue | The known matching issue key |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the supported search query. | The request is accepted. |
| 2 | Retrieve search results. | A collection of matching Jira issues is returned. |
| 3 | Inspect the results. | The expected issue is included and satisfies the query. |

### Overall Expected Result

Jira search returns the expected accessible issue for the submitted query.
