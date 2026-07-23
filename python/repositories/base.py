
"""Reusable in-memory repository foundation.

Purpose
-------
Provides deterministic, validated CRUD operations for canonical domain
objects without coupling the dashboard engine to files, databases, Jira,
or any other external storage system.

The repository stores immutable canonical objects in memory and exposes
safe lookup and collection operations.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Generic, TypeVar


ItemType = TypeVar("ItemType")


class RepositoryError(Exception):
    """Base exception for repository operations."""


class RepositoryValidationError(RepositoryError, ValueError):
    """Raised when repository input is invalid."""


class DuplicateItemError(RepositoryError):
    """Raised when adding an item whose identifier already exists."""


class ItemNotFoundError(RepositoryError, LookupError):
    """Raised when a requested item does not exist."""


class InMemoryRepository(Generic[ItemType]):
    """Generic deterministic in-memory repository.

    Parameters
    ----------
    item_type:
        Expected Python type for every stored item.

    id_getter:
        Function that returns the unique identifier of an item.

    entity_name:
        Human-readable entity name used in error messages.
    """

    def __init__(
        self,
        *,
        item_type: type[ItemType],
        id_getter: Callable[[ItemType], str],
        entity_name: str,
    ) -> None:
        if not isinstance(item_type, type):
            raise RepositoryValidationError(
                "item_type must be a Python type."
            )

        if not callable(id_getter):
            raise RepositoryValidationError(
                "id_getter must be callable."
            )

        if not isinstance(entity_name, str):
            raise RepositoryValidationError(
                "entity_name must be a string."
            )

        normalized_entity_name = entity_name.strip()

        if not normalized_entity_name:
            raise RepositoryValidationError(
                "entity_name must not be empty."
            )

        self._item_type = item_type
        self._id_getter = id_getter
        self._entity_name = normalized_entity_name
        self._items: dict[str, ItemType] = {}

    def add(self, item: ItemType) -> None:
        """Add one item.

        Raises
        ------
        RepositoryValidationError
            If the object type or identifier is invalid.

        DuplicateItemError
            If the identifier already exists.
        """
        item_id = self._extract_item_id(item)

        if item_id in self._items:
            raise DuplicateItemError(
                f"{self._entity_name} with ID "
                f"'{item_id}' already exists."
            )

        self._items[item_id] = item

    def add_many(
        self,
        items: Iterable[ItemType],
    ) -> None:
        """Add multiple items atomically.

        All input items are validated before the repository is changed.
        If one item is invalid or duplicated, no items are added.
        """
        if isinstance(items, (str, bytes)):
            raise RepositoryValidationError(
                "items must be an iterable of repository objects."
            )

        try:
            candidates = list(items)
        except TypeError as exc:
            raise RepositoryValidationError(
                "items must be an iterable of repository objects."
            ) from exc

        validated_items: list[tuple[str, ItemType]] = []
        incoming_ids: set[str] = set()

        for item in candidates:
            item_id = self._extract_item_id(item)

            if item_id in self._items:
                raise DuplicateItemError(
                    f"{self._entity_name} with ID "
                    f"'{item_id}' already exists."
                )

            if item_id in incoming_ids:
                raise DuplicateItemError(
                    f"{self._entity_name} with ID "
                    f"'{item_id}' appears more than once "
                    "in the input collection."
                )

            incoming_ids.add(item_id)
            validated_items.append((item_id, item))

        for item_id, item in validated_items:
            self._items[item_id] = item

    def get(self, item_id: str) -> ItemType:
        """Return an item by identifier.

        Raises
        ------
        ItemNotFoundError
            If the identifier does not exist.
        """
        normalized_id = self._normalize_lookup_id(item_id)

        try:
            return self._items[normalized_id]
        except KeyError as exc:
            raise ItemNotFoundError(
                f"{self._entity_name} with ID "
                f"'{normalized_id}' was not found."
            ) from exc

    def get_or_none(
        self,
        item_id: str,
    ) -> ItemType | None:
        """Return an item or ``None`` when the identifier is absent."""
        normalized_id = self._normalize_lookup_id(item_id)
        return self._items.get(normalized_id)

    def exists(self, item_id: str) -> bool:
        """Return whether an identifier exists."""
        normalized_id = self._normalize_lookup_id(item_id)
        return normalized_id in self._items

    def list_all(self) -> tuple[ItemType, ...]:
        """Return all items sorted by identifier."""
        return tuple(
            self._items[item_id]
            for item_id in sorted(self._items)
        )

    def replace(self, item: ItemType) -> ItemType:
        """Replace an existing item and return the previous object.

        The replacement object must have the same identifier as the
        stored item being replaced.
        """
        item_id = self._extract_item_id(item)

        if item_id not in self._items:
            raise ItemNotFoundError(
                f"{self._entity_name} with ID "
                f"'{item_id}' was not found."
            )

        previous_item = self._items[item_id]
        self._items[item_id] = item
        return previous_item

    def remove(self, item_id: str) -> ItemType:
        """Remove and return an item by identifier."""
        normalized_id = self._normalize_lookup_id(item_id)

        try:
            return self._items.pop(normalized_id)
        except KeyError as exc:
            raise ItemNotFoundError(
                f"{self._entity_name} with ID "
                f"'{normalized_id}' was not found."
            ) from exc

    def clear(self) -> None:
        """Remove every item from the repository."""
        self._items.clear()

    def count(self) -> int:
        """Return the number of stored items."""
        return len(self._items)

    def _extract_item_id(
        self,
        item: ItemType,
    ) -> str:
        """Validate an item and return its normalized identifier."""
        if not isinstance(item, self._item_type):
            raise RepositoryValidationError(
                f"Expected {self._entity_name} object, "
                f"received {type(item).__name__}."
            )

        try:
            item_id = self._id_getter(item)
        except Exception as exc:
            raise RepositoryValidationError(
                f"Unable to retrieve the "
                f"{self._entity_name} identifier."
            ) from exc

        if not isinstance(item_id, str):
            raise RepositoryValidationError(
                f"{self._entity_name} identifier "
                "must be a string."
            )

        normalized_id = item_id.strip()

        if not normalized_id:
            raise RepositoryValidationError(
                f"{self._entity_name} identifier "
                "must not be empty."
            )

        return normalized_id

    @staticmethod
    def _normalize_lookup_id(item_id: str) -> str:
        """Validate and trim an identifier supplied to a lookup."""
        if not isinstance(item_id, str):
            raise RepositoryValidationError(
                "Repository identifier must be a string."
            )

        normalized_id = item_id.strip()

        if not normalized_id:
            raise RepositoryValidationError(
                "Repository identifier must not be empty."
            )

        return normalized_id
