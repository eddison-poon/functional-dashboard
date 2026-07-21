from __future__ import annotations

from typing import Any

from .models import Status


VALID_STATUSES = {item.value for item in Status}


def validate_source(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    for group in payload.get("capability_groups", []):
        _unique(group.get("id"), "group", seen_ids, errors)
        for capability in group.get("capabilities", []):
            _unique(capability.get("id"), "capability", seen_ids, errors)
            for feature in capability.get("features", []):
                _unique(feature.get("id"), "feature", seen_ids, errors)
                for scenario in feature.get("scenarios", []):
                    _unique(scenario.get("id"), "scenario", seen_ids, errors)
                    for key in ("manual_status", "automation_status"):
                        status = scenario.get(key)
                        if status not in VALID_STATUSES:
                            errors.append(f"{scenario.get('id')}: invalid {key} '{status}'")
                    if not scenario.get("jira_id"):
                        errors.append(f"{scenario.get('id')}: jira_id is required")
                    for execution in scenario.get("executions", []):
                        _unique(execution.get("execution_id"), "execution", seen_ids, errors)
                        if execution.get("status") not in VALID_STATUSES:
                            errors.append(
                                f"{execution.get('execution_id')}: invalid status '{execution.get('status')}'"
                            )
    return errors


def _unique(value: str | None, kind: str, seen: set[str], errors: list[str]) -> None:
    if not value:
        errors.append(f"{kind} id is required")
    elif value in seen:
        errors.append(f"duplicate {kind} id: {value}")
    else:
        seen.add(value)
