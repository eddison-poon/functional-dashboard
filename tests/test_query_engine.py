from python.reporting import QueryEngine


class DummyRepository:
    def __init__(self):
        self.scenarios = [1, 2, 3]
        self.test_definitions = ["A", "B"]
        self.executions = ["E1", "E2", "E3", "E4"]
        self.requirements = ["REQ1"]
        self.defects = []
        self.evidence = ["EV1"]


def test_repository_none():
    try:
        QueryEngine(None)
        assert False
    except ValueError:
        assert True


def test_total_scenarios():
    assert QueryEngine(DummyRepository()).total_scenarios() == 3


def test_filtering():
    result = QueryEngine(DummyRepository()).scenarios(filters=[lambda x: x > 1])
    assert result == [2, 3]
