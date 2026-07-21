import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from dashboard_engine.builder import SnapshotBuilder


class BuilderTests(unittest.TestCase):
    def test_builds_sample_snapshot(self):
        snapshot = SnapshotBuilder(ROOT).build(ROOT / "sample_data" / "canonical_input.json")
        self.assertIn("kpis", snapshot)
        self.assertGreater(snapshot["kpis"]["total_features"], 0)
        self.assertEqual(len(snapshot["capability_groups"]), 4)


if __name__ == "__main__":
    unittest.main()
