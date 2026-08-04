# Phase 3.7 Repository Verification Patch

## Required code changes

Replace:

- `python/dashboard_engine/discovery/scanner.py`
- `tests/test_repository_discovery.py`

The scanner now ignores `test_cases/templates/`, preventing template placeholders
from being treated as real Business Scenarios or Test Definitions.

## Repository cleanup

Delete the committed directory:

```text
tests/__pycache__/
```

It is already covered by `.gitignore`.

## Data gap

The repository currently contains:

- 135 Business Scenarios in pending review
- 135 Automation Test Definitions in pending review
- 0 actual Manual Test Definitions

Only the Manual Test Definition template is present. Add Manual Test Definitions
later if Manual coverage is expected.

## Verified results after patch

- Full suite before patch: 627 tests passed
- Discovery tests after patch: 7 tests passed
- Phase 3.7 CLI: clean exit
- Discovery issues: 0
- Indexing issues: 0
- Ignored indexed assets: 0
- Scenarios: 135
- Automation Test Definitions: 135
- Manual Test Definitions: 0
