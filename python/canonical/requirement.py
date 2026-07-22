"""
Canonical Requirement model.

Purpose
-------
Defines and validates the canonical representation of a business or
technical requirement.

Inputs
------
Normalized requirement values supplied by connector or builder modules.

Outputs
-------
An immutable Requirement object and JSON-compatible dictionary output.

Dependencies
------------
Uses the Python standard library and canonical controlled vocabularies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from urllib.parse import urlparse

from .enums import (
    Priority,
    RequirementStatus,
    RequirementType,
    SourceSystem,
)


class RequirementValidationError(ValueError):
    """Raised when canonical Requirement data is invalid."""


def _require_text(
    value: object,
    field_name: str,
    *,
    maximum_length: int,
) -> str:
    """
    Validate and normalize a mandatory text field.

    The returned value has surrounding whitespace removed.
    """

    if not isinstance(value, str):
        raise RequirementValidationError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise RequirementValidationError(
            f"{field_name} must not be empty."
        )

    if len(normalized) > maximum_length:
        raise RequirementValidationError(
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
    Validate and normalize an optional text field.

    None and whitespace-only strings are normalized to None.
    """

    if value is None:
        return None

    if not isinstance(value, str):
        raise RequirementValidationError(
            f"{field_name} must be a string or null."
        )

    normalized = value.strip()

    if not normalized:
        return None

    if len(normalized) > maximum_length:
        raise RequirementValidationError(
            f"{field_name} must not exceed "
            f"{maximum_length} characters."
        )

    return normalized


def _normalize_labels(value: object) -> tuple[str, ...]:
    """
    Normalize labels into a unique immutable tuple.

    Labels are trimmed, converted to lowercase, and deduplicated while
    preserving their first-seen order.
    """

    if value is None:
        return ()

    if isinstance(value, str):
        raise RequirementValidationError(
            "labels must be a collection of strings, not a single string."
        )

    try:
        raw_labels = list(value)
    except TypeError as exc:
        raise RequirementValidationError(
            "labels must be a collection of strings."
        ) from exc

    normalized_labels: list[str] = []
    seen_labels: set[str] = set()

    for index, raw_label in enumerate(raw_labels):
        if not isinstance(raw_label, str):
            raise RequirementValidationError(
                f"labels[{index}] must be a string."
            )

        label = raw_label.strip().lower()

        if not label:
            continue

        if len(label) > 100:
            raise RequirementValidationError(
                f"labels[{index}] must not exceed 100 characters."
            )

        if label not in seen_labels:
            seen_labels.add(label)
            normalized_labels.append(label)

    return tuple(normalized_labels)


def _validate_url(value: str | None) -> str | None:
    """Validate an optional HTTP or HTTPS source URL."""

    if value is None:
        return None

    parsed = urlparse(value)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RequirementValidationError(
            "source_url must be a valid HTTP or HTTPS URL."
        )

    return value


@dataclass(frozen=True, slots=True)
class Requirement:
    """
    Immutable canonical business or technical requirement.

    Controlled values may be supplied either as enum members or strings.
    String values are parsed case-insensitively.
    """

    requirement_id: str
    title: str
    source_system: SourceSystem | str
    requirement_type: RequirementType | str
    status: RequirementStatus | str
    priority: Priority | str

    description: str | None = None
    source_project: str | None = None
    source_url: str | None = None
    component: str | None = None
    labels: tuple[str, ...] | list[str] = field(default_factory=tuple)
    release: str | None = None
    sprint: str | None = None
    owner: str | None = None
    active: bool = True

    def __post_init__(self) -> None:
        """Normalize and validate all Requirement fields."""

        object.__setattr__(
            self,
            "requirement_id",
            _require_text(
                self.requirement_id,
                "requirement_id",
                maximum_length=100,
            ),
        )

        object.__setattr__(
            self,
            "title",
            _require_text(
                self.title,
                "title",
                maximum_length=300,
            ),
        )

        object.__setattr__(
            self,
            "source_system",
            SourceSystem.parse(self.source_system),
        )

        object.__setattr__(
            self,
            "requirement_type",
            RequirementType.parse(self.requirement_type),
        )

        object.__setattr__(
            self,
            "status",
            RequirementStatus.parse(self.status),
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
            "source_project",
            _optional_text(
                self.source_project,
                "source_project",
                maximum_length=100,
            ),
        )

        normalized_url = _optional_text(
            self.source_url,
            "source_url",
            maximum_length=2_000,
        )

        object.__setattr__(
            self,
            "source_url",
            _validate_url(normalized_url),
        )

        object.__setattr__(
            self,
            "component",
            _optional_text(
                self.component,
                "component",
                maximum_length=300,
            ),
        )

        object.__setattr__(
            self,
            "labels",
            _normalize_labels(self.labels),
        )

        object.__setattr__(
            self,
            "release",
            _optional_text(
                self.release,
                "release",
                maximum_length=200,
            ),
        )

        object.__setattr__(
            self,
            "sprint",
            _optional_text(
                self.sprint,
                "sprint",
                maximum_length=200,
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
            raise RequirementValidationError(
                "active must be a Boolean value."
            )

    def to_dict(self) -> dict[str, Any]:
        """Return the Requirement as a JSON-compatible dictionary."""

        return {
            "requirement_id": self.requirement_id,
            "source_system": self.source_system.value,
            "source_project": self.source_project,
            "source_url": self.source_url,
            "title": self.title,
            "description": self.description,
            "requirement_type": self.requirement_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "component": self.component,
            "labels": list(self.labels),
            "release": self.release,
            "sprint": self.sprint,
            "owner": self.owner,
            "active": self.active,
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> "Requirement":
        """
        Build and validate a Requirement from dictionary input.

        Unknown fields are rejected instead of being silently ignored.
        """

        if not isinstance(data, Mapping):
            raise RequirementValidationError(
                "Requirement input must be a mapping."
            )

        try:
            return cls(**dict(data))
        except TypeError as exc:
            raise RequirementValidationError(
                f"Invalid Requirement fields: {exc}"
            ) from exc
