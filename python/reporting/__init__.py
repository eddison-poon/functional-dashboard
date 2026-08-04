"""
Reporting engine package.

Provides reusable read-only query interfaces over the canonical
repository models.
"""

from .query_engine import QueryEngine

__all__ = ["QueryEngine"]
