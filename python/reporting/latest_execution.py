"""
Latest execution resolver.
"""
from __future__ import annotations

def latest_execution(executions):
    executions=list(executions)
    if not executions:
        return None
    return max(
        executions,
        key=lambda e:(
            getattr(e,"execution_time",None),
            getattr(e,"execution_id","")
        )
    )

def latest_by_test_definition(executions):
    groups={}
    for e in executions:
        tid=getattr(e,"test_definition_id",None)
        groups.setdefault(tid,[]).append(e)
    return {k:latest_execution(v) for k,v in groups.items()}
