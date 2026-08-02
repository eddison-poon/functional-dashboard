---
scenario_id: MCP-FILESYSTEM-014
scenario_name: Read Multiple Files in One Request
business_feature: File Reading
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

`mcp-filesystem-read-multiple-files`

### Business Objective

Verify that an authorised caller can read multiple existing files from allowed filesystem paths in one request.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- Two or more supported files exist within allowed directories.
- Each file contains known content.
- The read-multiple-files tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| File paths | Two or more valid file paths |
| Expected markers | One unique marker per file |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit all target file paths in one request. | The request is accepted. |
| 2 | Retrieve the multi-file response. | A result is returned for each submitted file. |
| 3 | Inspect each result. | Each file result is associated with the correct path and contains its expected marker. |

### Overall Expected Result

All submitted files are read successfully and each returned result matches the correct source file.
