function badgeClassForDecision(decision) {
  const value = (decision || "").toUpperCase();
  if (value === "ALLOW") return "badge-allow";
  if (value === "ALLOW_WITH_REDACTION" || value === "REQUIRE_APPROVAL") return "badge-approval";
  if (value === "BLOCK") return "badge-block";
  return "badge-allow";
}

function threatStatusClass(threat) {
  const value = (threat || "").toUpperCase();
  if (value === "ESCALATE") return "status-escalate";
  if (value === "QUARANTINE") return "status-quarantine";
  if (value === "MONITOR") return "status-monitor";
  return "status-allow";
}

function formatDate(value) {
  if (!value) return "-";
  return value.replace("T", " ").slice(0, 19);
}

function updateMetrics(rows) {
  $("#totalLogs").text(rows.length);

  const blocks = rows.filter(x => (x.decision || "").toUpperCase() === "BLOCK").length;
  const approvals = rows.filter(x => (x.decision || "").toUpperCase() === "REQUIRE_APPROVAL").length;
  const avgRisk = rows.length
    ? Math.round(rows.reduce((sum, row) => sum + Number(row.risk_score || 0), 0) / rows.length)
    : 0;

  $("#totalBlocks").text(blocks);
  $("#totalApprovals").text(approvals);
  $("#avgRisk").text(avgRisk);
}

function renderLogs(rows) {
  const $body = $("#logsTableBody");
  $body.empty();

  if (!rows || rows.length === 0) {
    $("#logsEmptyState").removeClass("d-none");
    return;
  }

  $("#logsEmptyState").addClass("d-none");

  rows.forEach(row => {
    const decisionBadge = `<span class="table-badge ${badgeClassForDecision(row.decision)}">${row.decision || "-"}</span>`;
    const threatBadge = `<span class="status-pill ${threatStatusClass(row.threat_level)}">${row.threat_level || "-"}</span>`;

    $body.append(`
      <tr>
        <td>${row.id ?? ""}</td>
        <td>${row.action_type ?? "-"}</td>
        <td>${row.user_role ?? "-"}</td>
        <td>${decisionBadge}</td>
        <td>${threatBadge}</td>
        <td>${row.risk_score ?? "-"}</td>
        <td>${formatDate(row.created_at)}</td>
      </tr>
    `);
  });
}

async function loadLogs() {
  $("#logsLoadingState").removeClass("d-none");
  $("#logsStatus")
    .removeClass("status-allow status-monitor status-quarantine status-escalate status-block")
    .addClass("status-neutral")
    .text("Loading");

  try {
    const response = await fetch("/action-logs");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const rows = await response.json();
    updateMetrics(rows);
    renderLogs(rows);

    $("#logsStatus")
      .removeClass("status-neutral")
      .addClass("status-allow")
      .text("Loaded");
  } catch (error) {
    $("#logsEmptyState")
      .removeClass("d-none")
      .text(`Could not load logs: ${error.message}`);

    $("#logsStatus")
      .removeClass("status-allow")
      .addClass("status-neutral")
      .text("Error");
  } finally {
    $("#logsLoadingState").addClass("d-none");
  }
}

$(document).ready(function () {
  loadLogs();
  $("#refreshLogsBtn").on("click", loadLogs);
});
