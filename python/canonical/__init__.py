"""
Canonical data model package.

This package contains the governed entities and controlled vocabularies
used by the Functional Testing Dashboard data engine.
"""

from .enums import (
    AutomationFramework,
    Environment,
    EvidenceType,
    ExecutionStatus,
    InvalidEnumValueError,
    Priority,
    RequirementStatus,
    RequirementType,
    ScenarioType,
    Severity,
    SourceSystem,
    TestDefinitionStatus,
    TestType,
)


from .execution import (
    Execution,
    ExecutionValidationError,
)


from .requirement import (
    Requirement,
    RequirementValidationError,
)


from .scenario import {
    Scenario,
    ScenarioValidationError,
}


from .test_definition import (
    TestDefinition,
    TestDefinitionValidationError,
    TestStep,
)


__all__ = [
    "AutomationFramework",
    "Environment",
    "EvidenceType",
    "Execution",
    "ExecutionStatus",
    "ExecutionValidationError",
    "InvalidEnumValueError",
    "Priority",
    "Requirement",
    "RequirementStatus",
    "RequirementType",
    "RequirementValidationError",
    "Scenario",
    "ScenarioType",
    "ScenarioValidationError",
    "Severity",
    "SourceSystem",
    "TestDefinition",
    "TestDefinitionStatus",
    "TestDefinitionValidationError",
    "TestStep",
    "TestType",
]
