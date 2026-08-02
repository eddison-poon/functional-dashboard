---
scenario_id: ARK-SANDBOX-009
scenario_name: Upload File to Sandbox
business_feature: Sandbox File Transfer
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

`ark-sandbox-upload-file`

### Business Objective

Verify that an authorised caller can upload a valid file to a running sandbox.

### Preconditions

- The caller is authenticated and authorised to access the sandbox.
- The target sandbox is running and usable.
- The destination path is allowed and writable.
- A small non-sensitive test file is available.
- The upload-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox reference | A valid running sandbox |
| Local test file | A small non-sensitive file |
| Remote destination path | A writable sandbox path |
| Expected checksum or marker | Known source file content |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the sandbox reference, local file and destination path. | The request is accepted. |
| 2 | Confirm the upload operation. | The tool reports successful completion. |
| 3 | Download or read the remote file. | The uploaded file exists at the destination. |
| 4 | Validate the content. | The downloaded content or checksum matches the original file. |

### Overall Expected Result

The file is uploaded successfully to the intended sandbox path and its content is preserved.
