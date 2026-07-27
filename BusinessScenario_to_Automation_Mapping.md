# Business Scenario to Automation Test Definition Mapping

## Relationship

```text
One Business Scenario
        ↓
Zero, one or multiple Automation Test Definitions
        ↓
One or more Playwright tests
```

Manual and Automation Test Definitions are siblings under the same approved Business Scenario. Automation does not reference or depend on the Manual Test Definition ID.

## Mapping

| Business Scenario | Automation Test Definition |
|---|---|
| Scenario ID | `business_scenario_id` |
| Objective | Automation objective |
| Capability/module/feature | Matching metadata |
| Priority | Automation priority |
| Requirement IDs | `requirement_ids` |
| Preconditions | Automatable setup |
| Business flow | Automated actions |
| Expected outcome | Playwright assertions |
| Material variants | Separate definitions |

## Definition to Script

| Automation Definition | Playwright Script |
|---|---|
| Automation Test ID | Title, tag or annotation |
| Business Scenario ID | Tag or annotation |
| Preconditions | Fixture or setup |
| Test data | Factory, fixture or configuration |
| Automated flow | Playwright actions |
| Assertions | `expect` statements |
| Cleanup | UI or API helper |
| Script path | Repository path |

## Rules

- Preserve business intent.
- Add technical detail without inventing behaviour.
- Split materially different paths.
- Do not split by browser, environment or trivial navigation.
- Keep execution data separate.
- Use parent-level traceability only.

## Change Impact

Search Automation Test Definitions by `business_scenario_id`, update definitions first, follow `script_path` to update scripts, then re-run affected automation.
