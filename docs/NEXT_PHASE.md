# Next Implementation Phase

The repository contains a working sample-data pipeline and a formal connector boundary.
The next phase can implement separate Python programs for:

1. Jira extraction and pagination
2. Mandatory-field validation
3. Jira label mapping
4. Test-definition ingestion
5. Manual execution ingestion
6. Automated execution ingestion
7. Execution ID generation
8. Snapshot scheduling and archival
9. Defect correlation
10. Historical trend generation

These programs should produce the canonical input format consumed by
`build_snapshot.py`; the HTML, CSS, and JavaScript should not need to change.
