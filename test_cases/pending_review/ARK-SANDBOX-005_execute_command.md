---
scenario_id: ARK-SANDBOX-005
scenario_name: Execute Shell Command in Sandbox
business_feature: Sandbox Command Execution
business_module: Ark Sandbox
priority: High
test_type: Functional
category: Sandbox Integration
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

### Tool

`ark-sandbox-execute-command`

### Business Objective

Verify that an authorised caller can execute an approved shell command inside a running sandbox and retrieve its output.

### Preconditions

- The caller is authenticated and authorised to execute commands.
- The target sandbox is running and usable.
- The command is permitted by the sandbox execution policy.
- The execute-command tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox reference | A valid running sandbox |
| Command | A safe deterministic command such as printing a unique marker |
| Expected exit code | Zero |
| Expected stdout | The generated marker |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the sandbox reference and approved command. | The request is accepted. |
| 2 | Execute the command. | The tool returns command completion metadata. |
| 3 | Inspect command results. | The exit code is zero, stdout contains the expected marker and stderr is empty or acceptable. |

### Overall Expected Result

The approved command executes successfully in the intended sandbox and returns the expected output.
