# Functional Testing Dashboard — Test Case Data Dictionary

Version: 1.0

## Test-case metadata

| Field | Type | Required | Allowed / Format | Owner | Description |
|---|---|:---:|---|---|---|
| `scenario_id` | String | Yes | `^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3,}$` | Author | Permanent canonical test-case identifier |
| `scenario_name` | String | Yes | 5–160 characters | Author | Clear business behaviour being verified |
| `business_feature` | String | Yes | Non-empty | Author | Functional capability used for grouping |
| `business_module` | String | Yes | Non-empty | Author | Application, product area, or domain |
| `priority` | Enum | Yes | Critical, High, Medium, Low | Author/Reviewer | Delivery and business importance |
| `test_type` | Enum | Yes | Functional, Smoke, Sanity, Regression, Integration, End-to-End, API, UI | Author/Reviewer | Primary test classification |
| `category` | String | Yes | Non-empty | Author/Reviewer | Reporting category |
| `manual_exists` | Boolean | Yes | `true` / `false` | Author | Manual implementation exists or is intended |
| `automation_exists` | Boolean | Yes | `true` / `false` | Author | Automated implementation exists or is intended |
| `review_status` | Enum | Yes | Pending, Approved, Published, Rejected | Workflow | Governance lifecycle state |
| `jira_id` | String/null | Conditional | Jira issue key pattern | Publisher | Jira ticket returned after publication |
| `scenario_pattern` | String/null | No | Reserved | Future enhancement | Optional behaviour-pattern classification |
| `owner` | String/null | No | Team or person | Author/Reviewer | Functional ownership |
| `created_by` | String/null | No | GitHub identity or name | Author | Original contributor |
| `created_date` | Date/null | Recommended | `YYYY-MM-DD` | Author | Initial creation date |
| `reviewed_by` | String/null | Conditional | Reviewer identity | Reviewer | Required when Approved or Published |
| `reviewed_date` | Date/null | Conditional | `YYYY-MM-DD` | Reviewer | Required when Approved or Published |
| `published_date` | Date/null | Conditional | `YYYY-MM-DD` | Publisher | Required when Published |

## Markdown body sections

| Section | Required | Description |
|---|:---:|---|
| `Business Objective` | Yes | Business purpose and behaviour under test |
| `Preconditions` | Yes | Required access, data, dependency, and state |
| `Test Data` | No | Input values, data rules, or references |
| `Test Steps` | Yes | Ordered action and expected-outcome table |
| `Overall Expected Result` | Yes | Final observable acceptance outcome |
| `Automation Notes` | Conditional | Recommended when automation exists |
| `Remarks` | No | Additional information not represented elsewhere |

## Generated registry fields

| Field | Source | Description |
|---|---|---|
| `source_file` | Repository path | Location of the Markdown definition |
| `workflow_folder` | Folder name | pending_review, reviewed, published, or rejected |
| `validation_status` | Registry builder | Valid or Invalid |
| `validation_errors` | Validator | List of detected data-quality issues |
| `jira_url` | Configuration + Jira ID | Browser link to the published Jira ticket |
| `manual_coverage` | Derived | Same value as `manual_exists`, exposed for dashboard reporting |
| `automation_coverage` | Derived | Same value as `automation_exists`, exposed for dashboard reporting |

## Execution fields excluded from this phase

The following belong to the canonical Execution model and must not be added to test definitions:

- Environment
- Build version
- Execution date/time
- Tester or pipeline runner
- Pass, Fail, Blocked, Skipped, or Not Executed result
- Defect ID created during execution
- Execution evidence
- Execution duration
