from reporting.latest_execution import latest_execution, latest_by_test_definition
from datetime import datetime

class E:
    def __init__(self,tid,eid,t):
        self.test_definition_id=tid
        self.execution_id=eid
        self.execution_time=t

def test_latest():
    e1=E("T1","1",datetime(2026,1,1))
    e2=E("T1","2",datetime(2026,2,1))
    assert latest_execution([e1,e2]).execution_id=="2"

def test_group():
    e1=E("A","1",datetime(2026,1,1))
    e2=E("B","1",datetime(2026,1,2))
    assert len(latest_by_test_definition([e1,e2]))==2
