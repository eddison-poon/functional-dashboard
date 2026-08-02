---
scenario_id: MCP-FILESYSTEM-010
scenario_name: List Directory Entries with Sizes
business_feature: Directory Inspection
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

`mcp-filesystem-list-directory-with-sizes`

### Business Objective

Verify that an authorised caller can list directory entries together with supported size information.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target directory exists within an allowed root.
- The directory contains files with known sizes.
- The list-directory-with-sizes tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Directory path | A controlled test directory |
| Expected file | A known child file |
| Expected size | The known byte size of the child file |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target directory path. | The request is accepted. |
| 2 | Retrieve directory entries with sizes. | A collection of entries and supported size data is returned. |
| 3 | Inspect the expected file. | The file appears with the correct known size. |

### Overall Expected Result

Directory entries and their supported size information are returned successfully.
