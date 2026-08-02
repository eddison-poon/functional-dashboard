---
scenario_id: MCP-FILESYSTEM-018
scenario_name: Write File to Allowed Filesystem Path
business_feature: File Content Management
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

`mcp-filesystem-write-file`

### Business Objective

Verify that an authorised caller can create or overwrite a file with valid content inside an allowed filesystem directory.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target parent directory exists and is writable.
- The target path is inside an allowed root.
- The write-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target file path | A unique disposable file path |
| File content | A unique non-empty text value |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target path and valid content. | The request is accepted. |
| 2 | Confirm the write operation. | The tool reports successful completion. |
| 3 | Read the target file. | The file exists and its content exactly matches the submitted value. |

### Overall Expected Result

The file is written successfully at the intended allowed path with the submitted content.
