
"""Unit tests for the generic in-memory repository."""

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIRECTORY = REPOSITORY_ROOT / "python"

if str(PYTHON_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIRECTORY))

from repositories.base import (  # noqa: E402
    DuplicateItemError,
    InMemoryRepository,
    ItemNotFoundError,
    RepositoryValidationError,
)


@dataclass(frozen=True)
class ExampleItem:
    """Simple immutable object used by repository tests."""

    item_id: str
    name: str


class ExampleItemRepository(
    InMemoryRepository[ExampleItem]
):
    """Concrete repository used only for unit testing."""

    def __init__(self) -> None:
        super().__init__(
            item_type=ExampleItem,
            id_getter=lambda item: item.item_id,
            entity_name="Example Item",
        )


def example_item(
    item_id: str = "ITEM-001",
    name: str = "Example",
) -> ExampleItem:
    """Return a valid example item."""
    return ExampleItem(
        item_id=item_id,
        name=name,
    )


class RepositoryConstructionTests(unittest.TestCase):
    """Tests covering repository configuration."""

    def test_create_valid_repository(self) -> None:
        repository = ExampleItemRepository()

        self.assertEqual(repository.count(), 0)
        self.assertEqual(repository.list_all(), ())

    def test_item_type_must_be_type(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            InMemoryRepository(
                item_type="ExampleItem",  # type: ignore[arg-type]
                id_getter=lambda item: item.item_id,
                entity_name="Example Item",
            )

    def test_id_getter_must_be_callable(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            InMemoryRepository(
                item_type=ExampleItem,
                id_getter="item_id",  # type: ignore[arg-type]
                entity_name="Example Item",
            )

    def test_entity_name_must_not_be_blank(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            InMemoryRepository(
                item_type=ExampleItem,
                id_getter=lambda item: item.item_id,
                entity_name=" ",
            )


class RepositoryAddTests(unittest.TestCase):
    """Tests covering add operations."""

    def setUp(self) -> None:
        self.repository = ExampleItemRepository()

    def test_add_item(self) -> None:
        item = example_item()

        self.repository.add(item)

        self.assertEqual(self.repository.count(), 1)
        self.assertEqual(
            self.repository.get("ITEM-001"),
            item,
        )

    def test_add_rejects_incorrect_object_type(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add(  # type: ignore[arg-type]
                {"item_id": "ITEM-001"}
            )

    def test_add_rejects_duplicate_identifier(self) -> None:
        self.repository.add(example_item())

        with self.assertRaises(DuplicateItemError):
            self.repository.add(
                example_item(name="Replacement")
            )

        self.assertEqual(self.repository.count(), 1)

    def test_add_many_adds_all_items(self) -> None:
        items = [
            example_item("ITEM-001", "First"),
            example_item("ITEM-002", "Second"),
            example_item("ITEM-003", "Third"),
        ]

        self.repository.add_many(items)

        self.assertEqual(self.repository.count(), 3)

    def test_add_many_is_atomic_when_existing_id_conflicts(self) -> None:
        self.repository.add(
            example_item("ITEM-001", "Existing")
        )

        with self.assertRaises(DuplicateItemError):
            self.repository.add_many(
                [
                    example_item("ITEM-002", "New"),
                    example_item("ITEM-001", "Conflict"),
                ]
            )

        self.assertEqual(self.repository.count(), 1)
        self.assertFalse(
            self.repository.exists("ITEM-002")
        )

    def test_add_many_is_atomic_for_duplicate_input_ids(self) -> None:
        with self.assertRaises(DuplicateItemError):
            self.repository.add_many(
                [
                    example_item("ITEM-001", "First"),
                    example_item("ITEM-001", "Duplicate"),
                ]
            )

        self.assertEqual(self.repository.count(), 0)

    def test_add_many_rejects_incorrect_object_type(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add_many(
                [
                    example_item("ITEM-001"),
                    "invalid",  # type: ignore[list-item]
                ]
            )

        self.assertEqual(self.repository.count(), 0)

    def test_add_many_accepts_empty_collection(self) -> None:
        self.repository.add_many([])

        self.assertEqual(self.repository.count(), 0)

    def test_add_many_rejects_single_string(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.add_many(  # type: ignore[arg-type]
                "ITEM-001"
            )


class RepositoryLookupTests(unittest.TestCase):
    """Tests covering lookup behaviour."""

    def setUp(self) -> None:
        self.repository = ExampleItemRepository()
        self.item = example_item()
        self.repository.add(self.item)

    def test_get_existing_item(self) -> None:
        self.assertEqual(
            self.repository.get("ITEM-001"),
            self.item,
        )

    def test_get_trims_identifier(self) -> None:
        self.assertEqual(
            self.repository.get("  ITEM-001  "),
            self.item,
        )

    def test_get_is_case_sensitive(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.get("item-001")

    def test_get_missing_item_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.get("ITEM-999")

    def test_get_or_none_existing_item(self) -> None:
        self.assertEqual(
            self.repository.get_or_none("ITEM-001"),
            self.item,
        )

    def test_get_or_none_missing_item(self) -> None:
        self.assertIsNone(
            self.repository.get_or_none("ITEM-999")
        )

    def test_exists_returns_true_for_existing_id(self) -> None:
        self.assertTrue(
            self.repository.exists("ITEM-001")
        )

    def test_exists_returns_false_for_missing_id(self) -> None:
        self.assertFalse(
            self.repository.exists("ITEM-999")
        )

    def test_lookup_rejects_non_string_identifier(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.get(123)  # type: ignore[arg-type]

    def test_lookup_rejects_blank_identifier(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.get(" ")


class RepositoryListingTests(unittest.TestCase):
    """Tests covering deterministic collection output."""

    def test_list_all_is_sorted_by_identifier(self) -> None:
        repository = ExampleItemRepository()

        repository.add_many(
            [
                example_item("ITEM-003", "Third"),
                example_item("ITEM-001", "First"),
                example_item("ITEM-002", "Second"),
            ]
        )

        result = repository.list_all()

        self.assertEqual(
            tuple(item.item_id for item in result),
            (
                "ITEM-001",
                "ITEM-002",
                "ITEM-003",
            ),
        )

    def test_list_all_returns_tuple(self) -> None:
        repository = ExampleItemRepository()
        repository.add(example_item())

        self.assertIsInstance(
            repository.list_all(),
            tuple,
        )


class RepositoryReplaceTests(unittest.TestCase):
    """Tests covering replacement behaviour."""

    def setUp(self) -> None:
        self.repository = ExampleItemRepository()
        self.original = example_item(
            "ITEM-001",
            "Original",
        )
        self.repository.add(self.original)

    def test_replace_existing_item(self) -> None:
        replacement = example_item(
            "ITEM-001",
            "Updated",
        )

        previous = self.repository.replace(replacement)

        self.assertEqual(previous, self.original)
        self.assertEqual(
            self.repository.get("ITEM-001"),
            replacement,
        )
        self.assertEqual(self.repository.count(), 1)

    def test_replace_missing_item_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.replace(
                example_item("ITEM-999")
            )

    def test_replace_rejects_incorrect_object_type(self) -> None:
        with self.assertRaises(RepositoryValidationError):
            self.repository.replace(  # type: ignore[arg-type]
                {"item_id": "ITEM-001"}
            )


class RepositoryRemoveAndClearTests(unittest.TestCase):
    """Tests covering removal and clearing."""

    def setUp(self) -> None:
        self.repository = ExampleItemRepository()
        self.item = example_item()
        self.repository.add(self.item)

    def test_remove_existing_item(self) -> None:
        removed = self.repository.remove("ITEM-001")

        self.assertEqual(removed, self.item)
        self.assertEqual(self.repository.count(), 0)

    def test_remove_trims_identifier(self) -> None:
        removed = self.repository.remove(
            " ITEM-001 "
        )

        self.assertEqual(removed, self.item)

    def test_remove_missing_item_raises_error(self) -> None:
        with self.assertRaises(ItemNotFoundError):
            self.repository.remove("ITEM-999")

    def test_clear_removes_all_items(self) -> None:
        self.repository.add(
            example_item("ITEM-002")
        )

        self.repository.clear()

        self.assertEqual(self.repository.count(), 0)
        self.assertEqual(self.repository.list_all(), ())


if __name__ == "__main__":
    unittest.main()
