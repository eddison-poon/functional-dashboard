# Automation Test Definition Workflow

## Workflow

```text
Approved Business Scenario
          ↓
Generate Automation Test Definition
          ↓
test_cases/automation/pending_review/
          ↓
Definition review
          ↓
test_cases/automation/reviewed/
          ↓
Implement Playwright script
          ↓
Code review and controlled execution
          ↓
test_cases/automation/implemented/
```

## Generate

Inputs:

```text
Approved Business Scenario
docs/Automation_Testing_Standards.md
docs/Approved_Automation_Test_Definition_Example.md
docs/Playwright_Implementation_Guide.md
test_cases/templates/automation_test_definition_template.md
prompts/Automation_Test_Definition_Generator.md
```

New definitions use `DRAFT`.

## Review

Use `docs/Automation_Test_Review_Checklist.md`. When approved, set status to `APPROVED` and move the file to `reviewed`.

## Implement

Create the script under the approved `script_path`, add both traceability IDs, implement setup, actions, assertions and cleanup, externalise environment settings and submit for code review.

## Controlled Execution

When code review passes and the script completes a controlled execution successfully, set status to `IMPLEMENTED` and move the definition to `implemented`.

## Change Handling

When the Business Scenario changes, search by `business_scenario_id`, reassess affected definitions, update definitions first, then update and re-run scripts. Retain IDs unless an artefact is retired and replaced by materially different coverage.

## Execution Separation

Execution records hold environment, build, cycle, status, duration, evidence, errors, defects and timestamps. These values do not belong in the reusable definition.
