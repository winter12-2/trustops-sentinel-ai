let selectedAttachments = [];

const scenarios = {
  1: {
    action_type: "send_email",
    user_role: "employee",
    recipients: ["teammate@company.com"],
    subject: "Internal sprint update",
    content: "Sharing this week's internal sprint progress summary.",
    attachments: [],
    contains_pii: false,
    is_external: false,
    claim_requires_verification: false
  },
  2: {
    action_type: "send_email",
    user_role: "employee",
    recipients: ["partner@example.com"],
    subject: "Internal report for review",
    content: "Please review the attached internal report before tomorrow's meeting.",
    attachments: ["internal_report.pdf"],
    contains_pii: false,
    is_external: true,
    claim_requires_verification: false
  },
  3: {
    action_type: "send_email",
    user_role: "employee",
    recipients: ["external@example.com", "client@example.com"],
    subject: "Latest outage update",
    content: "Acme has a major outage affecting all customers today.",
    attachments: ["internal_report.pdf"],
    contains_pii: false,
    is_external: true,
    claim_requires_verification: true
  },
  4: {
    action_type: "send_email",
    user_role: "employee",
    recipients: [
      "a@example.com","b@example.com","c@example.com","d@example.com","e@example.com",
      "f@example.com","g@example.com","h@example.com","i@example.com","j@example.com",
      "k@example.com","l@example.com","m@example.com","n@example.com","o@example.com",
      "p@example.com","q@example.com","r@example.com","s@example.com","t@example.com",
      "u@example.com","v@example.com","w@example.com","x@example.com","y@example.com",
      "z@example.com"
    ],
    subject: "Customer churn and latest issue summary",
    content: "Sharing current issue details and customer retention observations.",
    attachments: ["churn.xlsx", "internal_report.pdf"],
    contains_pii: true,
    is_external: true,
    claim_requires_verification: true
  }
};

function splitCsv(value) {
  if (!value) return [];
  return value
    .split(",")
    .map(item => item.trim())
    .filter(item => item.length > 0);
}

function prettyJson(obj) {
  if (obj === null || obj === undefined) return "null";
  return JSON.stringify(obj, null, 2);
}

function statusClassFromThreat(threatLevel, decision) {
  const level = (threatLevel || "").toUpperCase();
  const dec = (decision || "").toUpperCase();

  if (dec === "BLOCK") return "status-block";
  if (level === "ESCALATE") return "status-escalate";
  if (level === "QUARANTINE") return "status-quarantine";
  if (level === "MONITOR") return "status-monitor";
  return "status-allow";
}

function decisionBadgeClass(decision) {
  const value = (decision || "").toUpperCase();
  if (value === "ALLOW") return "green-badge";
  if (value === "ALLOW_WITH_REDACTION" || value === "REQUIRE_APPROVAL") return "yellow-badge";
  if (value === "BLOCK") return "red-badge";
  return "neutral-badge";
}

function threatBadgeClass(threat) {
  const value = (threat || "").toUpperCase();
  if (value === "ALLOW") return "green-badge";
  if (value === "MONITOR" || value === "QUARANTINE") return "yellow-badge";
  if (value === "ESCALATE") return "red-badge";
  return "neutral-badge";
}

function renderReasons(reasons) {
  const $list = $("#reasonsList");
  $list.empty();

  if (!reasons || reasons.length === 0) {
    $list.append('<li class="list-group-item">No policy reasons returned.</li>');
    return;
  }

  reasons.forEach(reason => {
    $list.append(`<li class="list-group-item">${reason}</li>`);
  });
}

