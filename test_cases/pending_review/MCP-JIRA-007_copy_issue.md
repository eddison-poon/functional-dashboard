---
scenario_id: MCP-JIRA-007
scenario_name: Copy Existing Jira Issue
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

`mcp-jira-jira-copy-issue`

### Business Objective

Verify that an authorised caller can copy an existing Jira issue into a new issue using supported copy options.

### Preconditions

- The caller is authenticated and authorised to browse the source issue and create issues.
- A suitable source issue exists.
- The destination project and issue type are valid when configurable.
- The Jira MCP server and copy-issue tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Source issue | A valid existing issue |
| Destination configuration | Supported target project or issue type when required |
| New summary | A unique copied-issue summary when supported |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the source issue and supported copy options. | The request is accepted. |
| 2 | Confirm the copy operation. | A new issue is created and a new issue key is returned. |
| 3 | Retrieve the copied issue. | The new issue contains the expected copied fields and is distinct from the source. |

### Overall Expected Result

A new Jira issue is created successfully from the source issue with the expected copied information.
