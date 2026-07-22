
"""
Controlled vocabularies for the canonical testing data model.

Purpose
-------
Defines the governed values used by requirements, scenarios, test
definitions, executions, evidence, defects, and source connectors.

Inputs
------
String values supplied by canonical data builders or connector modules.

Outputs
-------
Validated enum members that serialize cleanly into JSON strings.

Dependencies
------------
This module uses only the Python standard library.
"""

from __future__ import annotations

from enum import Enum
from typing import TypeVar


class InvalidEnumValueError(ValueError):
    """Raised when a value is not accepted by a controlled vocabulary."""


EnumType = TypeVar("EnumType", bound="CanonicalEnum")


class CanonicalEnum(str, Enum):
    """
    Base class for all canonical controlled vocabularies.

    Inheriting from both ``str`` and ``Enum`` means each enum member can
    be serialized by Python's standard JSON encoder as a string.
    """

    @classmethod
    def parse(cls: type[EnumType], value: object) -> EnumType:
        """
        Convert a string or existing enum member into a validated member.

        Parsing is case-insensitive and ignores surrounding whitespace.

        Examples
        --------
        ExecutionStatus.parse("passed")
        ExecutionStatus.parse(" PASSED ")
        ExecutionStatus.parse(ExecutionStatus.PASSED)

        All return:
            ExecutionStatus.PASSED

        Raises
        ------
        InvalidEnumValueError
            If the value is null, empty, not a string, or unsupported.
        """

        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            cls._raise_invalid(value)

        normalized_value = value.strip().upper()

        if not normalized_value:
            cls._raise_invalid(value)

        for member in cls:
            if member.value.upper() == normalized_value:
                return member

        cls._raise_invalid(value)

    @classmethod
    def values(cls) -> tuple[str, ...]:
        """Return all accepted canonical string values."""

        return tuple(member.value for member in cls)

    @classmethod
    def contains(cls, value: object) -> bool:
        """Return ``True`` when a value can be parsed by this enum."""

        try:
            cls.parse(value)
        except InvalidEnumValueError:
            return False

        return True

    @classmethod
    def _raise_invalid(cls, value: object) -> None:
        accepted_values = ", ".join(cls.values())

        raise InvalidEnumValueError(
            f"Invalid value {value!r} for {cls.__name__}. "
            f"Accepted values: {accepted_values}."
        )

    def __str__(self) -> str:
        """Return the canonical string value."""

        return self.value


class RequirementStatus(CanonicalEnum):
    """Lifecycle status of a business or technical requirement."""

    DRAFT = "DRAFT"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class RequirementType(CanonicalEnum):
    """Classification of a business or technical requirement."""

    EPIC = "EPIC"
    STORY = "STORY"
    TASK = "TASK"
    BUG = "BUG"
    CHANGE_REQUEST = "CHANGE_REQUEST"
    TECHNICAL_REQUIREMENT = "TECHNICAL_REQUIREMENT"
    BUSINESS_REQUIREMENT = "BUSINESS_REQUIREMENT"
    OTHER = "OTHER"
    

class TestDefinitionStatus(CanonicalEnum):
    """Lifecycle status of a reusable manual or automated test."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    DEPRECATED = "DEPRECATED"


class ExecutionStatus(CanonicalEnum):
    """Result or current state of an individual test execution."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    NOT_EXECUTED = "NOT_EXECUTED"
    SKIPPED = "SKIPPED"
    ABORTED = "ABORTED"
    IN_PROGRESS = "IN_PROGRESS"


class TestType(CanonicalEnum):
    """Execution approach used by a test definition."""

    MANUAL = "MANUAL"
    AUTOMATION = "AUTOMATION"


class Environment(CanonicalEnum):
    """Supported functional testing environments."""

    DEV = "DEV"
    SIT = "SIT"
    UAT = "UAT"
    PRE_PRODUCTION = "PRE_PRODUCTION"
    PRODUCTION_VERIFICATION = "PRODUCTION_VERIFICATION"


class Priority(CanonicalEnum):
    """Business or testing priority."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Severity(CanonicalEnum):
    """Impact level of a defect or testing issue."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ScenarioType(CanonicalEnum):
    """Classification of a functional testing scenario."""

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    BOUNDARY = "BOUNDARY"
    PERMISSION = "PERMISSION"
    INTEGRATION = "INTEGRATION"
    ERROR_HANDLING = "ERROR_HANDLING"
    REGRESSION = "REGRESSION"
    SMOKE = "SMOKE"


class EvidenceType(CanonicalEnum):
    """Evidence attached to an execution record."""

    SCREENSHOT = "SCREENSHOT"
    LOG = "LOG"
    VIDEO = "VIDEO"
    REPORT = "REPORT"
    TRACE = "TRACE"
    API_RESPONSE = "API_RESPONSE"
    ATTACHMENT = "ATTACHMENT"


class SourceSystem(CanonicalEnum):
    """Origin of a canonical record."""

    JIRA = "JIRA"
    XRAY = "XRAY"
    ZEPHYR = "ZEPHYR"
    TESTRAIL = "TESTRAIL"
    CSV = "CSV"
    GITHUB_ACTIONS = "GITHUB_ACTIONS"
    JENKINS = "JENKINS"
    PLAYWRIGHT = "PLAYWRIGHT"
    SELENIUM = "SELENIUM"
    PYTEST = "PYTEST"
    MANUAL_ENTRY = "MANUAL_ENTRY"
  
