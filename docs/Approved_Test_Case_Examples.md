# Approved Test Case Examples

The examples in this document demonstrate expected authoring quality. The machine-readable source example is stored in `test_cases/published/MCP-JIRA-001.md` only after a real Jira ticket exists. Until then, use the template and the example below as guidance.

## Example — Create Jira Issue with Mandatory Fields

| Field | Value |
|---|---|
| Scenario ID | `MCP-JIRA-001` |
| Scenario Name | Create Jira Issue with Mandatory Fields |
| Business Feature | Issue Management |
| Business Module | Jira |
| Priority | High |
| Test Type | Functional |
| Category | MCP Integration |
| Manual Exists | Yes |
| Automation Exists | Yes |

### Business Objective

Verify that an authorized user or supported MCP client can create a Jira issue using only the mandatory fields.

### Preconditions

- The caller is authenticated.
- The caller has permission to create issues in the target Jira project.
- Jira and the supported MCP path are available.

### Test Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit valid values for all mandatory issue fields. | The request is accepted without validation errors. |
| 2 | Confirm the issue-creation request. | A new issue is created and a unique issue key is returned. |
| 3 | Retrieve or open the created issue. | The issue exists in the target project with the submitted values. |

### Overall Expected Result

A new Jira issue is created successfully, assigned a unique Jira issue key, and stored in the intended project with the submitted mandatory values.
