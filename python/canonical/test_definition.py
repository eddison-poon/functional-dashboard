"""
Canonical Test Definition model.

Purpose
-------
Defines reusable manual and automated tests covering canonical
Scenarios.

Inputs
------
Normalized Test Definition values supplied by builder or connector
modules.

Outputs
-------
Immutable TestDefinition and TestStep objects with JSON-compatible
dictionary output.

Dependencies
------------
Uses the Python standard library and canonical controlled
vocabularies.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping

from .enums import (
    AutomationFramework,
    TestDefinitionStatus,
    TestType,
)


class TestDefinitionValidationError(ValueError):
    """Raised when canonical Test Definition data is invalid."""


def _require_text(
    value: object,
    field_name: str,
    *,
    maximum_length: int,
) -> str:
    """Validate and normalize mandatory text."""

    if not isinstance(value, str):
        raise TestDefinitionValidationError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise TestDefinitionValidationError(
            f"{field_name} must not be empty."
        )

    if len(normalized) > maximum_length:
        raise TestDefinitionValidationError(
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
        raise TestDefinitionValidationError(
            f"{field_name} must be a string or null."
        )

    normalized = value.strip()

    if not normalized:
        return None

    if len(normalized) > maximum_length:
        raise TestDefinitionValidationError(
            f"{field_name} must not exceed "
            f"{maximum_length} characters."
        )

    return normalized


def _normalize_text_collection(
    value: object,
    field_name: str,
    *,
    lowercase: bool,
    maximum_item_length: int,
) -> tuple[str, ...]:
    """
    Normalize a collection of strings.

    Blank values are ignored. Values are deduplicated while preserving
    first-seen order.
    """

    if value is None:
        return ()

    if isinstance(value, str):
        raise TestDefinitionValidationError(
            f"{field_name} must be a collection of strings, "
            "not a single string."
        )

    try:
        raw_values = list(value)
    except TypeError as exc:
        raise TestDefinitionValidationError(
            f"{field_name} must be a collection of strings."
        ) from exc

    normalized_values: list[str] = []
    seen_values: set[str] = set()

    for index, raw_value in enumerate(raw_values):
        if not isinstance(raw_value, str):
            raise TestDefinitionValidationError(
                f"{field_name}[{index}] must be a string."
            )

        normalized = raw_value.strip()

        if lowercase:
            normalized = normalized.lower()

        if not normalized:
            continue

        if len(normalized) > maximum_item_length:
            raise TestDefinitionValidationError(
                f"{field_name}[{index}] must not exceed "
                f"{maximum_item_length} characters."
            )

        if normalized not in seen_values:
            seen_values.add(normalized)
            normalized_values.append(normalized)

    return tuple(normalized_values)


def _validate_version(value: object) -> str:
    """Validate a Test Definition version."""

    version = _require_text(
        value,
        "version",
        maximum_length=30,
    )

    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", version):
        raise TestDefinitionValidationError(
            "version must use the format major.minor "
            "or major.minor.patch."
        )

    return version


@dataclass(frozen=True, slots=True)
class TestStep:
    """One immutable manual test instruction."""

    step_number: int
    action: str
    expected_result: str
    test_data: str | None = None

    def __post_init__(self) -> None:
        """Normalize and validate the Test Step."""

        if type(self.step_number) is not int:
            raise TestDefinitionValidationError(
                "step_number must be an integer."
            )

        if self.step_number < 1:
            raise TestDefinitionValidationError(
                "step_number must be greater than zero."
            )

        object.__setattr__(
            self,
            "action",
            _require_text(
                self.action,
                "action",
                maximum_length=5_000,
            ),
        )

        object.__setattr__(
            self,
            "expected_result",
            _require_text(
                self.expected_result,
                "expected_result",
                maximum_length=5_000,
            ),
        )

        object.__setattr__(
            self,
            "test_data",
            _optional_text(
                self.test_data,
                "test_data",
                maximum_length=5_000,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return the Test Step as a JSON-compatible dictionary."""

        return {
            "step_number": self.step_number,
            "action": self.action,
            "expected_result": self.expected_result,
            "test_data": self.test_data,
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> "TestStep":
        """Build and validate a Test Step from dictionary input."""

        if not isinstance(data, Mapping):
            raise TestDefinitionValidationError(
                "Test Step input must be a mapping."
            )

        try:
            return cls(**dict(data))
        except TypeError as exc:
            raise TestDefinitionValidationError(
                f"Invalid Test Step fields: {exc}"
            ) from exc


def _normalize_steps(value: object) -> tuple[TestStep, ...]:
    """Normalize Test Step objects or dictionaries."""

    if value is None:
        return ()

    if isinstance(value, (str, bytes)):
        raise TestDefinitionValidationError(
            "steps must be a collection of Test Steps."
        )

    try:
        raw_steps = list(value)
    except TypeError as exc:
        raise TestDefinitionValidationError(
            "steps must be a collection of Test Steps."
        ) from exc

    normalized_steps: list[TestStep] = []

    for index, raw_step in enumerate(raw_steps):
        if isinstance(raw_step, TestStep):
            step = raw_step
        elif isinstance(raw_step, Mapping):
            step = TestStep.from_dict(raw_step)
        else:
            raise TestDefinitionValidationError(
                f"steps[{index}] must be a TestStep or mapping."
            )

        normalized_steps.append(step)

    step_numbers = [step.step_number for step in normalized_steps]

    if len(step_numbers) != len(set(step_numbers)):
        raise TestDefinitionValidationError(
            "Manual Test Step numbers must be unique."
        )

    if step_numbers:
        expected_numbers = list(range(1, len(step_numbers) + 1))

        if step_numbers != expected_numbers:
            raise TestDefinitionValidationError(
                "Manual Test Step numbers must form a continuous "
                "sequence beginning with 1."
            )

    return tuple(normalized_steps)


@dataclass(frozen=True, slots=True)
class TestDefinition:
    """Immutable canonical Manual or Automation Test Definition."""

    test_definition_id: str
    scenario_id: str
    test_type: TestType | str
    name: str
    status: TestDefinitionStatus | str

    version: str = "1.0"
    description: str | None = None
    preconditions: tuple[str, ...] | list[str] = field(
        default_factory=tuple
    )
    steps: tuple[TestStep, ...] | list[TestStep] | list[dict] = field(
        default_factory=tuple
    )

    framework: AutomationFramework | str | None = None
    repository: str | None = None
    script_path: str | None = None
    pipeline_name: str | None = None

    owner: str | None = None
    tags: tuple[str, ...] | list[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Normalize and validate the Test Definition."""

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
            "scenario_id",
            _require_text(
                self.scenario_id,
                "scenario_id",
                maximum_length=100,
            ),
        )

        parsed_test_type = TestType.parse(self.test_type)

        object.__setattr__(
            self,
            "test_type",
            parsed_test_type,
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
            "status",
            TestDefinitionStatus.parse(self.status),
        )

        object.__setattr__(
            self,
            "version",
            _validate_version(self.version),
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
            "preconditions",
            _normalize_text_collection(
                self.preconditions,
                "preconditions",
                lowercase=False,
                maximum_item_length=1_000,
            ),
        )

        normalized_steps = _normalize_steps(self.steps)

        object.__setattr__(
            self,
            "steps",
            normalized_steps,
        )

        parsed_framework: AutomationFramework | None

        if self.framework is None:
            parsed_framework = None
        else:
            parsed_framework = AutomationFramework.parse(
                self.framework
            )

        object.__setattr__(
            self,
            "framework",
            parsed_framework,
        )

        object.__setattr__(
            self,
            "repository",
            _optional_text(
                self.repository,
                "repository",
                maximum_length=500,
            ),
        )

        object.__setattr__(
            self,
            "script_path",
            _optional_text(
                self.script_path,
                "script_path",
                maximum_length=1_000,
            ),
        )

        object.__setattr__(
            self,
            "pipeline_name",
            _optional_text(
                self.pipeline_name,
                "pipeline_name",
                maximum_length=500,
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

        object.__setattr__(
            self,
            "tags",
            _normalize_text_collection(
                self.tags,
                "tags",
                lowercase=True,
                maximum_item_length=100,
            ),
        )

        self._validate_type_specific_fields()

    def _validate_type_specific_fields(self) -> None:
        """Validate Manual and Automation conditional rules."""

        if self.test_type is TestType.MANUAL:
            if not self.steps:
                raise TestDefinitionValidationError(
                    "A Manual Test Definition must contain at "
                    "least one Test Step."
                )

            automation_fields = {
                "framework": self.framework,
                "repository": self.repository,
                "script_path": self.script_path,
                "pipeline_name": self.pipeline_name,
            }

            populated_fields = [
                name
                for name, value in automation_fields.items()
                if value is not None
            ]

            if populated_fields:
                raise TestDefinitionValidationError(
                    "A Manual Test Definition must not define "
                    "automation fields: "
                    + ", ".join(populated_fields)
                    + "."
                )

        elif self.test_type is TestType.AUTOMATION:
            if self.steps:
                raise TestDefinitionValidationError(
                    "An Automation Test Definition must not contain "
                    "manual Test Steps."
                )

            if self.framework is None:
                raise TestDefinitionValidationError(
                    "An Automation Test Definition requires framework."
                )

            if self.script_path is None:
                raise TestDefinitionValidationError(
                    "An Automation Test Definition requires "
                    "script_path."
                )

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-compatible Test Definition data."""

        return {
            "test_definition_id": self.test_definition_id,
            "scenario_id": self.scenario_id,
            "test_type": self.test_type.value,
            "name": self.name,
            "status": self.status.value,
            "version": self.version,
            "description": self.description,
            "preconditions": list(self.preconditions),
            "steps": [step.to_dict() for step in self.steps],
            "framework": (
                self.framework.value
                if self.framework is not None
                else None
            ),
            "repository": self.repository,
            "script_path": self.script_path,
            "pipeline_name": self.pipeline_name,
            "owner": self.owner,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
    ) -> "TestDefinition":
        """Build a Test Definition from dictionary input."""

        if not isinstance(data, Mapping):
            raise TestDefinitionValidationError(
                "Test Definition input must be a mapping."
            )

        try:
            return cls(**dict(data))
        except TypeError as exc:
            raise TestDefinitionValidationError(
                f"Invalid Test Definition fields: {exc}"
            ) from exc
