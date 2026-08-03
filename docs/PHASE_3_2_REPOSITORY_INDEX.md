# Phase 3.2 — Repository Index

## Objective

Phase 3.2 transforms the flat asset list produced by Phase 3.1 into a
relationship-aware in-memory index.

The accepted relationship model is:

```text
One Business Scenario
    ├── zero or more Manual Test Definitions
    └── zero or more Automation Test Definitions
```

Each Test Definition references its parent Business Scenario ID.

Phase 3.2 does not introduce Business Step IDs or step-level traceability.

## Input

`dashboard_engine.discovery.DiscoveryReport`

## Output

`dashboard_engine.indexing.RepositoryIndex`

The index contains:

- Business Scenarios;
- Manual Test Definitions;
- Automation Test Definitions;
- parent Scenario relationships;
- direct lookup maps;
- relationship issues;
- ignored assets.

## Supported parent reference fields

The index accepts these metadata keys:

1. `parent_scenario_id`
2. `business_scenario_id`
3. `scenario_id`
4. `parent_id`

`parent_scenario_id` is the recommended canonical field for new files.

## Relationship rules

1. One Scenario may have zero or more Manual Test Definitions.
2. One Scenario may have zero or more Automation Test Definitions.
3. One Test Definition must reference exactly one parent Scenario.
4. A Test Definition with no parent Scenario reference is excluded and reported.
5. A Test Definition referencing an unknown Scenario is excluded and reported.
6. Duplicate Scenario or Test Definition IDs are reported.
7. A Scenario with no linked Test Definition remains valid and is indexed.

## Run

```bash
python3 scripts/build_repository_index.py
```

Write JSON output:

```bash
python3 scripts/build_repository_index.py \
  --output data/repository_index.json
```

Enable strict Phase 3.1 discovery:

```bash
python3 scripts/build_repository_index.py \
  --strict-discovery \
  --output data/repository_index.json
```

## Exit codes

- `0`: no discovery or indexing issues;
- `1`: one or more non-fatal discovery or indexing issues.

## Phase boundary

Phase 3.2 does not calculate:

- coverage;
- execution completion;
- pass rate;
- review completion;
- environment readiness;
- release readiness.

Those calculations belong to Phase 3.3 and later.
