---
manual_test_id: MCP-JIRA-M-001
business_scenario_id: MCP-JIRA-001
name: Create Jira ticket with mandatory fields
status: APPROVED
priority: HIGH
test_type: FUNCTIONAL
test_level: SYSTEM
capability: MCP
business_module: JIRA
business_feature: CREATE_TICKET
requirement_ids:
  - REQ-MCP-JIRA-001
jira_id:
owner: Functional Testing Team
---

# Manual Test Definition: Create Jira Ticket with Mandatory Fields

## Objective

Verify that an authorised user can create a Jira ticket using all mandatory fields and that Jira displays the new ticket with a unique Jira ID.

## Parent Business Scenario

| Field | Value |
|---|---|
| Business Scenario ID | MCP-JIRA-001 |
| Business Scenario Name | Create Jira ticket |
| Coverage | Successful manual path using valid mandatory data |

## Preconditions

- The target Jira environment is available.
- The tester is authenticated.
- The tester has permission to create issues in the selected project.
- The selected project supports the chosen issue type.
- No known environment issue blocks ticket creation.

## Required Test Data

| Data Item | Value or Selection Rule |
|---|---|
| Project | Select an active project accessible to the tester |
| Issue Type | Task |
| Summary | `Phase 2.6 manual test definition validation` |
| Description | `Validate successful Jira ticket creation using all mandatory fields.` |
| Priority | Medium, when required and available |

## Test Steps

| Step | Action | Expected Result |
|---:|---|---|
| 1 | Open Jira in the target test environment. | Jira is displayed. |
| 2 | Open the Create Issue dialog. | The Create Issue dialog is displayed with the applicable fields. |
| 3 | Select the target project. | The selected project is displayed and its issue configuration is loaded. |
| 4 | Select `Task` as the issue type. | `Task` is displayed as the selected issue type. |
| 5 | Enter the specified Summary. | The Summary is accepted without a validation error. |
| 6 | Enter the specified Description. | The Description is accepted without a validation error. |
| 7 | Populate any other mandatory fields using valid values. | All mandatory fields contain accepted values. |
| 8 | Submit the Create Issue form. | The form is accepted and a successful creation confirmation is displayed or the dialog closes. |
| 9 | Open the newly created ticket when it is not displayed automatically. | The new ticket is displayed. |
| 10 | Verify the created ticket details. | A unique Jira ID is displayed and the saved values match the submitted data. |

## Postconditions

- One Jira ticket exists with the supplied data.
- The ticket may be retained as evidence or removed according to the project clean-up policy.

## Notes

- Environment, build, actual result, evidence and pass/fail status belong to the Execution record.
- Missing mandatory fields, invalid data, permission failures and downstream failures require separate definitions when in scope.

## Approval Record

| Role | Name | Date | Decision |
|---|---|---|---|
| Author | Example Author | YYYY-MM-DD | Submitted |
| Reviewer | Example Reviewer | YYYY-MM-DD | Approved |
