---
scenario_id: MCP-FILESYSTEM-001
scenario_name: Append Content to Existing File
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

`mcp-filesystem-append-file`

### Business Objective

Verify that an authorised caller can append valid content to an existing file located within an allowed filesystem directory.

### Preconditions

- The caller is authenticated and authorised to use the filesystem MCP server.
- A writable text file exists inside an allowed directory.
- The target path is permitted by the filesystem access policy.
- The append-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target file | A disposable writable text file within an allowed directory |
| Append content | A unique non-empty text marker |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target file path and valid append content. | The request is accepted. |
| 2 | Confirm the append operation. | The tool reports successful completion. |
| 3 | Read the updated file. | The original content is preserved and the appended marker appears at the end. |

### Overall Expected Result

The supplied content is appended successfully to the intended file without overwriting existing content.
