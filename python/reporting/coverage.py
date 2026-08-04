"""
Coverage calculation utilities.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CoverageResult:
    covered:int
    total:int

    @property
    def percentage(self)->float:
        if self.total==0:
            return 0.0
        return round((self.covered/self.total)*100,2)

def calculate_coverage(covered:int,total:int)->CoverageResult:
    return CoverageResult(covered=covered,total=total)

def manual_coverage(total_manual:int,executed_manual:int)->CoverageResult:
    return calculate_coverage(executed_manual,total_manual)

def automation_coverage(total_auto:int,executed_auto:int)->CoverageResult:
    return calculate_coverage(executed_auto,total_auto)

def execution_coverage(total_tests:int,executed:int)->CoverageResult:
    return calculate_coverage(executed,total_tests)
