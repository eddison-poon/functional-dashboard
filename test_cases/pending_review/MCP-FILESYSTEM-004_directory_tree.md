---
scenario_id: MCP-FILESYSTEM-004
scenario_name: Retrieve Recursive Directory Tree
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

`mcp-filesystem-directory-tree`

### Business Objective

Verify that an authorised caller can retrieve a recursive tree view of files and directories beneath an allowed root path.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target root directory exists within the allowed filesystem scope.
- The directory contains a known nested structure.
- The directory-tree tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Root path | A test directory containing known child files and nested directories |
| Expected nested entry | A known descendant path |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the allowed root directory path. | The request is accepted. |
| 2 | Retrieve the recursive directory tree. | A hierarchical representation is returned. |
| 3 | Inspect the returned hierarchy. | The expected nested directory and file entries are included in the correct structure. |

### Overall Expected Result

The recursive tree for the intended directory is returned successfully with the expected hierarchy.
