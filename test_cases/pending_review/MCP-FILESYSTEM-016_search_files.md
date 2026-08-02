---
scenario_id: MCP-FILESYSTEM-016
scenario_name: Search Files within Allowed Directory
business_feature: File Discovery
business_module: Filesystem
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

`mcp-filesystem-search-files`

### Business Objective

Verify that an authorised caller can search for files within an allowed directory using supported search criteria.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The search root is an allowed directory.
- At least one known test file matches the search criteria.
- The search-files tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Search root | A controlled test directory |
| Search query | A supported filename or content criterion |
| Expected result | A known matching file path |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the search root and supported query. | The request is accepted. |
| 2 | Retrieve search results. | A collection of matching files is returned. |
| 3 | Inspect the results. | The expected file is included and corresponds to the submitted query. |

### Overall Expected Result

The expected file is returned successfully for the submitted filesystem search query.
