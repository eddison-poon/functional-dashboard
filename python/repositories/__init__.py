"""Repository layer for canonical dashboard entities."""

from .base import (
    DuplicateItemError,
    InMemoryRepository,
    ItemNotFoundError,
    RepositoryError,
    RepositoryValidationError,
)

__all__ = [
    "DuplicateItemError",
    "InMemoryRepository",
    "ItemNotFoundError",
    "RepositoryError",
    "RepositoryValidationError",
]
