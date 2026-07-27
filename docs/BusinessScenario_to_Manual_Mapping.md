# Business Scenario to Manual Test Definition Mapping

## 1. Purpose

This document explains how an approved Business Scenario becomes one or more Manual Test Definitions. Phase 2.6 uses **parent-level document traceability only**.

## 2. Relationship

```text
One Business Scenario
        ↓
One or more Manual Test Definitions
```

Example:

```text
MCP-JIRA-001 — Create Jira ticket
        ├── MCP-JIRA-M-001 — Create with mandatory fields
        ├── MCP-JIRA-M-002 — Reject missing Summary
        └── MCP-JIRA-M-003 — Reject unauthorised user
```

Each child contains:

```text
business_scenario_id: MCP-JIRA-001
```

No separate mapping record is required.

## 3. Content Mapping

| Business Scenario | Manual Test Definition |
|---|---|
| Scenario ID | `business_scenario_id` |
| Name and objective | Manual name and objective |
| Capability | Capability metadata |
| Business module | Business module metadata |
| Business feature | Business feature metadata |
| Priority | Normally inherited priority |
| Requirement IDs | `requirement_ids` |
| Preconditions | Executable preconditions |
| Business flow | Detailed tester actions |
| Expected outcome | Observable Expected Results |
| Material variations | Separate Manual Test Definitions |

## 4. Not Required

Phase 2.6 does not require:

- Business Step IDs;
- Manual Step mapping IDs;
- step-to-step mapping tables;
- a mapping registry;
- separate mapping approval;
- Execution IDs inside the definition.

## 5. Transformation Rules

### Preserve Business Intent

Operational detail may be added, but no new business rule may be invented.

### Expand, Do Not Redesign

A business action such as `Submit a Jira ticket using mandatory information` may expand into navigation, field entry and submission steps. This is operational detail, not new behaviour.

### Split Materially Different Paths

Use separate definitions for successful, invalid-data, missing-data, permission and service-failure paths when they need independent execution.

### Do Not Split Trivial Variations

Do not create separate definitions only for different navigation routes unless the route itself is required behaviour.

### Keep Execution Separate

Do not add environment result, actual result, evidence, defect, status or execution date.

## 6. Simple Review Method

The reviewer answers:

1. Does the definition reference the correct approved Business Scenario?
2. Does the complete definition verify one valid path within it?
3. Has it avoided adding unsupported behaviour?

If yes, parent-level traceability is sufficient.

## 7. Change Impact

When a Business Scenario changes:

1. search by `business_scenario_id`;
2. review all matching definitions;
3. update affected definitions;
4. resubmit changed definitions.

The project does not need to identify exact step-to-step relationships.

## 8. Complexity

| Area | Phase 2.6 Approach | Complexity |
|---|---|---|
| Parent relationship | One `business_scenario_id` | Low |
| Multiple child definitions | Allowed | Low |
| Step mapping | Not used | None |
| Mapping registry | Not used | None |
| Change impact | Search parent ID and review children | Low |
| Dashboard reporting | Aggregate by Business Scenario ID | Low |

## 9. Dashboard Use

```text
Business Scenario: MCP-JIRA-001
Manual Definitions: 3
Approved: 2
Draft: 1
Latest Manual Execution: PASS
```

Step-level mapping is not needed for coverage or readiness reporting.

## 10. Principle

Use the Business Scenario ID as the single traceability link. Add finer mapping only when a proven requirement makes parent-level traceability insufficient.