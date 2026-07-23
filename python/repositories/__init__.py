"""Repository layer for canonical dashboard entities."""

from .base import (
    DuplicateItemError,
    InMemoryRepository,
    ItemNotFoundError,
    RepositoryError,
    RepositoryValidationError,
)
from .execution_repository import ExecutionRepository
from .requirement_repository import RequirementRepository
from .scenario_repository import ScenarioRepository
from .test_definition_repository import TestDefinitionRepository
from .validation import (
    RepositoryRelationshipValidator,
    ValidationCode,
    ValidationFinding,
    ValidationReport,
    ValidationSeverity,
)

__all__ = [
    "DuplicateItemError",
    "ExecutionRepository",
    "InMemoryRepository",
    "ItemNotFoundError",
    "RepositoryError",
    "RepositoryRelationshipValidator",
    "RepositoryValidationError",
    "RequirementRepository",
    "ScenarioRepository",
    "TestDefinitionRepository",
    "ValidationCode",
    "ValidationFinding",
    "ValidationReport",
    "ValidationSeverity",
]
