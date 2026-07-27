# Playwright Implementation Guide

## Recommended Structure

```text
automation/playwright/
├── package.json
├── playwright.config.ts
├── tests/
│   └── <capability>/<module>/
├── pages/
├── fixtures/
├── helpers/
└── test-data/
```

Create support directories only when they provide real reuse.

## Basic Pattern

```typescript
import { test, expect } from '@playwright/test';

test(
  'MCP-JIRA-A-001 create Jira ticket with mandatory fields',
  { tag: ['@MCP-JIRA-A-001', '@MCP-JIRA-001', '@regression'] },
  async ({ page }) => {
    const summary = `MCP-JIRA-A-001-${Date.now()}`;
    await page.goto('/');
    await page.getByRole('button', { name: /create/i }).click();
    await page.getByLabel(/summary/i).fill(summary);
    await page.getByRole('button', { name: /^create$/i }).click();
    await expect(page.getByText(summary)).toBeVisible();
  },
);
```

## Configuration

Use environment variables for base URL, credentials, project keys and other environment-specific values. Configure HTML and JSON reporting plus trace, screenshot and video retention on failure.

Recommended `.gitignore`:

```text
.env
.env.*
playwright-report/
test-results/
blob-report/
playwright/.auth/
```

## Authentication

Prefer secure storage state or an approved login fixture. Never commit authentication state.

## Locators

Prefer role, label and test ID locators. Avoid generated classes, deep XPath and positional selectors.

## Waiting

Wait for observable state, relevant responses or assertions. Avoid fixed sleeps.

## Test Steps

Use `test.step` for meaningful business phases, not every click.

## Assertions

Assert business outcomes such as created identifiers, submitted values and rejection messages.

## Test Data

Generate unique values and use small factories only when useful.

## Page Objects

Use page objects when multiple tests share meaningful workflows. Do not wrap every locator call unnecessarily.

## API Assistance

Use Playwright API requests for setup, cleanup or backend verification when approved. The primary tested behaviour must remain aligned with the Automation Test Definition.

## Definition of Done

The definition is approved, the script follows it, traceability is present, secrets are externalised, selectors are stable, assertions prove the objective, the test runs independently, code review passes and one controlled execution succeeds.
