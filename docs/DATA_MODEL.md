# Canonical Data Model

## Capability group

Examples:

- MCP Marketplace
- Skills Marketplace
- Knowledge Base
- Team Management

## Capability

Examples:

- Jira MCP
- Confluence MCP
- Code Reviewer
- Workflow Team

## Feature

The final user-visible capability in a flow.

Examples:

- Create Jira Ticket
- View Confluence Page
- Review Java Code

## Scenario

A functional behaviour or variation belonging to one feature.

Each scenario may reference:

- Jira requirement
- manual test definition
- automation test definition
- current manual status
- current automation status
- zero or more immutable executions

## Execution

Required fields:

```json
{
  "execution_id": "EXE-20260722-175841-0002",
  "status": "PASSED",
  "environment": "SIT",
  "build": "2.3.18",
  "executed_at": "2026-07-22T17:58:41+08:00"
}
```

Execution records are append-only. The generated dashboard snapshot calculates
the latest execution without deleting earlier evidence.
