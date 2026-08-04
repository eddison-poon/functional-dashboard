"""Tests for Phase 3.1 repository discovery."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from python.dashboard_engine.discovery import (
    AssetKind,
    RepositoryDiscovery,
    ReviewState,
)


class RepositoryDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.test_cases = self.root / "test_cases"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_discovers_markdown_assets_from_pending_review(self) -> None:
        path = (
            self.test_cases
            / "pending_review"
            / "business_scenarios"
            / "MCP-JIRA-001.md"
        )
        path.parent.mkdir(parents=True)
        path.write_text(
            """
# Create Jira Ticket

| Field | Value |
|---|---|
| Scenario ID | MCP-JIRA-001 |
| Scenario Name | Create Jira Ticket |
""".strip(),
            encoding="utf-8",
        )

        report = RepositoryDiscovery(self.root).discover()

        self.assertEqual(1, len(report.assets))
        asset = report.assets[0]
        self.assertEqual(AssetKind.BUSINESS_SCENARIO, asset.asset_kind)
        self.assertEqual(ReviewState.PENDING_REVIEW, asset.review_state)
        self.assertEqual("MCP-JIRA-001", asset.asset_id)
        self.assertEqual("Create Jira Ticket", asset.title)

    def test_discovers_json_manual_and_automation_assets(self) -> None:
        manual_path = self.test_cases / "reviewed" / "manual" / "manual.json"
        automation_path = self.test_cases / "published" / "automation" / "auto.json"
        manual_path.parent.mkdir(parents=True)
        automation_path.parent.mkdir(parents=True)

        manual_path.write_text(
            json.dumps(
                {
                    "manual_test_id": "MCP-JIRA-M-001",
                    "title": "Create ticket manually",
                }
            ),
            encoding="utf-8",
        )
        automation_path.write_text(
            json.dumps(
                {
                    "automation_test_id": "MCP-JIRA-A-001",
                    "title": "Create ticket through automation",
                }
            ),
            encoding="utf-8",
        )

        report = RepositoryDiscovery(self.root).discover()
        by_id = {asset.asset_id: asset for asset in report.assets}

        self.assertEqual(AssetKind.MANUAL_TEST, by_id["MCP-JIRA-M-001"].asset_kind)
        self.assertEqual(ReviewState.REVIEWED, by_id["MCP-JIRA-M-001"].review_state)
        self.assertEqual(
            AssetKind.AUTOMATION_TEST,
            by_id["MCP-JIRA-A-001"].asset_kind,
        )
        self.assertEqual(
            ReviewState.PUBLISHED,
            by_id["MCP-JIRA-A-001"].review_state,
        )

    def test_reports_duplicate_ids(self) -> None:
        first = self.test_cases / "pending_review" / "manual" / "first.md"
        second = self.test_cases / "reviewed" / "manual" / "second.md"
        first.parent.mkdir(parents=True)
        second.parent.mkdir(parents=True)
        body = "| Manual Test ID | MCP-JIRA-M-001 |"
        first.write_text(body, encoding="utf-8")
        second.write_text(body, encoding="utf-8")

        report = RepositoryDiscovery(self.root).discover()

        codes = [issue.code for issue in report.issues]
        self.assertIn("DUPLICATE_ASSET_ID", codes)

    def test_reports_parse_error_without_stopping_scan(self) -> None:
        bad = self.test_cases / "pending_review" / "manual" / "bad.json"
        good = self.test_cases / "pending_review" / "manual" / "good.json"
        bad.parent.mkdir(parents=True)
        bad.write_text("{broken", encoding="utf-8")
        good.write_text(
            json.dumps({"manual_test_id": "MCP-JIRA-M-002"}),
            encoding="utf-8",
        )

        report = RepositoryDiscovery(self.root).discover()

        self.assertEqual(1, len(report.assets))
        self.assertIn("PARSE_ERROR", [issue.code for issue in report.issues])

    def test_ignores_readme_and_unsupported_files(self) -> None:
        folder = self.test_cases / "pending_review" / "manual"
        folder.mkdir(parents=True)
        (folder / "README.md").write_text("Instructions", encoding="utf-8")
        (folder / "notes.txt").write_text("Not an asset", encoding="utf-8")

        report = RepositoryDiscovery(self.root).discover()

        self.assertEqual(0, len(report.assets))
        self.assertEqual(2, report.ignored_files)

    def test_report_counts_assets_by_kind_and_state(self) -> None:
        scenario = self.test_cases / "pending_review" / "scenarios" / "s.md"
        manual = self.test_cases / "reviewed" / "manual" / "m.md"
        scenario.parent.mkdir(parents=True)
        manual.parent.mkdir(parents=True)
        scenario.write_text("| Scenario ID | S-001 |", encoding="utf-8")
        manual.write_text("| Manual Test ID | M-001 |", encoding="utf-8")

        report = RepositoryDiscovery(self.root).discover()

        self.assertEqual(1, report.count_by_kind()["business_scenario"])
        self.assertEqual(1, report.count_by_kind()["manual_test"])
        self.assertEqual(1, report.count_by_state()["pending_review"])
        self.assertEqual(1, report.count_by_state()["reviewed"])

    def test_ignores_template_directory_assets(self) -> None:
        folder = self.test_cases / "templates"
        folder.mkdir(parents=True)
        (folder / "business_scenario_template.md").write_text(
            "| Scenario ID | <CAPABILITY-MODULE-NNN> |",
            encoding="utf-8",
        )

        report = RepositoryDiscovery(self.root, strict_unknown_state=True).discover()

        self.assertEqual(0, len(report.assets))
        self.assertEqual(1, report.ignored_files)
        self.assertTrue(report.is_clean)


if __name__ == "__main__":
    unittest.main()
