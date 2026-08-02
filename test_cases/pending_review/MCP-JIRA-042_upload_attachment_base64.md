---
scenario_id: MCP-JIRA-042
scenario_name: Upload Base64 Attachment to Jira Issue
business_feature: Attachment Management
business_module: Jira
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

`mcp-jira-jira-upload-attachment-base64`

### Business Objective

Verify that an authorised caller can upload a valid Base64-encoded file attachment to an existing Jira issue.

### Preconditions

- The caller is authenticated and authorised to add attachments to the target issue.
- The target Jira issue exists and attachments are enabled.
- The file type and size are permitted by Jira configuration.
- A valid Base64-encoded test file and matching filename are available.
- The Jira MCP server and upload-attachment-base64 tool are available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Issue reference | A valid disposable Jira issue key or ID |
| Filename | A unique permitted filename such as `mcp-jira-a-042.txt` |
| MIME type | A valid supported type such as `text/plain` when required |
| Base64 content | Valid Base64 encoding of known non-sensitive test content |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the issue reference, filename, supported MIME type and valid Base64 content. | The request is accepted without validation or permission errors. |
| 2 | Confirm the attachment upload. | The tool reports successful completion and returns attachment metadata or a success response. |
| 3 | Retrieve or inspect the target issue attachments. | The uploaded attachment is listed with the submitted filename and expected size or MIME type. |
| 4 | Open or download the attachment through an approved verification method. | The decoded content matches the original test file content. |

### Overall Expected Result

The Base64-encoded file is uploaded successfully to the intended Jira issue and its content and metadata can be verified.
