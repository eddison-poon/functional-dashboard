"""
Reusable reporting filters.
"""
from __future__ import annotations

def filter_environment(environment):
    return lambda obj: getattr(obj, "environment", None) == environment

def filter_status(status):
    return lambda obj: getattr(obj, "status", None) == status

def filter_priority(priority):
    return lambda obj: getattr(obj, "priority", None) == priority

def filter_feature(feature):
    return lambda obj: getattr(obj, "feature", None) == feature

def filter_requirement(requirement_id):
    return lambda obj: getattr(obj, "requirement_id", None) == requirement_id

def filter_manual():
    return lambda obj: getattr(obj, "test_type", "").lower() == "manual"

def filter_automation():
    return lambda obj: getattr(obj, "test_type", "").lower() == "automation"

def compose(*predicates):
    def _combined(obj):
        return all(p(obj) for p in predicates)
    return _combined
