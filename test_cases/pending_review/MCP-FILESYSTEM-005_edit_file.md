---
scenario_id: MCP-FILESYSTEM-005
scenario_name: Edit Existing Text File
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

`mcp-filesystem-edit-file`

### Business Objective

Verify that an authorised caller can apply a valid line-based edit to an existing text file within an allowed directory.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- A writable text file exists inside an allowed directory.
- The existing content contains a known target value.
- The edit-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target file | A disposable text file |
| Existing text | A known value present in the file |
| Replacement text | A unique valid replacement value |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target file and valid edit instruction. | The request is accepted. |
| 2 | Confirm the edit operation. | The tool reports successful completion. |
| 3 | Read the updated file. | The target text is replaced as intended and unrelated content remains unchanged. |

### Overall Expected Result

The intended text file is edited successfully with the requested change.
