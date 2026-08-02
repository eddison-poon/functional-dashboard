---
scenario_id: MCP-FILESYSTEM-008
scenario_name: List Allowed Filesystem Directories
business_feature: Filesystem Access Policy
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

`mcp-filesystem-list-allowed-directories`

### Business Objective

Verify that the MCP tool returns the directories currently permitted by the filesystem access policy.

### Preconditions

- The caller is authorised to use the filesystem MCP server.
- At least one allowed directory is configured.
- The expected allowed test root is known.
- The list-allowed-directories tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Expected allowed root | A configured permitted directory path |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Invoke the list-allowed-directories tool. | The request is accepted. |
| 2 | Retrieve configured allowed directories. | A collection of permitted root paths is returned. |
| 3 | Inspect the returned paths. | The expected allowed test root is included. |

### Overall Expected Result

The configured allowed filesystem directories are returned successfully and include the expected test root.
