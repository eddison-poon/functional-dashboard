---
scenario_id: MCP-FILESYSTEM-017
scenario_name: Retrieve Filesystem Workspace Information
business_feature: Workspace Metadata
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

`mcp-filesystem-workspace-info`

### Business Objective

Verify that the MCP tool returns the configured filesystem workspace information available to the caller.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- A filesystem workspace is configured.
- Expected workspace metadata is known.
- The workspace-info tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Expected workspace marker | A configured workspace root, name or identifier |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Invoke the workspace-info tool. | The request is accepted. |
| 2 | Retrieve workspace information. | A workspace metadata response is returned. |
| 3 | Inspect the response. | The expected workspace root, name or identifier is included. |

### Overall Expected Result

The configured filesystem workspace information is returned successfully and matches the expected environment.
