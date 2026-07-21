(() => {
  "use strict";

  const state = {
    snapshot: null,
    selectedCapabilityId: null,
    expandedGroups: new Set(),
    searchTerm: ""
  };

  const els = {};

  document.addEventListener("DOMContentLoaded", () => {
    cacheElements();
    bindEvents();
    loadSnapshot();
  });

  function cacheElements() {
    [
      "releaseLabel", "sprintLabel", "buildLabel", "snapshotLabel",
      "kpiGrid", "capabilityTree", "detailContent", "refreshButton",
      "collapseAllButton", "capabilitySearch", "executionDialog",
      "dialogTitle", "dialogBody", "closeDialogButton"
    ].forEach(id => { els[id] = document.getElementById(id); });
  }

  function bindEvents() {
    els.refreshButton.addEventListener("click", loadSnapshot);
    els.collapseAllButton.addEventListener("click", () => {
      state.expandedGroups.clear();
      renderCapabilityTree();
    });
    els.capabilitySearch.addEventListener("input", event => {
      state.searchTerm = event.target.value.trim().toLowerCase();
      renderCapabilityTree();
    });
    els.closeDialogButton.addEventListener("click", closeDialog);
    els.executionDialog.addEventListener("click", event => {
      if (event.target === els.executionDialog) closeDialog();
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && !els.executionDialog.hidden) closeDialog();
    });
  }

  async function loadSnapshot() {
    els.refreshButton.disabled = true;
    els.refreshButton.textContent = "Loading…";

    try {
      const response = await fetch(`data/snapshot.json?ts=${Date.now()}`, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.snapshot = await response.json();
      validateSnapshot(state.snapshot);
      state.expandedGroups = new Set(
        state.snapshot.capability_groups
          .filter(group => group.default_expanded)
          .map(group => group.id)
      );
      renderAll();
    } catch (error) {
      console.error(error);
      els.detailContent.innerHTML = `
        <div class="error-banner">
          <strong>Unable to load dashboard data.</strong><br>
          Confirm <code>data/snapshot.json</code> exists and serve this repository through a web server.
        </div>`;
    } finally {
      els.refreshButton.disabled = false;
      els.refreshButton.textContent = "Refresh data";
    }
  }

  function validateSnapshot(snapshot) {
    const required = ["metadata", "kpis", "capability_groups"];
    for (const key of required) {
      if (!(key in snapshot)) throw new Error(`Snapshot missing '${key}'`);
    }
  }

  function renderAll() {
    renderMetadata();
    renderKpis();
    renderCapabilityTree();

    if (state.selectedCapabilityId) {
      const selected = findCapability(state.selectedCapabilityId);
      if (selected) renderCapabilityDetail(selected.group, selected.capability);
      else renderEmptyState();
    } else {
      renderEmptyState();
    }
  }

  function renderMetadata() {
    const meta = state.snapshot.metadata;
    els.releaseLabel.textContent = `Release ${meta.release}`;
    els.sprintLabel.textContent = `Sprint ${meta.sprint}`;
    els.buildLabel.textContent = `Build ${meta.build}`;
    els.snapshotLabel.textContent = `Snapshot ${formatDate(meta.generated_at)}`;
  }

  function renderKpis() {
    const cards = [
      ["Overall Health", `${state.snapshot.kpis.overall_score}%`, state.snapshot.kpis.overall_health, "Calculated from current feature readiness"],
      ["Features Ready", `${state.snapshot.kpis.features_ready}/${state.snapshot.kpis.total_features}`, null, "Ready across selected release"],
      ["Manual Coverage", `${state.snapshot.kpis.manual_coverage}%`, healthForScore(state.snapshot.kpis.manual_coverage), "Reusable manual test definitions"],
      ["Automation Coverage", `${state.snapshot.kpis.automation_coverage}%`, healthForScore(state.snapshot.kpis.automation_coverage), "Reusable automated test definitions"],
      ["Executed Today", state.snapshot.kpis.executed_today, null, `${state.snapshot.kpis.passed_today} passed · ${state.snapshot.kpis.failed_today} failed`],
      ["Critical Issues", state.snapshot.kpis.critical_issues, state.snapshot.kpis.critical_issues > 0 ? "red" : "green", "Release-impacting defects or blockers"]
    ];

    els.kpiGrid.innerHTML = cards.map(([label, value, health, detail]) => `
      <article class="kpi-card ${health ? `health-${health}` : ""}">
        <span class="kpi-label">${escapeHtml(label)}</span>
        <strong class="kpi-value">${escapeHtml(String(value))}</strong>
        <span class="kpi-detail">${escapeHtml(detail)}</span>
      </article>
    `).join("");
  }

  function renderCapabilityTree() {
    const term = state.searchTerm;
    const groups = state.snapshot.capability_groups.filter(group => {
      if (!term) return true;
      return group.name.toLowerCase().includes(term) ||
        group.capabilities.some(cap => cap.name.toLowerCase().includes(term));
    });

    if (!groups.length) {
      els.capabilityTree.innerHTML = `<p class="feature-meta">No matching capabilities.</p>`;
      return;
    }

    els.capabilityTree.innerHTML = groups.map(group => {
      const isOpen = term ? true : state.expandedGroups.has(group.id);
      const visibleCaps = group.capabilities.filter(cap =>
        !term || group.name.toLowerCase().includes(term) || cap.name.toLowerCase().includes(term)
      );
      return `
        <div class="tree-group">
          <button class="tree-row" type="button"
                  data-action="toggle-group" data-group-id="${escapeAttr(group.id)}"
                  aria-expanded="${isOpen}">
            <span class="tree-toggle ${isOpen ? "open" : ""}" aria-hidden="true">›</span>
            <span class="tree-name">${escapeHtml(group.name)}</span>
            <span class="health-dot ${escapeAttr(group.health)}" title="${escapeAttr(group.health)}"></span>
          </button>
          <div class="tree-children" ${isOpen ? "" : "hidden"}>
            ${visibleCaps.map(cap => `
              <button class="tree-row child ${state.selectedCapabilityId === cap.id ? "active" : ""}"
                      type="button" role="treeitem"
                      data-action="select-capability"
                      data-capability-id="${escapeAttr(cap.id)}">
                <span></span>
                <span class="tree-name">${escapeHtml(cap.name)}</span>
                <span class="health-dot ${escapeAttr(cap.health)}" title="${escapeAttr(cap.health)}"></span>
              </button>
            `).join("")}
          </div>
        </div>`;
    }).join("");

    els.capabilityTree.querySelectorAll("[data-action='toggle-group']").forEach(button => {
      button.addEventListener("click", () => {
        const id = button.dataset.groupId;
        state.expandedGroups.has(id) ? state.expandedGroups.delete(id) : state.expandedGroups.add(id);
        renderCapabilityTree();
      });
    });

    els.capabilityTree.querySelectorAll("[data-action='select-capability']").forEach(button => {
      button.addEventListener("click", () => {
        state.selectedCapabilityId = button.dataset.capabilityId;
        const selected = findCapability(state.selectedCapabilityId);
        renderCapabilityTree();
        renderCapabilityDetail(selected.group, selected.capability);
      });
    });
  }

  function findCapability(id) {
    for (const group of state.snapshot.capability_groups) {
      const capability = group.capabilities.find(item => item.id === id);
      if (capability) return { group, capability };
    }
    return null;
  }

  function renderEmptyState() {
    els.detailContent.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon" aria-hidden="true">◎</div>
        <h2 id="detailTitle">Select a capability</h2>
        <p>Choose an item from the left panel to review feature readiness, scenario results, environment health, and execution history.</p>
      </div>`;
  }

  function renderCapabilityDetail(group, capability) {
    els.detailContent.innerHTML = `
      <div class="breadcrumbs">Agent Hub › ${escapeHtml(group.name)} › ${escapeHtml(capability.name)}</div>
      <div class="detail-title-row">
        <div>
          <h2 id="detailTitle">${escapeHtml(capability.name)}</h2>
          <p class="detail-subtitle">${escapeHtml(capability.description || "Capability testing readiness")}</p>
        </div>
        <span class="health-pill ${escapeAttr(capability.health)}">${escapeHtml(capability.health.toUpperCase())} · ${capability.score}%</span>
      </div>

      ${renderSummary(capability.summary)}
      ${renderEnvironmentGrid(capability.environments)}
      ${renderFeatureList(capability)}
      <div id="featureWorkspace"></div>
    `;

    els.detailContent.querySelectorAll("[data-feature-id]").forEach(button => {
      button.addEventListener("click", () => {
        const feature = capability.features.find(item => item.id === button.dataset.featureId);
        renderFeatureWorkspace(capability, feature);
      });
    });

    if (capability.features.length) renderFeatureWorkspace(capability, capability.features[0]);
  }

  function renderSummary(summary) {
    const items = [
      ["Features", summary.total_features],
      ["Ready", summary.ready],
      ["Failed", summary.failed],
      ["Blocked", summary.blocked],
      ["Not Executed", summary.not_executed]
    ];
    return `<div class="summary-grid">${items.map(([label, value]) => `
      <div class="summary-card">
        <span class="summary-label">${escapeHtml(label)}</span>
        <span class="summary-value">${escapeHtml(String(value))}</span>
      </div>`).join("")}</div>`;
  }

  function renderEnvironmentGrid(environments) {
    return `
      <section class="content-section">
        <h3>Environment health</h3>
        <div class="environment-grid">
          ${Object.entries(environments).map(([env, data]) => `
            <div class="environment-card">
              <span class="health-pill ${escapeAttr(data.health)}">${escapeHtml(env)}</span>
              <strong>${data.score}%</strong>
              <span>${escapeHtml(data.status)}</span>
            </div>`).join("")}
        </div>
      </section>`;
  }

  function renderFeatureList(capability) {
    return `
      <section class="content-section">
        <h3>Features</h3>
        <div class="feature-list">
          ${capability.features.map(feature => `
            <button class="feature-button" type="button" data-feature-id="${escapeAttr(feature.id)}">
              <span>
                <span class="feature-name">${escapeHtml(feature.name)}</span>
                <span class="feature-meta">${feature.scenarios.length} scenario${feature.scenarios.length === 1 ? "" : "s"}</span>
              </span>
              <span class="health-pill ${escapeAttr(feature.health)}">${feature.score}%</span>
              <span aria-hidden="true">›</span>
            </button>`).join("")}
        </div>
      </section>`;
  }

  function renderFeatureWorkspace(capability, feature) {
    const workspace = document.getElementById("featureWorkspace");
    workspace.innerHTML = `
      <section class="content-section">
        <div class="detail-title-row">
          <div>
            <p class="eyebrow">Selected feature</p>
            <h3>${escapeHtml(feature.name)}</h3>
          </div>
          <span class="health-pill ${escapeAttr(feature.health)}">${escapeHtml(feature.health.toUpperCase())} · ${feature.score}%</span>
        </div>
        <div class="scenario-table-wrap">
          <table class="scenario-table">
            <thead>
              <tr>
                <th>Scenario</th>
                <th>Manual</th>
                <th>Automation</th>
                <th>Latest execution</th>
                <th>Executed</th>
                <th>Jira</th>
                <th>History</th>
              </tr>
            </thead>
            <tbody>
              ${feature.scenarios.map(scenario => `
                <tr>
                  <td>
                    <div class="scenario-name">${escapeHtml(scenario.name)}</div>
                    <div class="feature-meta">${escapeHtml(scenario.test_definition_id)}</div>
                  </td>
                  <td>${resultIcon(scenario.manual_status)}</td>
                  <td>${resultIcon(scenario.automation_status)}</td>
                  <td>${resultIcon(scenario.latest_execution.status)}</td>
                  <td>${escapeHtml(formatDate(scenario.latest_execution.executed_at))}</td>
                  <td><a href="${escapeAttr(scenario.jira_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(scenario.jira_id)} ↗</a></td>
                  <td><button class="link-button" type="button" data-history-scenario="${escapeAttr(scenario.id)}">View</button></td>
                </tr>`).join("")}
            </tbody>
          </table>
        </div>
      </section>`;

    workspace.querySelectorAll("[data-history-scenario]").forEach(button => {
      button.addEventListener("click", () => {
        const scenario = feature.scenarios.find(item => item.id === button.dataset.historyScenario);
        openExecutionDialog(scenario);
      });
    });
  }

  function resultIcon(status) {
    const normalized = (status || "NOT_EXECUTED").toUpperCase();
    const map = {
      PASSED: ["pass", "✓", "Passed"],
      FAILED: ["fail", "×", "Failed"],
      BLOCKED: ["blocked", "!", "Blocked"],
      NOT_EXECUTED: ["none", "–", "Not executed"]
    };
    const [klass, symbol, label] = map[normalized] || map.NOT_EXECUTED;
    return `<span class="result-icon ${klass}" title="${label}" aria-label="${label}">${symbol}</span>`;
  }

  function openExecutionDialog(scenario) {
    els.dialogTitle.textContent = scenario.name;
    els.dialogBody.innerHTML = `
      <p class="detail-subtitle">${escapeHtml(scenario.test_definition_id)} · ${escapeHtml(scenario.jira_id)}</p>
      <div class="history-list">
        ${scenario.execution_history.map(run => `
          <div class="history-row">
            <span><strong>${escapeHtml(run.execution_id)}</strong><br><small>${escapeHtml(formatDate(run.executed_at))}</small></span>
            <span class="status-pill ${escapeAttr(run.status.toLowerCase().replace("_", "-"))}">${escapeHtml(run.status)}</span>
            <span>${escapeHtml(run.environment)}</span>
            <span>${escapeHtml(run.build)}</span>
          </div>`).join("")}
      </div>`;
    els.executionDialog.hidden = false;
    els.closeDialogButton.focus();
  }

  function closeDialog() {
    els.executionDialog.hidden = true;
  }

  function healthForScore(score) {
    const rules = state.snapshot.health_rules;
    if (score >= rules.green_min) return "green";
    if (score >= rules.amber_min) return "amber";
    return "red";
  }

  function formatDate(value) {
    if (!value) return "—";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return new Intl.DateTimeFormat("en-US", {
      month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit",
      hour12: false
    }).format(date);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    })[char]);
  }

  function escapeAttr(value) {
    return escapeHtml(value);
  }
})();
