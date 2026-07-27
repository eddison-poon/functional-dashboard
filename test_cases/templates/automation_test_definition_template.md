---
automation_test_id: <CAPABILITY-MODULE-A-NNN>
business_scenario_id: <APPROVED-BUSINESS-SCENARIO-ID>
name: <Concise automation test definition name>
status: DRAFT
priority: <CRITICAL|HIGH|MEDIUM|LOW>
test_type: FUNCTIONAL
test_level: <COMPONENT|INTEGRATION|SYSTEM|ACCEPTANCE>
automation_framework: PLAYWRIGHT
automation_language: TYPESCRIPT
capability: <Capability>
business_module: <Business module>
business_feature: <Business feature>
requirement_ids:
  - <Requirement ID>
tags:
  - <regression|smoke|other>
  - <capability tag>
  - <module tag>
script_path: automation/playwright/tests/<capability>/<module>/<name>.spec.ts
jira_id:
owner: <Owner or team>
---

# Automation Test Definition: <Name>

## Objective

<State clearly what the automation verifies.>

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | <Business Scenario ID> |
| Business Scenario Name | <Business Scenario name> |
| Coverage | <Single automated verification path> |

## Automation Suitability

| Assessment | Value |
|---|---|
| Suitability | <SUITABLE|PARTIALLY_SUITABLE|NOT_CURRENTLY_SUITABLE> |
| Rationale | <Why this path should or should not be automated> |

## Automation Scope

<State what is automated and what is excluded.>

## Preconditions

- <Environment or service condition>
- <Authentication or permission condition>
- <Required reference data or setup>

## Required Test Data

| Data Item | Value or Generation Rule |
|---|---|
| <Data item> | <Secure value source or generation rule> |

Do not include passwords, tokens or secrets.

## Automated Flow and Assertions

| Step | Automated Action | Required Assertion |
|---:|---|---|
| 1 | <Automated action> | <Observable assertion> |
| 2 | <Automated action> | <Observable assertion> |
| 3 | <Automated action> | <Observable assertion> |

Do not add Business Step IDs or code-step mapping IDs.

## Locator Strategy

- <Preferred accessible locator>
- <Approved test ID when necessary>
- <Application-specific locator information still required>

## Implementation Notes

- Framework: Playwright
- Language: TypeScript
- Script path: `<repository-relative path>`
- Configuration values must be externalised.
- Execution results and evidence belong to the Execution record.

## Cleanup

- <Cleanup action or `None`>

## Expected Execution Outputs

- Playwright test result
- Configured report output
- Trace, screenshot or video according to policy
- Execution metadata associated with `automation_test_id`

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | <Name> | <YYYY-MM-DD> | Submitted |
| Reviewer | <Name> | <YYYY-MM-DD> | <Approved|Returned|Rejected> |
