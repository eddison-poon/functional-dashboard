# Automation Test Definition and Playwright Review Checklist

## Definition Review

### Traceability

- [ ] `business_scenario_id` is present and approved.
- [ ] `requirement_ids` are preserved.
- [ ] The definition does not depend on a Manual Test Definition.
- [ ] No step-level mapping IDs are introduced.

### Metadata

- [ ] `automation_test_id` follows `<CAPABILITY>-<MODULE>-A-<NNN>`.
- [ ] Framework is `PLAYWRIGHT`.
- [ ] Language is `TYPESCRIPT` unless approved otherwise.
- [ ] Status, priority, test type and level are valid.
- [ ] Capability, module and feature match the parent.
- [ ] Tags are stable and meaningful.

### Scope and Suitability

- [ ] Suitability is assessed.
- [ ] Scope and exclusions are clear.
- [ ] The path is coherent and non-duplicated.
- [ ] No unsupported business behaviour is added.

### Preconditions and Data

- [ ] Setup is reliable and repeatable.
- [ ] Authentication is secure.
- [ ] Data generation avoids collisions.
- [ ] Cleanup is identified where needed.
- [ ] No secrets are stored in the definition.

### Flow and Assertions

- [ ] Automated actions are clear.
- [ ] Important outcomes have assertions.
- [ ] Assertions prove the objective.
- [ ] No actual execution result appears in the definition.

## Playwright Code Review

### Traceability

- [ ] Automation Test ID appears in title, tag or annotation.
- [ ] Business Scenario ID appears in title, tag or annotation.
- [ ] `script_path` matches the actual file.

### Isolation and Stability

- [ ] The test runs independently.
- [ ] Execution order is irrelevant.
- [ ] Fixed waits are avoided.
- [ ] Retries do not conceal flakiness.

### Locators

- [ ] Accessible locators are preferred.
- [ ] Generated CSS and deep XPath are avoided.
- [ ] Locators are specific enough to avoid false matches.

### Assertions

- [ ] Assertions verify business outcomes.
- [ ] Final assertions prove the expected behaviour.
- [ ] Failures produce useful diagnostic information.

### Security and Configuration

- [ ] Base URL and environment data are externalised.
- [ ] Credentials and tokens are externalised.
- [ ] No secret is logged or committed.

### Maintainability

- [ ] Test naming is clear.
- [ ] `test.step` is used only where useful.
- [ ] Helpers or page objects provide real reuse.
- [ ] Abstraction is not excessive.

### Reporting

- [ ] Failure evidence follows project policy.
- [ ] Tags support regression and dashboard grouping.
- [ ] Results can be associated with `automation_test_id`.

## Minimum Implementation Approval

A script may be marked `IMPLEMENTED` only when the definition is approved, traceability is present, secure configuration is used, assertions are complete, the test runs independently, review passes and one controlled execution succeeds.
