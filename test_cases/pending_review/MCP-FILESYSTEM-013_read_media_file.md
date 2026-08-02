---
scenario_id: MCP-FILESYSTEM-013
scenario_name: Read Media File from Allowed Path
business_feature: Media File Reading
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

`mcp-filesystem-read-media-file`

### Business Objective

Verify that an authorised caller can read a supported media file from an allowed filesystem path.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- A small supported media file exists inside an allowed directory.
- The expected MIME type and file signature are known.
- The read-media-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Media file path | A small supported image or media file |
| Expected MIME type | Known media type |
| Expected file signature | Known initial bytes or encoded marker |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the media file path. | The request is accepted. |
| 2 | Retrieve the media response. | Media content or an encoded representation is returned. |
| 3 | Inspect metadata and content. | The MIME type and decoded file signature match the source media file. |

### Overall Expected Result

The intended media file is returned successfully with the expected format and content.
