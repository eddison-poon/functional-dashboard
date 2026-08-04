from python.reporting.aggregations import *

class Item:
    def __init__(self,s,e):
        self.status=s
        self.environment=e

items=[Item("Passed","UAT"),Item("Passed","SIT"),Item("Failed","UAT")]

def test_count():
    assert count(items)==3

def test_group_by():
    g=group_by(items, lambda x:x.environment)
    assert len(g["UAT"])==2

def test_count_by():
    c=count_by(items, lambda x:x.status)
    assert c["Passed"]==2

def test_pass_rate():
    assert pass_rate(items)==66.67

def test_failure_rate():
    assert failure_rate(items)==33.33
