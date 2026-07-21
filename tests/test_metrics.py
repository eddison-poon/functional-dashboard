import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from dashboard_engine.metrics import aggregate_score, latest_execution
from dashboard_engine.models import Health, HealthRules


class MetricsTests(unittest.TestCase):
    def test_health_thresholds(self):
        rules = HealthRules(green_min=80, amber_min=70)
        self.assertEqual(rules.classify(80), Health.GREEN)
        self.assertEqual(rules.classify(79), Health.AMBER)
        self.assertEqual(rules.classify(70), Health.AMBER)
        self.assertEqual(rules.classify(69), Health.RED)

    def test_latest_execution(self):
        executions = [
            {"execution_id": "1", "executed_at": "2026-07-21T10:00:00+08:00", "status": "FAILED"},
            {"execution_id": "2", "executed_at": "2026-07-22T10:00:00+08:00", "status": "PASSED"},
        ]
        self.assertEqual(latest_execution(executions)["execution_id"], "2")

    def test_aggregate_score(self):
        self.assertEqual(aggregate_score([100, 50, 0]), 50.0)
        self.assertEqual(aggregate_score([]), 0.0)


if __name__ == "__main__":
    unittest.main()
