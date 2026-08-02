---
scenario_id: MCP-FILESYSTEM-011
scenario_name: Move File within Allowed Filesystem
business_feature: Path Management
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

`mcp-filesystem-move-file`

### Business Objective

Verify that an authorised caller can move a file from one allowed path to another allowed path.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- A disposable source file exists.
- The destination parent directory exists and is writable.
- The destination path does not already exist.
- The move-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Source path | A disposable source file |
| Destination path | A valid new path within an allowed directory |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the source and destination paths. | The request is accepted. |
| 2 | Confirm the move operation. | The tool reports successful completion. |
| 3 | Inspect source and destination locations. | The source path is absent and the destination file exists. |
| 4 | Read the destination file. | Its content matches the original source content. |

### Overall Expected Result

The file is moved successfully to the intended destination without changing its content.
