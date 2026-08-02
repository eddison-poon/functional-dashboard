---
scenario_id: MCP-FILESYSTEM-003
scenario_name: Delete File or Directory from Allowed Path
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

`mcp-filesystem-delete-path`

### Business Objective

Verify that an authorised caller can delete a disposable file or directory located inside an allowed filesystem path.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- A disposable target path exists within an allowed directory.
- The target may safely be deleted.
- The delete-path tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target path | A disposable file or empty directory inside an allowed location |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the disposable target path. | The request is accepted. |
| 2 | Confirm path deletion. | The tool reports successful completion. |
| 3 | Attempt to retrieve or list the deleted path. | The path is not returned as an existing active filesystem object. |

### Overall Expected Result

The intended disposable filesystem path is deleted successfully and is no longer retrievable.
