---
scenario_id: MCP-FILESYSTEM-006
scenario_name: Find Files by Supported Criteria
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

`mcp-filesystem-find-files`

### Business Objective

Verify that an authorised caller can find files within an allowed directory using supported matching criteria.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The search root is within an allowed directory.
- At least one known file matches the configured criteria.
- The find-files tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Search root | A controlled test directory |
| Matching criterion | A supported filename or pattern |
| Expected file | A known matching path |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the search root and supported matching criterion. | The request is accepted. |
| 2 | Retrieve matching files. | A collection of matching paths is returned. |
| 3 | Inspect the results. | The expected file is included and non-matching test files are excluded where applicable. |

### Overall Expected Result

Files matching the submitted criteria are returned successfully from the intended allowed directory.
