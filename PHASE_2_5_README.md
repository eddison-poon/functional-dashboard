# Phase 2.5 Drop-in Package

This package adds test-case governance, review folders, Jira publication scaffolding, a generated registry, and a GitHub Pages inventory page.

## Files to add

Copy every file and directory in this package to the repository root, preserving paths.

## Local setup

```bash
python -m pip install -r requirements-phase-2.5.txt
python scripts/validate_test_cases.py
python scripts/build_test_case_registry.py
```

To view the dashboard page locally, start an HTTP server from the repository root:

```bash
python -m http.server 8000
```

Then open `/reports/test_cases.html` through the local server.

## First authoring cycle

1. Copy `test_cases/templates/test_case_template.md`.
2. Rename it using the Scenario ID, for example `MCP-JIRA-001.md`.
3. Complete the file and place it in `test_cases/pending_review/`.
4. Run validation.
5. After approval, set `review_status: Approved`, complete reviewer fields, and move it to `test_cases/reviewed/`.
6. Run the Jira publisher without `--live` to inspect the payload.

```bash
python scripts/publish_test_cases_to_jira.py --scenario-id MCP-JIRA-001
```

## Jira configuration

Edit `config/jira.example.json` with the real Jira base URL, project key, issue type, and custom field IDs. Empty mappings are ignored.

For live local publication, provide these environment variables without committing them:

- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

Then run:

```bash
python scripts/publish_test_cases_to_jira.py --live --scenario-id MCP-JIRA-001
```

The live publisher uses Jira REST API v2 and assumes the issue type accepts a plain-text description. Jira project configuration and test-management plugins may require payload adjustments before first live use.

## GitHub Actions secrets

Create repository secrets with these exact names:

- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

The publication workflow is manually triggered and defaults to dry-run.

## Existing dashboard integration

Add a link from the existing dashboard navigation to:

```text
reports/test_cases.html
```

No existing Phase 2 canonical model files need to be changed for this package.
