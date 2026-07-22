
"""
Canonical Scenario model.

Purpose
-------
Defines and validates one independently verifiable business behaviour.

Inputs
------
Normalized Scenario values supplied by builder or connector modules.

Outputs
-------
An immutable Scenario object and JSON-compatible dictionary output.

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
    """
    Validate and normalize a mandatory text value.

    Surrounding whitespace is removed before the value is returned.
    """

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
    """
    Validate and normalize an optional text value.

    None and whitespace-only strings are normalized to None.
    """

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


def _normalize_identifiers(
    value: object,
    field_name: str,
    *,
    minimum_count: int = 0,
    maximum_item_length: int = 100,
) -> tuple[str, ...]:
    """
    Normalize an identifier collection into a unique immutable tuple.

    Values are trimmed and deduplicated while preserving their
    first-seen order.
    """

    if value is None:
        raw_values: list[object] = []
    else:
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
            raise ScenarioValidationError(
                f"{field_name}[{index}] must not be empty."
            )

        if len(normalized) > maximum_item_length:
            raise ScenarioValidationError(
                f"{field_name}[{index}] must not exceed "
                f"{maximum_item_length} characters."
            )

        if normalized not in seen_values:
            seen_values.add(normalized)
            normalized_values.append(normalized)

    if len(normalized_values) < minimum_count:
        raise ScenarioValidationError(
            f"{field_name} must contain at least "
            f"{minimum_count} value(s)."
        )

    return tuple(normalized_values)


def _normalize_tags(value: object) -> tuple[str, ...]:
    """
    Normalize tags into a unique lowercase immutable tuple.

    Blank tags are ignored.
    """

    if value is None:
        return ()

    if isinstance(value, str):
        raise ScenarioValidationError(
            "tags must be a collection of strings, "
            "not a single string."
        )

    try:
        raw_tags = list(value)
    except TypeError as exc:
        raise ScenarioValidationError(
            "tags must be a collection of strings."
        ) from exc

    normalized_tags: list[str] = []
    seen_tags: set[str] = set()

    for index, raw_tag in enumerate(raw_tags):
        if not isinstance(raw_tag, str):
            raise ScenarioValidationError(
                f"tags[{index}] must be a string."
            )

        tag = raw_tag.strip().lower()

        if not tag:
            continue

        if len(tag) > 100:
            raise ScenarioValidationError(
                f"tags[{index}] must not exceed 100 characters."
            )

        if tag not in seen_tags:
            seen_tags.add(tag)
            normalized_tags.append(tag)

    return tuple(normalized_tags)


def _normalize_preconditions(value: object) -> tuple[str, ...]:
    """
    Normalize preconditions into a unique immutable tuple.

    Preconditions retain capitalization because they are human-readable.
    Blank values are ignored.
    """

    if value is None:
        return ()

    if isinstance(value, str):
        raise ScenarioValidationError(
            "preconditions must be a collection of strings, "
            "not a single string."
        )

    try:
        raw_preconditions = list(value)
    except TypeError as exc:
        raise ScenarioValidationError(
            "preconditions must be a collection of strings."
        ) from exc

    normalized_preconditions: list[str] = []
    seen_preconditions: set[str] = set()

    for index, raw_precondition in enumerate(raw_preconditions):
        if not isinstance(raw_precondition, str):
            raise ScenarioValidationError(
                f"preconditions[{index}] must be a string."
            )

        precondition = raw_precondition.strip()

        if not precondition:
            continue

        if len(precondition) > 1_000:
            raise ScenarioValidationError(
                f"preconditions[{index}] must not exceed "
                "1000 characters."
            )

        if precondition not in seen_preconditions:
            seen_preconditions.add(precondition)
            normalized_preconditions.append(precondition)

    return tuple(normalized_preconditions)


@dataclass(frozen=True, slots=True)
class Scenario:
    """
    Immutable canonical business-behaviour Scenario.

    Controlled fields may be supplied as canonical enum members or
    case-insensitive strings.
    """

    scenario_id: str
    feature_id: str
    requirement_ids: tuple[str, ...] | list[str]
    name: str
    scenario_type: ScenarioType | str
    priority: Priority | str

    description: str | None = None
    tags: tuple[str, ...] | list[str] = field(default_factory=tuple)
    preconditions: tuple[str, ...] | list[str] = field(
        default_factory=tuple
    )
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
                maximum_length=150,
            ),
        )

        object.__setattr__(
            self,
            "requirement_ids",
            _normalize_identifiers(
                self.requirement_ids,
                "requirement_ids",
                minimum_count=1,
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
            _normalize_tags(self.tags),
        )

        object.__setattr__(
            self,
            "preconditions",
            _normalize_preconditions(self.preconditions),
        )

        object.__setattr__(
            self,
            "expected_outcome",
            _optional_text(
                self.expected_outcome,
                "expected_outcome",
                maximum_length=5_000,
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
            "description": self.description,
            "scenario_type": self.scenario_type.value,
            "priority": self.priority.value,
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

        Unknown fields are rejected rather than silently ignored.
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
