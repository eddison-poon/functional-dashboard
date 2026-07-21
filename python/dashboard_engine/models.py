from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class Status(StrEnum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    NOT_EXECUTED = "NOT_EXECUTED"


class Health(StrEnum):
    GREEN = "green"
    AMBER = "amber"
    RED = "red"
    GREY = "grey"


@dataclass(frozen=True)
class HealthRules:
    green_min: int = 80
    amber_min: int = 70

    def classify(self, score: float) -> Health:
        if score >= self.green_min:
            return Health.GREEN
        if score >= self.amber_min:
            return Health.AMBER
        return Health.RED


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def require_keys(payload: dict[str, Any], keys: list[str], context: str) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise ValueError(f"{context} missing required keys: {', '.join(missing)}")
