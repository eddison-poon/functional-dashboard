"""
Canonical Scenario model.

Purpose
-------
Defines and validates a canonical business Scenario linked to one
Feature and one or more Requirements.

Inputs
------
Normalized Scenario values supplied by connector or builder modules.

Outputs
-------
An immutable Scenario object with JSON-compatible dictionary output.

Dependencies
------------
Uses the Python standard library and canonical controlled vocabularies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .enums import Priority, ScenarioType


class ScenarioValidationError(ValueError):
    """Raised when canonical Scenario data is invalid."""


def _require_text(
    value: object,
    field_name: str,
    *,
    maximum_length: int,
) -> str:
    """Validate and normalize mandatory text."""

    if not isinstance(value, str):
        raise ScenarioValidationError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ScenarioValidationError(
            f"{field_name} must not be empty."
        )

    if len(normalized) > maximum_length:
        raise ScenarioValidationError(
            f"{field_name} must not exceed "
            f"{maximum_length} characters."
        )

    return normalized


def _optional_text(
    value: object,
    field_name: str,
    *,
    maximum_length: int,
) -> str | None:
    """Validate and normalize optional text."""

    if value is None:
        return None

    if not isinstance(value, str):
        raise ScenarioValidationError(
            f"{field_name} must be a string or null."
        )

    normalized = value.strip()

    if not normalized:
        return None

    if len(normalized) > maximum_length:
        raise ScenarioValidationError(
            f"{field_name} must not exceed "
            f"{maximum_length} characters."
        )

    return normalized


def _normalize_text_collection(
    value: object,
    field_name: str,
    *,
    required: bool,
    lowercase: bool,
    maximum_item_length: int,
) -> tuple[str, ...]:
    """
    Normalize a collection of strings.

    Blank optional values are ignored. Values are deduplicated while
    preserving their first-seen order.
    """

    if value is None:
        if required:
            raise ScenarioValidationError(
                f"{field_name} must be a non-empty collection of strings."
            )
        return ()

    if isinstance(value, str):
        raise ScenarioValidationError(
            f"{field_name} must be a collection of strings, "
            "not a single string."
        )

    try:
        raw_values = list(value)
    except TypeError as exc:
        raise ScenarioValidationError(
            f"{field_name} must be a collection of strings."
        ) from exc

    normalized_values: list[str] = []
    seen_values: set[str] = set()

    for index, raw_value in enumerate(raw_values):
        if not isinstance(raw_value, str):
            raise ScenarioValidationError(
                f"{field_name}[{index}] must be a string."
            )

        normalized = raw_value.strip()

        if not normalized:
            if required:
                raise ScenarioValidationError(
                    f"{field_name}[{index}] must not be empty."
                )
            continue

        if lowercase:
            normalized = normalized.lower()

        if len(normalized) > maximum_item_length:
            raise ScenarioValidationError(
                f"{field_name}[{index}] must not exceed "
                f"{maximum_item_length} characters."
            )

        if normalized not in seen_values:
            seen_values.add(normalized)
            normalized_values.append(normalized)

    if required and not normalized_values:
        raise ScenarioValidationError(
            f"{field_name} must contain at least one value."
        )

    return tuple(normalized_values)


@dataclass(frozen=True, slots=True)
class Scenario:
    """
    Immutable canonical business Scenario.

    Controlled values may be supplied as enum members or strings.
    String values are parsed case-insensitively.
    """

    scenario_id: str
    feature_id: str
    requirement_ids: tuple[str, ...] | list[str]
    name: str
    scenario_type: ScenarioType | str
    priority: Priority | str

    description: str | None = None
    tags: tuple[str, ...] | list[str] = field(default_factory=tuple)
    preconditions: tuple[str, ...] | list[str] = field(default_factory=tuple)
    expected_outcome: str | None = None
    owner: str | None = None
    active: bool = True

    def __post_init__(self) -> None:
        """Normalize and validate all Scenario fields."""

        object.__setattr__(
            self,
            "scenario_id",
            _require_text(
                self.scenario_id,
                "scenario_id",
                maximum_length=100,
            ),
        )

        object.__setattr__(
            self,
            "feature_id",
            _require_text(
                self.feature_id,
                "feature_id",
                maximum_length=200,
            ),
        )

        object.__setattr__(
            self,
            "requirement_ids",
            _normalize_text_collection(
                self.requirement_ids,
                "requirement_ids",
                required=True,
                lowercase=False,
                maximum_item_length=100,
            ),
        )

        object.__setattr__(
            self,
            "name",
            _require_text(
                self.name,
                "name",
                maximum_length=300,
            ),
        )

        object.__setattr__(
            self,
            "scenario_type",
            ScenarioType.parse(self.scenario_type),
        )

        object.__setattr__(
            self,
            "priority",
            Priority.parse(self.priority),
        )

        object.__setattr__(
            self,
            "description",
            _optional_text(
                self.description,
                "description",
                maximum_length=20_000,
            ),
        )

        object.__setattr__(
            self,
            "tags",
            _normalize_text_collection(
                self.tags,
                "tags",
                required=False,
                lowercase=True,
                maximum_item_length=100,
            ),
        )

        object.__setattr__(
            self,
            "preconditions",
            _normalize_text_collection(
                self.preconditions,
                "preconditions",
                required=False,
                lowercase=False,
                maximum_item_length=5_000,
            ),
        )

        object.__setattr__(
            self,
            "expected_outcome",
            _optional_text(
                self.expected_outcome,
                "expected_outcome",
                maximum_length=20_000,
            ),
        )

        object.__setattr__(
            self,
            "owner",
            _optional_text(
                self.owner,
                "owner",
                maximum_length=300,
            ),
        )

        if type(self.active) is not bool:
            raise ScenarioValidationError(
                "active must be a Boolean value."
            )

    def to_dict(self) -> dict[str, Any]:
        """Return the Scenario as a JSON-compatible dictionary."""

        return {
            "scenario_id": self.scenario_id,
            "feature_id": self.feature_id,
            "requirement_ids": list(self.requirement_ids),
            "name": self.name,
            "scenario_type": self.scenario_type.value,
            "priority": self.priority.value,
            "description": self.description,
            "tags": list(self.tags),
            "preconditions": list(self.preconditions),
            "expected_outcome": self.expected_outcome,
            "owner": self.owner,
            "active": self.active,
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> "Scenario":
        """
        Build and validate a Scenario from dictionary input.

        Unknown or missing required fields are converted into a
        ScenarioValidationError rather than being silently ignored.
        """

        if not isinstance(data, Mapping):
            raise ScenarioValidationError(
                "Scenario input must be a mapping."
            )

        try:
            return cls(**dict(data))
        except TypeError as exc:
            raise ScenarioValidationError(
                f"Invalid Scenario fields: {exc}"
            ) from exc
