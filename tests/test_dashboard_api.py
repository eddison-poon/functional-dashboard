"""Tests for the Phase 3.7 public Dashboard Engine API."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from dashboard_engine.api import (
    DashboardEngine,
    DashboardEngineConfig,
    DashboardEngineError,
)


class DashboardEngineApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.test_cases = self.root / "test_cases"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_asset(self, relative_path: str, content: str) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip(), encoding="utf-8")

    def test_generates_complete_dashboard_output(self) -> None:
        self._write_asset(
            "test_cases/reviewed/scenarios/scenario.md",
            """
# Create Jira Ticket

| Scenario ID | MCP-JIRA-001 |
| Scenario Name | Create Jira Ticket |
""",
        )
        self._write_asset(
            "test_cases/reviewed/manual/manual.md",
            """
# Create Jira Ticket Manually

| Manual Test ID | MCP-JIRA-M-001 |
| Parent Scenario ID | MCP-JIRA-001 |
""",
        )

        generated_at = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)
        output = DashboardEngine(self.root).generate_dashboard(
            generated_at=generated_at
        )

        self.assertTrue(output.is_clean)
        self.assertEqual(
            "MCP-JIRA-001",
            output.snapshot.repository_index.scenarios[0].asset_id,
        )
        self.assertEqual(
            "green",
            output.executive_summary.overall_health.value,
        )

    def test_generate_snapshot_returns_snapshot_only(self) -> None:
        self._write_asset(
            "test_cases/pending_review/scenarios/scenario.md",
            "| Scenario ID | S-001 |",
        )

        snapshot = DashboardEngine(self.root).generate_snapshot()

        self.assertEqual("1.0", snapshot.metadata.schema_version)

    def test_generate_executive_summary_returns_summary_only(self) -> None:
        self._write_asset(
            "test_cases/pending_review/scenarios/scenario.md",
            "| Scenario ID | S-001 |",
        )

        summary = DashboardEngine(self.root).generate_executive_summary()

        self.assertEqual("Test Design and Review", summary.current_phase)

    def test_supports_custom_configuration(self) -> None:
        custom_root = self.root / "custom_assets"
        self._write_asset(
            "custom_assets/reviewed/scenarios/scenario.md",
            "| Scenario ID | S-100 |",
        )
        config = DashboardEngineConfig(
            repository_root=self.root,
            asset_roots=(Path("custom_assets"),),
            green_minimum=90.0,
            amber_minimum=75.0,
            current_phase="Repository Review",
            source="unit-test",
        )

        output = DashboardEngine(config=config).generate_dashboard()

        self.assertEqual("unit-test", output.snapshot.metadata.source)
        self.assertEqual(
            "Repository Review",
            output.executive_summary.current_phase,
        )

    def test_output_is_json_compatible(self) -> None:
        self._write_asset(
            "test_cases/pending_review/scenarios/scenario.md",
            "| Scenario ID | S-001 |",
        )

        output = DashboardEngine(self.root).generate_dashboard()
        rendered = json.dumps(output.to_dict())

        self.assertIn('"snapshot"', rendered)
        self.assertIn('"executive_summary"', rendered)

    def test_rejects_repository_root_and_config_together(self) -> None:
        config = DashboardEngineConfig(repository_root=self.root)

        with self.assertRaises(ValueError):
            DashboardEngine(self.root, config=config)

    def test_wraps_invalid_repository_error(self) -> None:
        missing = self.root / "missing"

        with self.assertRaises(DashboardEngineError):
            DashboardEngine(missing).generate_dashboard()


if __name__ == "__main__":
    unittest.main()
