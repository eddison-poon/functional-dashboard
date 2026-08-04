from reporting.filters import *

class Dummy:
    def __init__(self):
        self.environment="UAT"
        self.status="Passed"
        self.priority="High"
        self.feature="Jira"
        self.requirement_id="REQ-1"
        self.test_type="Manual"

def test_environment():
    assert filter_environment("UAT")(Dummy())
    assert not filter_environment("SIT")(Dummy())

def test_status():
    assert filter_status("Passed")(Dummy())

def test_priority():
    assert filter_priority("High")(Dummy())

def test_manual():
    assert filter_manual()(Dummy())

def test_compose():
    d=Dummy()
    assert compose(filter_environment("UAT"),filter_status("Passed"))(d)
