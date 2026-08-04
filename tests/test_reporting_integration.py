"""
Integration tests for reporting package.
"""
from reporting import QueryEngine
from reporting.filters import filter_environment
from reporting.aggregations import count_by
from reporting.coverage import execution_coverage

class Execution:
    def __init__(self, environment, status):
        self.environment = environment
        self.status = status

class Repo:
    def __init__(self):
        self.scenarios=[1,2]
        self.test_definitions=["T1","T2"]
        self.executions=[
            Execution("UAT","Passed"),
            Execution("UAT","Failed"),
            Execution("SIT","Passed"),
        ]
        self.requirements=[]
        self.defects=[]
        self.evidence=[]

def test_query_filter_aggregate():
    engine=QueryEngine(Repo())
    uat=engine.executions(filters=[filter_environment("UAT")])
    result=count_by(uat, lambda x:x.status)
    assert result["Passed"]==1
    assert result["Failed"]==1

def test_execution_coverage():
    c=execution_coverage(10,7)
    assert c.covered==7
    assert c.total==10
    assert c.percentage==70.0
