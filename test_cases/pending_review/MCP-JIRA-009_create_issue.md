---
scenario_id: MCP-JIRA-009
scenario_name: Create Jira Issue with Mandatory Fields
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

`mcp-jira-jira-create-issue`

### Business Objective

Verify that an authorised caller can create a Jira issue by supplying all mandatory fields.

### Preconditions

- The caller is authenticated and authorised to create issues in the target project.
- The target project exists and supports the selected issue type.
- Mandatory fields and valid values are known.
- The Jira MCP server and create-issue tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Project | A valid project key or ID |
| Issue type | A supported issue type such as Task |
| Summary | A unique valid summary |
| Description | Valid non-empty content |
| Other mandatory fields | Valid project-specific values |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid mandatory issue data. | The request is accepted without validation or permission errors. |
| 2 | Confirm issue creation. | A new Jira issue is created and a unique issue key is returned. |
| 3 | Retrieve the created issue. | The issue exists and its submitted mandatory fields match. |

### Overall Expected Result

A new Jira issue is created successfully with a unique key and the submitted mandatory values.