function renderResult(result) {
  $("#emptyState").addClass("d-none");
  $("#resultContainer").removeClass("d-none");

  $("#decisionText").text(result.decision || "-");
  $("#threatLevelText").text(result.threat_level || "-");
  $("#riskScoreText").text(result.risk_score ?? "-");

  renderReasons(result.reasons || []);
  $("#safeTransformBox").text(prettyJson(result.safe_transform));
  $("#liveVerificationBox").text(prettyJson(result.live_verification));

  const statusClass = statusClassFromThreat(result.threat_level, result.decision);
  $("#resultStatus")
    .removeClass("status-neutral status-allow status-monitor status-quarantine status-escalate status-block")
    .addClass(statusClass)
    .text(result.decision || "Done");

  $("#decisionBadge")
    .removeClass("neutral-badge green-badge yellow-badge red-badge")
    .addClass(decisionBadgeClass(result.decision))
    .text(result.decision || "Waiting");

  $("#threatBadge")
    .removeClass("neutral-badge green-badge yellow-badge red-badge")
    .addClass(threatBadgeClass(result.threat_level))
    .text(result.threat_level || "Waiting");

  const resultSection = document.getElementById("resultContainer");
  if (resultSection) {
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function setLoading(isLoading) {
  $("#loadingState").toggleClass("d-none", !isLoading);
  $("#evaluateBtn").prop("disabled", isLoading);
}

function renderAttachments() {
  const $list = $("#attachmentList");
  const $clearBtn = $("#clearAttachmentsBtn");

  if (!selectedAttachments.length) {
    $list.addClass("empty").html("No attachments selected.");
    $clearBtn.addClass("d-none");
    return;
  }

  $list.removeClass("empty");
  $clearBtn.removeClass("d-none");

  const items = selectedAttachments.map((name, index) => {
    return `
      <div class="attachment-chip">
        <span class="attachment-name">${name}</span>
        <button type="button" class="attachment-remove" data-index="${index}">&times;</button>
      </div>
    `;
  });

  $list.html(items.join(""));
}

function addFiles(files) {
  for (const file of files) {
    if (!selectedAttachments.includes(file.name)) {
      selectedAttachments.push(file.name);
    }
  }
  renderAttachments();
}

function applyScenario(data) {
  $("#action_type").val(data.action_type || "send_email");
  $("#user_role").val(data.user_role || "");
  $("#recipients").val((data.recipients || []).join(", "));
  $("#subject").val(data.subject || "");
  $("#content").val(data.content || "");
  $("#contains_pii").prop("checked", !!data.contains_pii);
  $("#is_external").prop("checked", !!data.is_external);
  $("#claim_requires_verification").prop("checked", !!data.claim_requires_verification);

  selectedAttachments = [...(data.attachments || [])];
  renderAttachments();
}

$(document).ready(function () {
  renderAttachments();

  $(".scenario-btn").on("click", function () {
    const id = $(this).data("scenario");
    if (scenarios[id]) {
      applyScenario(scenarios[id]);
    }
  });

  $("#loadSampleBtn").on("click", function () {
    applyScenario(scenarios[3]);
  });

  $("#addAttachmentBtn").on("click", function () {
    $("#attachmentPicker").trigger("click");
  });

  $("#attachmentPicker").on("change", function () {
    const files = this.files;
    if (files && files.length > 0) {
      addFiles(files);
    }
    $(this).val("");
  });

  $("#clearAttachmentsBtn").on("click", function () {
    selectedAttachments = [];
    renderAttachments();
  });

  $("#attachmentList").on("click", ".attachment-remove", function () {
    const index = Number($(this).data("index"));
    selectedAttachments.splice(index, 1);
    renderAttachments();
  });

  $("#actionForm").on("submit", async function (e) {
    e.preventDefault();

    const payload = {
      action_type: $("#action_type").val().trim(),
      user_role: $("#user_role").val().trim(),
      recipients: splitCsv($("#recipients").val()),
      subject: $("#subject").val().trim(),
      content: $("#content").val().trim(),
      attachments: selectedAttachments,
      contains_pii: $("#contains_pii").is(":checked"),
      is_external: $("#is_external").is(":checked"),
      claim_requires_verification: $("#claim_requires_verification").is(":checked")
    };

    setLoading(true);

    try {
      const response = await fetch("/evaluate-action", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const result = await response.json();
      renderResult(result);
    } catch (error) {
      $("#emptyState")
        .removeClass("d-none")
        .text(`Request failed: ${error.message}`);
      $("#resultContainer").addClass("d-none");
      $("#resultStatus")
        .removeClass("status-allow status-monitor status-quarantine status-escalate status-block")
        .addClass("status-neutral")
        .text("Error");
    } finally {
      setLoading(false);
    }
  });
});
