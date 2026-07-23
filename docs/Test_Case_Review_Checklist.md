# Test Case Review Checklist

Use this checklist before moving a file from `pending_review/` to `reviewed/`.

## Identity and classification

- [ ] File name exactly matches `<scenario_id>.md`.
- [ ] Scenario ID is unique and follows the naming convention.
- [ ] Scenario name describes one clear business behaviour.
- [ ] Module, feature, category, priority, and test type are correctly assigned.
- [ ] At least one of Manual Exists or Automation Exists is true.

## Content quality

- [ ] Business objective explains what is being verified and why.
- [ ] Preconditions are complete, concise, and reusable.
- [ ] Test data is provided where specific values or rules are required.
- [ ] Steps are ordered, reproducible, and limited to one action per row where practical.
- [ ] Each step has an observable expected outcome.
- [ ] Overall expected result is measurable.
- [ ] Negative, permission, validation, or error behaviour is not accidentally mixed into a separate happy-path scenario.

## Model compliance

- [ ] No environment, build, execution date, tester, or result appears in the reusable definition.
- [ ] No Jira ID has been invented or manually assigned before publication.
- [ ] Manual and automation flags describe availability, not execution status.
- [ ] Scenario Pattern is left blank unless intentionally used as optional metadata.

## Approval actions

- [ ] Automated validation passes.
- [ ] Reviewer updates `review_status: Approved`.
- [ ] Reviewer records `reviewed_by` and `reviewed_date`.
- [ ] File is moved to `test_cases/reviewed/` in the same pull request.
