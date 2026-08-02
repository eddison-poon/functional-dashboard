---
scenario_id: MCP-FILESYSTEM-002
scenario_name: Create Directory in Allowed Filesystem Path
business_feature: Directory Management
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

`mcp-filesystem-create-directory`

### Business Objective

Verify that an authorised caller can create a new directory within an allowed filesystem location.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The parent path exists and is writable.
- The target directory does not already exist.
- The create-directory tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Parent path | A writable allowed directory |
| Directory name | A unique valid directory name |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the new directory path. | The request is accepted. |
| 2 | Confirm directory creation. | The tool reports successful completion. |
| 3 | List the parent directory. | The new directory is included in the returned entries. |

### Overall Expected Result

A new directory is created successfully at the intended allowed path.
