---
scenario_id: ARK-SANDBOX-004
scenario_name: Download File from Sandbox
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

`ark-sandbox-download-file`

### Business Objective

Verify that an authorised caller can download an existing file from a sandbox.

### Preconditions

- The caller is authenticated and authorised to access the sandbox.
- The target sandbox is running and usable.
- A known file exists at an allowed path inside the sandbox.
- The download-file tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Sandbox reference | A valid running sandbox |
| Remote file path | A known file inside the sandbox |
| Expected content marker | Known file content or checksum |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the sandbox reference and remote file path. | The request is accepted. |
| 2 | Retrieve the file response. | A downloadable file or encoded file content is returned. |
| 3 | Validate the downloaded content. | The file name, size and content marker or checksum match the source file. |

### Overall Expected Result

The intended sandbox file is downloaded successfully and matches the source content.
