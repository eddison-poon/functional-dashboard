"""Jira connector boundary.

This module intentionally defines the interface only. The next implementation phase
can add REST API authentication, pagination, Jira field extraction, and label mapping
without changing the dashboard or snapshot schema.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JiraConnector(ABC):
    @abstractmethod
    def fetch_issues(self, jql: str) -> list[dict[str, Any]]:
        """Return Jira issues matching the supplied JQL query."""
        raise NotImplementedError


class UnconfiguredJiraConnector(JiraConnector):
    def fetch_issues(self, jql: str) -> list[dict[str, Any]]:
        raise RuntimeError(
            "Jira connector is not configured. Use sample_data/canonical_input.json "
            "until the Jira integration phase is implemented."
        )
