from __future__ import annotations

from collections import Counter
from typing import Any

from .models import Health, HealthRules, Status


STATUS_SCORE = {
    Status.PASSED.value: 100,
    Status.BLOCKED.value: 50,
    Status.FAILED.value: 0,
    Status.NOT_EXECUTED.value: 0,
}


def latest_execution(executions: list[dict[str, Any]]) -> dict[str, Any]:
    if not executions:
        return {
            "execution_id": "—",
            "status": Status.NOT_EXECUTED.value,
            "environment": "—",
            "build": "—",
            "executed_at": None,
        }
    return max(executions, key=lambda item: item["executed_at"])


def scenario_score(scenario: dict[str, Any]) -> float:
    latest = latest_execution(scenario.get("executions", []))
    statuses = [
        scenario.get("manual_status", Status.NOT_EXECUTED.value),
        scenario.get("automation_status", Status.NOT_EXECUTED.value),
        latest["status"],
    ]
    return sum(STATUS_SCORE.get(status, 0) for status in statuses) / len(statuses)


def aggregate_score(values: list[float]) -> float:
    return round(sum(values) / len(values), 1) if values else 0.0


def status_counts(statuses: list[str]) -> Counter:
    return Counter(statuses)


def environment_health(status: str, rules: HealthRules) -> dict[str, Any]:
    score = STATUS_SCORE.get(status, 0)
    health = Health.GREY if status == Status.NOT_EXECUTED.value else rules.classify(score)
    return {
        "status": status.replace("_", " ").title(),
        "score": score,
        "health": health.value,
    }


def feature_status(score: float, rules: HealthRules) -> str:
    return rules.classify(score).value
