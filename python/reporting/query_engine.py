"""
Canonical reporting query engine.
"""

from __future__ import annotations
from typing import Callable, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class QueryEngine:
    def __init__(self, repository):
        if repository is None:
            raise ValueError("repository cannot be None")
        self._repository = repository

    @staticmethod
    def _apply_filters(
        items: Iterable[T],
        filters: Optional[list[Callable[[T], bool]]] = None,
    ) -> List[T]:
        results = list(items)
        if not filters:
            return results
        for predicate in filters:
            results = [item for item in results if predicate(item)]
        return results

    def scenarios(self, filters=None):
        return self._apply_filters(getattr(self._repository, "scenarios", []), filters)

    def test_definitions(self, filters=None):
        return self._apply_filters(getattr(self._repository, "test_definitions", []), filters)

    def executions(self, filters=None):
        return self._apply_filters(getattr(self._repository, "executions", []), filters)

    def requirements(self, filters=None):
        return self._apply_filters(getattr(self._repository, "requirements", []), filters)

    def defects(self, filters=None):
        return self._apply_filters(getattr(self._repository, "defects", []), filters)

    def evidence(self, filters=None):
        return self._apply_filters(getattr(self._repository, "evidence", []), filters)

    def total_scenarios(self):
        return len(self.scenarios())

    def total_test_definitions(self):
        return len(self.test_definitions())

    def total_executions(self):
        return len(self.executions())

    def total_requirements(self):
        return len(self.requirements())

    def total_defects(self):
        return len(self.defects())

    def total_evidence(self):
        return len(self.evidence())
