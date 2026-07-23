# Phase 2.5 — Test Case Governance and Jira Publishing

## Workflow

```text
Author creates Markdown test case
        ↓
test_cases/pending_review/
        ↓
Automated validation + human review
        ↓
test_cases/reviewed/
        ↓
Manual Jira publication workflow
        ↓
Jira ID returned and written to metadata
        ↓
test_cases/published/
        ↓
data/test_case_registry.json
        ↓
reports/test_cases.html
```

## State rules

| State | Folder | Metadata | Jira ID |
|---|---|---|---|
| Pending | `pending_review/` | `Pending` | Empty |
| Approved | `reviewed/` | `Approved` | Empty |
| Published | `published/` | `Published` | Required |
| Rejected | `rejected/` | `Rejected` | Empty unless previously published |

## Contributor process

1. Copy the test-case template.
2. Complete the mandatory metadata and Markdown sections.
3. Place the file in `pending_review/`.
4. Open a pull request.
5. Correct validation or review findings.

## Reviewer process

1. Run or confirm automated validation.
2. Complete the review checklist.
3. Update approval metadata.
4. Move the file to `reviewed/`.
5. Merge the pull request.

## Publisher process

1. Configure Jira locally or in protected GitHub secrets.
2. Run the publisher in dry-run mode.
3. Review the generated Jira payloads.
4. Run live publication through the manual GitHub Action or command line.
5. Commit changed Markdown files, registry, and dashboard output.

## Safety controls

- Publication is dry-run by default.
- Only Approved files in `reviewed/` are eligible.
- Files with an existing Jira ID are skipped.
- Scenario IDs already present as Published in the registry are skipped.
- Jira secrets must never be committed.
- The publisher stops on an individual error and leaves the source file in `reviewed/` for retry.
