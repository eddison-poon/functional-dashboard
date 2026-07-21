from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from .metrics import aggregate_score, environment_health, feature_status, latest_execution, scenario_score
from .models import HealthRules, Status, require_keys


class SnapshotBuilder:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.dashboard_config = self._load_json(root / "config" / "dashboard.json")
        health_payload = self._load_json(root / "config" / "health_rules.json")
        self.rules = HealthRules(
            green_min=int(health_payload["green_min"]),
            amber_min=int(health_payload["amber_min"]),
        )
        self.environments = self._load_json(root / "config" / "environments.json")["environments"]

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Required file not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    def build(self, source_path: Path) -> dict[str, Any]:
        source = self._load_json(source_path)
        require_keys(source, ["metadata", "capability_groups"], "source")
        output = deepcopy(source)

        all_scenarios: list[dict[str, Any]] = []
        all_features: list[dict[str, Any]] = []
        all_capabilities: list[dict[str, Any]] = []

        for group in output["capability_groups"]:
            require_keys(group, ["id", "name", "capabilities"], f"group {group.get('id', '?')}")
            group_scores: list[float] = []

            for capability in group["capabilities"]:
                require_keys(capability, ["id", "name", "features"], f"capability {capability.get('id', '?')}")
                all_capabilities.append(capability)
                feature_scores: list[float] = []
                latest_statuses: list[str] = []

                for feature in capability["features"]:
                    require_keys(feature, ["id", "name", "scenarios"], f"feature {feature.get('id', '?')}")
                    all_features.append(feature)
                    scenario_scores: list[float] = []

                    for scenario in feature["scenarios"]:
                        require_keys(
                            scenario,
                            ["id", "name", "jira_id", "manual_status", "automation_status", "executions"],
                            f"scenario {scenario.get('id', '?')}",
                        )
                        all_scenarios.append(scenario)
                        latest = latest_execution(scenario["executions"])
                        latest_statuses.append(latest["status"])

                        scenario["test_definition_id"] = (
                            scenario.get("automation_test_id")
                            or scenario.get("manual_test_id")
                            or "—"
                        )
                        scenario["jira_url"] = (
                            self.dashboard_config["jira_base_url"].rstrip("/") + "/" + scenario["jira_id"]
                        )
                        scenario["latest_execution"] = latest
                        scenario["execution_history"] = sorted(
                            scenario["executions"],
                            key=lambda item: item["executed_at"],
                            reverse=True,
                        )
                        scenario_scores.append(scenario_score(scenario))

                    feature["score"] = aggregate_score(scenario_scores)
                    feature["health"] = feature_status(feature["score"], self.rules)
                    feature_scores.append(feature["score"])

                capability["score"] = aggregate_score(feature_scores)
                capability["health"] = feature_status(capability["score"], self.rules)
                capability["summary"] = self._summary(capability["features"])

                env_source = capability.get("environments", {})
                capability["environments"] = {
                    env: environment_health(env_source.get(env, Status.NOT_EXECUTED.value), self.rules)
                    for env in self.environments
                }
                group_scores.append(capability["score"])

            group["score"] = aggregate_score(group_scores)
            group["health"] = feature_status(group["score"], self.rules)

        output["health_rules"] = {
            "green_min": self.rules.green_min,
            "amber_min": self.rules.amber_min,
        }
        output["kpis"] = self._kpis(all_features, all_scenarios, all_capabilities, output["metadata"])
        return output

    def _summary(self, features: list[dict[str, Any]]) -> dict[str, int]:
        summary = {"total_features": len(features), "ready": 0, "failed": 0, "blocked": 0, "not_executed": 0}
        for feature in features:
            statuses = [
                scenario["latest_execution"]["status"]
                for scenario in feature["scenarios"]
            ]
            if statuses and all(status == Status.PASSED.value for status in statuses):
                summary["ready"] += 1
            elif any(status == Status.FAILED.value for status in statuses):
                summary["failed"] += 1
            elif any(status == Status.BLOCKED.value for status in statuses):
                summary["blocked"] += 1
            else:
                summary["not_executed"] += 1
        return summary

    def _kpis(
        self,
        features: list[dict[str, Any]],
        scenarios: list[dict[str, Any]],
        capabilities: list[dict[str, Any]],
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        overall_score = aggregate_score([capability["score"] for capability in capabilities])
        ready = sum(1 for feature in features if feature["health"] == "green")

        manual_defined = sum(
            1 for scenario in scenarios
            if scenario.get("manual_test_id") and scenario.get("manual_status") != Status.NOT_EXECUTED.value
        )
        automation_defined = sum(
            1 for scenario in scenarios
            if scenario.get("automation_test_id") and scenario.get("automation_status") != Status.NOT_EXECUTED.value
        )
        total = len(scenarios) or 1

        snapshot_date = datetime.fromisoformat(metadata["generated_at"]).date()
        executions_today = [
            execution
            for scenario in scenarios
            for execution in scenario.get("executions", [])
            if datetime.fromisoformat(execution["executed_at"]).date() == snapshot_date
        ]

        failed_today = sum(1 for execution in executions_today if execution["status"] == Status.FAILED.value)
        blocked_today = sum(1 for execution in executions_today if execution["status"] == Status.BLOCKED.value)

        return {
            "overall_score": round(overall_score),
            "overall_health": self.rules.classify(overall_score).value,
            "features_ready": ready,
            "total_features": len(features),
            "manual_coverage": round(manual_defined / total * 100),
            "automation_coverage": round(automation_defined / total * 100),
            "executed_today": len(executions_today),
            "passed_today": sum(1 for execution in executions_today if execution["status"] == Status.PASSED.value),
            "failed_today": failed_today,
            "critical_issues": failed_today + blocked_today,
        }
