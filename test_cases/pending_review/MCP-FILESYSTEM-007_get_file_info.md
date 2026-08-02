---
scenario_id: MCP-FILESYSTEM-007
scenario_name: Retrieve Filesystem Path Information
business_feature: Path Metadata
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

`mcp-filesystem-get-file-info`

### Business Objective

Verify that an authorised caller can retrieve metadata for an existing file or directory within an allowed path.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- The target file or directory exists inside an allowed location.
- Expected path metadata is known.
- The get-file-info tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Target path | A known test file or directory |
| Expected type | File or directory |
| Expected size marker | Known file size when testing a file |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the target path. | The request is accepted. |
| 2 | Retrieve path metadata. | Information about the target path is returned. |
| 3 | Inspect metadata. | The returned path type and supported attributes match the target object. |

### Overall Expected Result

Metadata for the intended filesystem object is returned successfully and matches its known state.
