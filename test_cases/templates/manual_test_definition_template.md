---
manual_test_id: <CAPABILITY-MODULE-M-NNN>
business_scenario_id: <APPROVED-BUSINESS-SCENARIO-ID>
name: <Concise manual test definition name>
status: DRAFT
priority: <CRITICAL|HIGH|MEDIUM|LOW>
test_type: FUNCTIONAL
test_level: <COMPONENT|INTEGRATION|SYSTEM|ACCEPTANCE>
capability: <Capability>
business_module: <Business module>
business_feature: <Business feature>
requirement_ids:
  - <Requirement ID>
jira_id:
owner: <Owner or team>
---

# Manual Test Definition: <Name>

## Objective

<State what this definition verifies.>

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | <Business Scenario ID> |
| Business Scenario Name | <Business Scenario name> |
| Coverage | <Single verification path covered> |

## Preconditions

- <Required condition before execution>
- <Required access, permission or system state>

Use `- None` only when no precondition is genuinely required.

## Required Test Data

| Data Item | Value or Selection Rule |
|---|---|
| <Data item> | <Explicit value or selection rule> |

Use `| None | No test data is required |` only when genuinely applicable.

## Test Steps

| Step | Action | Expected Result |
|---:|---|---|
| 1 | <Tester action> | <Observable expected result> |
| 2 | <Tester action> | <Observable expected result> |
| 3 | <Tester action> | <Observable expected result> |

Add or remove rows as required.

Do not add Business Step IDs, mapping IDs, actual results, pass/fail status or execution evidence.

## Postconditions

- <Expected end state or clean-up requirement>

Use `- None` only when no postcondition applies.

## Notes

- <Optional governance or maintenance note>
- Environment, build, actual result, evidence and execution status belong to Execution.

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |