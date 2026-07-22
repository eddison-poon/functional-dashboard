
"""Canonical Execution model.

Purpose
-------
Defines an individual planned or completed execution of a canonical
Manual or Automation Test Definition.

Inputs
------
Normalized execution values supplied by builders, connectors, CI/CD
pipelines, test-management tools, or manual entry.

Outputs
-------
An immutable Execution object with validated fields and JSON-compatible
dictionary output.

Dependencies
------------
Uses the Python standard library and canonical controlled vocabularies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping

from .enums import (
    Environment,
    ExecutionStatus,
    SourceSystem,
)


class ExecutionValidationError(ValueError):
    """Raised when canonical Execution data is invalid."""


def _require_text(
    value: object,
    field_name: str,
    *,
    maximum_length: int,
) -> str:
    """Validate and normalize mandatory text."""
    if not isinstance(value, str):
        raise ExecutionValidationError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ExecutionValidationError(
            f"{field_name} must not be empty."
        )

    if len(normalized) > maximum_length:
        raise ExecutionValidationError(
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
        raise ExecutionValidationError(
            f"{field_name} must be a string or null."
        )

    normalized = value.strip()

    if not normalized:
        return None

    if len(normalized) > maximum_length:
        raise ExecutionValidationError(
            f"{field_name} must not exceed "
            f"{maximum_length} characters."
        )

    return normalized


def _normalize_identifier_collection(
    value: object,
    field_name: str,
    *,
    maximum_item_length: int,
) -> tuple[str, ...]:
    """Normalize and deduplicate a collection of identifiers.

    Blank identifiers are ignored. Duplicate values are removed while
    preserving the order in which they first appeared.
    """
    if value is None:
        return ()

    if isinstance(value, (str, bytes)):
        raise ExecutionValidationError(
            f"{field_name} must be a collection of strings, "
            "not a single string."
        )

    try:
        raw_values = list(value)
    except TypeError as exc:
        raise ExecutionValidationError(
            f"{field_name} must be a collection of strings."
        ) from exc

    normalized_values: list[str] = []
    seen_values: set[str] = set()

    for index, raw_value in enumerate(raw_values):
        if not isinstance(raw_value, str):
            raise ExecutionValidationError(
                f"{field_name}[{index}] must be a string."
            )

        normalized = raw_value.strip()

        if not normalized:
            continue

        if len(normalized) > maximum_item_length:
            raise ExecutionValidationError(
                f"{field_name}[{index}] must not exceed "
                f"{maximum_item_length} characters."
            )

        if normalized not in seen_values:
            seen_values.add(normalized)
            normalized_values.append(normalized)

    return tuple(normalized_values)


def _validate_datetime(
    value: object,
    field_name: str,
) -> datetime | None:
    """Validate an optional timezone-aware datetime."""
    if value is None:
        return None

    if not isinstance(value, datetime):
        raise ExecutionValidationError(
            f"{field_name} must be a datetime or null."
        )

    if value.tzinfo is None or value.utcoffset() is None:
        raise ExecutionValidationError(
            f"{field_name} must be timezone-aware."
        )

    return value


def _parse_datetime(
    value: object,
    field_name: str,
) -> datetime | None:
    """Parse an optional ISO-8601 datetime from dictionary input."""
    if value is None or isinstance(value, datetime):
        return _validate_datetime(value, field_name)

    if not isinstance(value, str):
        raise ExecutionValidationError(
            f"{field_name} must be an ISO-8601 string, "
            "datetime, or null."
        )

    normalized = value.strip()

    if not normalized:
        return None

    try:
        parsed_value = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ExecutionValidationError(
            f"{field_name} must use a valid ISO-8601 format."
        ) from exc

    return _validate_datetime(parsed_value, field_name)


@dataclass(frozen=True, slots=True)
class Execution:
    """One immutable canonical test execution instance."""

    execution_id: str
    test_definition_id: str
    environment: Environment | str
    status: ExecutionStatus | str

    execution_cycle: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    executed_by: str | None = None
    build_version: str | None = None
    source_system: SourceSystem | str = SourceSystem.MANUAL_ENTRY
    external_reference: str | None = None
    defect_ids: tuple[str, ...] | list[str] = field(
        default_factory=tuple
    )
    evidence_ids: tuple[str, ...] | list[str] = field(
        default_factory=tuple
    )
    remarks: str | None = None
    rerun_of_execution_id: str | None = None

    def __post_init__(self) -> None:
        """Normalize and validate the Execution."""
        object.__setattr__(
            self,
            "execution_id",
            _require_text(
                self.execution_id,
                "execution_id",
                maximum_length=150,
            ),
        )

        object.__setattr__(
            self,
            "test_definition_id",
            _require_text(
                self.test_definition_id,
                "test_definition_id",
                maximum_length=150,
            ),
        )

        object.__setattr__(
            self,
            "environment",
            Environment.parse(self.environment),
        )

        object.__setattr__(
            self,
            "status",
            ExecutionStatus.parse(self.status),
        )

        object.__setattr__(
            self,
            "execution_cycle",
            _optional_text(
                self.execution_cycle,
                "execution_cycle",
                maximum_length=200,
            ),
        )

        object.__setattr__(
            self,
            "started_at",
            _validate_datetime(
                self.started_at,
                "started_at",
            ),
        )

        object.__setattr__(
            self,
            "completed_at",
            _validate_datetime(
                self.completed_at,
                "completed_at",
            ),
        )

        object.__setattr__(
            self,
            "executed_by",
            _optional_text(
                self.executed_by,
                "executed_by",
                maximum_length=300,
            ),
        )

        object.__setattr__(
            self,
            "build_version",
            _optional_text(
                self.build_version,
                "build_version",
                maximum_length=100,
            ),
        )

        object.__setattr__(
            self,
            "source_system",
            SourceSystem.parse(self.source_system),
        )

        object.__setattr__(
            self,
            "external_reference",
            _optional_text(
                self.external_reference,
                "external_reference",
                maximum_length=300,
            ),
        )

        object.__setattr__(
            self,
            "defect_ids",
            _normalize_identifier_collection(
                self.defect_ids,
                "defect_ids",
                maximum_item_length=150,
            ),
        )

        object.__setattr__(
            self,
            "evidence_ids",
            _normalize_identifier_collection(
                self.evidence_ids,
                "evidence_ids",
                maximum_item_length=300,
            ),
        )

        object.__setattr__(
            self,
            "remarks",
            _optional_text(
                self.remarks,
                "remarks",
                maximum_length=20_000,
            ),
        )

        object.__setattr__(
            self,
            "rerun_of_execution_id",
            _optional_text(
                self.rerun_of_execution_id,
                "rerun_of_execution_id",
                maximum_length=150,
            ),
        )

        self._validate_execution_rules()

    def _validate_execution_rules(self) -> None:
        """Validate status, timestamp, and rerun relationships."""
        if (
            self.rerun_of_execution_id is not None
            and self.rerun_of_execution_id == self.execution_id
        ):
            raise ExecutionValidationError(
                "rerun_of_execution_id must not reference "
                "the current execution_id."
            )

        if (
            self.started_at is not None
            and self.completed_at is not None
            and self.completed_at < self.started_at
        ):
            raise ExecutionValidationError(
                "completed_at must not be earlier than started_at."
            )

        if self.status is ExecutionStatus.NOT_EXECUTED:
            if self.started_at is not None:
                raise ExecutionValidationError(
                    "A NOT_EXECUTED Execution must not define started_at."
                )

            if self.completed_at is not None:
                raise ExecutionValidationError(
                    "A NOT_EXECUTED Execution must not define completed_at."
                )

        if self.status is ExecutionStatus.IN_PROGRESS:
            if self.started_at is None:
                raise ExecutionValidationError(
                    "An IN_PROGRESS Execution requires started_at."
                )

            if self.completed_at is not None:
                raise ExecutionValidationError(
                    "An IN_PROGRESS Execution must not define completed_at."
                )

        terminal_statuses = {
            ExecutionStatus.PASSED,
            ExecutionStatus.FAILED,
            ExecutionStatus.BLOCKED,
            ExecutionStatus.SKIPPED,
            ExecutionStatus.ABORTED,
        }

        if (
            self.status in terminal_statuses
            and self.completed_at is None
        ):
            raise ExecutionValidationError(
                f"A {self.status.value} Execution requires completed_at."
            )

    @property
    def duration_seconds(self) -> float | None:
        """Return elapsed execution time in seconds when available."""
        if self.started_at is None or self.completed_at is None:
            return None

        return (
            self.completed_at - self.started_at
        ).total_seconds()

    @property
    def is_executed(self) -> bool:
        """Return whether execution activity has started."""
        return self.status is not ExecutionStatus.NOT_EXECUTED

    @property
    def is_terminal(self) -> bool:
        """Return whether the Execution has reached a final state."""
        return self.status in {
            ExecutionStatus.PASSED,
            ExecutionStatus.FAILED,
            ExecutionStatus.BLOCKED,
            ExecutionStatus.SKIPPED,
            ExecutionStatus.ABORTED,
        }

    @property
    def is_successful(self) -> bool:
        """Return whether the final execution result passed."""
        return self.status is ExecutionStatus.PASSED

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-compatible Execution data."""
        return {
            "execution_id": self.execution_id,
            "test_definition_id": self.test_definition_id,
            "environment": self.environment.value,
            "status": self.status.value,
            "execution_cycle": self.execution_cycle,
            "started_at": (
                self.started_at.isoformat()
                if self.started_at is not None
                else None
            ),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at is not None
                else None
            ),
            "executed_by": self.executed_by,
            "build_version": self.build_version,
            "source_system": self.source_system.value,
            "external_reference": self.external_reference,
            "defect_ids": list(self.defect_ids),
            "evidence_ids": list(self.evidence_ids),
            "remarks": self.remarks,
            "rerun_of_execution_id": self.rerun_of_execution_id,
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> "Execution":
        """Build and validate an Execution from dictionary input."""
        if not isinstance(data, Mapping):
            raise ExecutionValidationError(
                "Execution input must be a mapping."
            )

        payload = dict(data)

        if "started_at" in payload:
            payload["started_at"] = _parse_datetime(
                payload["started_at"],
                "started_at",
            )

        if "completed_at" in payload:
            payload["completed_at"] = _parse_datetime(
                payload["completed_at"],
                "completed_at",
            )

        try:
            return cls(**payload)
        except TypeError as exc:
            raise ExecutionValidationError(
                f"Invalid Execution fields: {exc}"
            ) from exc
