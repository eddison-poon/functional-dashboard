# Phase 2.7 — Automation Test Definition Package

This package provides repository-ready governance material for Playwright-based Automation Test Definitions and scripts.

## Traceability Model

```text
Approved Business Scenario
        ├── Manual Test Definition
        └── Automation Test Definition
                 ↓
          Playwright Script
                 ↓
             Execution
```

Phase 2.7 uses parent-level traceability:

```text
Business Scenario ID → Automation Test Definition → Playwright script
```

Automation Test Definitions do not depend on Manual Test Definitions. Both are sibling artefacts derived from the same approved Business Scenario.
