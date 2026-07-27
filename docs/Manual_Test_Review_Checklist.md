# Manual Test Definition Review Checklist

Use this checklist before moving a definition from `test_cases/manual/pending_review/` to `test_cases/manual/reviewed/`.

## 1. Parent Traceability

- [ ] `business_scenario_id` is present.
- [ ] The referenced Business Scenario exists and is approved.
- [ ] The definition preserves the approved business intent.
- [ ] `requirement_ids` are present and consistent with the parent.
- [ ] No unnecessary step-level mapping IDs are present.

## 2. Identity and Metadata

- [ ] `manual_test_id` follows `<CAPABILITY>-<MODULE>-M-<NNN>`.
- [ ] The ID is unique.
- [ ] The file name begins with the ID.
- [ ] Name, status, priority, test type and test level use approved standards.
- [ ] Capability, module and feature match the parent scenario.

## 3. Scope and Objective

- [ ] The objective clearly states what is verified.
- [ ] The definition covers one coherent verification path.
- [ ] It does not combine unrelated positive and negative paths.
- [ ] It does not invent new business behaviour.
- [ ] It does not duplicate another active definition.

## 4. Preconditions and Data

- [ ] Preconditions are complete and are not execution steps.
- [ ] Required access, permissions and system state are identified.
- [ ] Required test data is listed separately.
- [ ] Data values or selection rules are clear.
- [ ] No credentials, secrets or sensitive personal data are included.

## 5. Test Steps

- [ ] Steps are numbered from 1.
- [ ] Each row contains one primary tester action.
- [ ] Actions use clear verbs and are executable without interpretation.
- [ ] Navigation is sufficient but not excessive.
- [ ] No Business Step IDs or mapping IDs are required.
- [ ] No actual result, evidence or execution status appears.
- [ ] No unjustified environment-specific URL, build or date is embedded.

## 6. Expected Results

- [ ] Expected Results are objective and observable.
- [ ] Vague wording such as `works correctly` is not used.
- [ ] The final Expected Result proves the objective.
- [ ] Actual execution outcomes are not included.

## 7. Postconditions and Separation

- [ ] The expected end state or clean-up requirement is stated.
- [ ] No executor, execution timestamp, status, defect or evidence is included.
- [ ] Definition content is cleanly separated from Execution content.

## 8. Writing Quality

- [ ] Language is concise and professional.
- [ ] Terminology matches the Business Scenario.
- [ ] The approved template is followed.
- [ ] The definition is no more detailed than necessary for reliable execution.

## Review Decision

| Decision | Meaning |
|---|---|
| Approve | All mandatory checks pass |
| Return for update | Correctable issues remain |
| Reject | Invalid, duplicated or outside the approved scenario |

## Minimum Approval Rule

Do not approve unless the parent is approved, traceability is valid, the test is executable, Expected Results are measurable, and execution data is absent.