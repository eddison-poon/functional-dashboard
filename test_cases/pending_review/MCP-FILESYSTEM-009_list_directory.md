---
scenario_id: MCP-FILESYSTEM-009
scenario_name: List Directory Entries
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

`mcp-filesystem-list-directory`

### Business Objective

Verify that an authorised caller can list the immediate entries of an allowed directory.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target directory exists within an allowed root.
- The directory contains known child entries.
- The list-directory tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Directory path | A controlled test directory |
| Expected entries | Known immediate child file and directory names |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target directory path. | The request is accepted. |
| 2 | Retrieve the directory listing. | A collection of immediate child entries is returned. |
| 3 | Inspect the listing. | The expected child file and directory are included. |

### Overall Expected Result

The immediate contents of the intended directory are returned successfully.
