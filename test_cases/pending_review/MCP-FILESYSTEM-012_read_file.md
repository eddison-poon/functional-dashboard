---
scenario_id: MCP-FILESYSTEM-012
scenario_name: Read Existing File
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

`mcp-filesystem-read-file`

### Business Objective

Verify that an authorised caller can read an existing supported file from an allowed filesystem path.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target file exists inside an allowed directory.
- The file format is supported by the tool.
- The read-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target file | A known supported file |
| Expected content marker | Known content contained in the file |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target file path. | The request is accepted. |
| 2 | Retrieve the file content. | A non-empty file response is returned. |
| 3 | Inspect the response. | The expected content marker or encoded data is present according to the tool contract. |

### Overall Expected Result

The intended file is read successfully and its returned content matches the known source.
