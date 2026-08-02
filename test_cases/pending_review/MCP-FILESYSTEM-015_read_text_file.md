---
scenario_id: MCP-FILESYSTEM-015
scenario_name: Read Text File from Allowed Path
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

`mcp-filesystem-read-text-file`

### Business Objective

Verify that an authorised caller can read the text content of an existing text file within an allowed directory.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- A valid text file exists inside an allowed directory.
- The file encoding is supported.
- The read-text-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target file | A known UTF-8 text file |
| Expected text | Known exact or unique content |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target text-file path. | The request is accepted. |
| 2 | Retrieve the text content. | Text is returned without binary encoding. |
| 3 | Compare the content. | The returned text matches the known source content. |

### Overall Expected Result

The intended text file is read successfully and its returned text matches the source.
