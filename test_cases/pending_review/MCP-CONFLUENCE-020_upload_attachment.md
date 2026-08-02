---
scenario_id: MCP-CONFLUENCE-020
scenario_name: Upload Attachment to Confluence Page
business_feature: Attachment Management
business_module: Confluence
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

`mcp-confluence-upload-attachment`

### Business Objective

Verify that an authorised caller can upload a valid file attachment to an existing Confluence page.

### Preconditions

- The caller is authenticated and authorised to add attachments to the target page.
- The target page exists inside an approved test space.
- The file type and size comply with Confluence configuration.
- A small non-sensitive test file is available.
- The upload-attachment tool is available.

### Test Data

| Data Item | Value / Rule |
|---|---|
| Page reference | A valid disposable or approved test page |
| Filename | A unique permitted filename |
| File content | Known non-sensitive test content |
| MIME type | A supported type when required |

### Business Steps

| Step | Action | Expected Outcome |
|---:|---|---|
| 1 | Submit the page reference and valid attachment file. | The request is accepted. |
| 2 | Confirm the upload operation. | The tool reports successful completion and returns attachment metadata or a success response. |
| 3 | Retrieve or inspect page attachments. | The uploaded filename is listed with expected metadata. |
| 4 | Open or download the attachment using an approved method. | The content matches the original test file. |

### Overall Expected Result

The attachment is uploaded successfully to the intended page and its metadata and content are verifiable.
