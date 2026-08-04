"""
Aggregation helpers for reporting.
"""
from __future__ import annotations
from collections import Counter
from typing import Any, Callable, Iterable

def count(items: Iterable[Any]) -> int:
    return sum(1 for _ in items)

def group_by(items: Iterable[Any], key: Callable[[Any], Any]) -> dict[Any, list[Any]]:
    result: dict[Any, list[Any]] = {}
    for item in items:
        k = key(item)
        result.setdefault(k, []).append(item)
    return result

def count_by(items: Iterable[Any], key: Callable[[Any], Any]) -> dict[Any, int]:
    return dict(Counter(key(i) for i in items))

def pass_rate(items: Iterable[Any], status_attr: str="status", passed_value: str="Passed") -> float:
    items = list(items)
    if not items:
        return 0.0
    passed = sum(1 for i in items if getattr(i, status_attr, None)==passed_value)
    return round((passed/len(items))*100,2)

def failure_rate(items: Iterable[Any], status_attr: str="status", failed_value: str="Failed") -> float:
    items = list(items)
    if not items:
        return 0.0
    failed = sum(1 for i in items if getattr(i, status_attr, None)==failed_value)
    return round((failed/len(items))*100,2)
