/* PDPC enforcement index — loads data/rulings.json, renders the breakdown and
   the filterable register. Progressive enhancement: the page is meaningful
   without this script; with it, the full register becomes browsable. */
(function () {
  "use strict";

  var OBLIGATION_ORDER = [
    "Consent", "Purpose Limitation", "Notification", "Access", "Correction",
    "Accuracy", "Protection", "Retention Limitation", "Transfer Limitation",
    "Accountability", "Openness", "Do Not Call", "Data Protection",
    "Other PDPA offence", "Not adjudicated", "Unspecified"
  ];
  var FINDING_LABEL = {
    "breach": "Breach found", "no breach": "No breach",
    "undertaking": "Undertaking", "review": "Review", "other": "Other"
  };

  var els = {
    bars: document.getElementById("bars"),
    barsNote: document.getElementById("bars-note"),
    body: document.getElementById("ix-body"),
    count: document.getElementById("result-count"),
    accessList: document.getElementById("access-list"),
    fObligation: document.getElementById("f-obligation"),
    fType: document.getElementById("f-type"),
    fFinding: document.getElementById("f-finding"),
    fYear: document.getElementById("f-year"),
    fSearch: document.getElementById("f-search"),
    fReset: document.getElementById("f-reset")
  };

  function fail(msg) {
    if (els.body) els.body.innerHTML = '<tr><td colspan="6" class="ix-empty">' + msg + "</td></tr>";
    if (els.bars) els.bars.innerHTML = '<p class="meta">' + msg + "</p>";
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  fetch("data/rulings.json")
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) { init(data.records || []); })
    .catch(function () {
      fail("Could not load the register data file. View the source register at pdpc.gov.sg.");
    });

  function init(records) {
    setStats(records);
    renderBars(records);
    renderAccessList(records);
    populateFilters(records);
    bindFilters(records);
    render(records);
  }

  /* --- Headline figures (overwrite static fallbacks so they can't drift) --- */
  function setStats(records) {
    var years = records.map(function (r) { return r.year; }).filter(Boolean);
    var range = years.length ? Math.min.apply(null, years) + "–" + Math.max.apply(null, years) : "—";
    var accessBreaches = records.filter(function (r) {
      return r.finding === "breach" && r.obligations.indexOf("Access") !== -1;
    }).length;
    setText("total", records.length);
    setText("years", range);
    setText("accessBreaches", accessBreaches);
  }
  function setText(name, val) {
    document.querySelectorAll('[data-stat="' + name + '"]').forEach(function (n) {
      n.textContent = val;
    });
  }

  /* --- Breakdown bars: breach findings per obligation (Decisions) --- */
  function renderBars(records) {
    var counts = {};
    records.forEach(function (r) {
      if (r.finding !== "breach") return;
      r.obligations.forEach(function (o) { counts[o] = (counts[o] || 0) + 1; });
    });
    var rows = OBLIGATION_ORDER.filter(function (o) {
      return counts[o] || o === "Access";   // always show Access, even at zero
    });
    var max = Math.max(1, Math.max.apply(null, rows.map(function (o) { return counts[o] || 0; })));

    els.bars.innerHTML = "";
    rows.forEach(function (o) {
      var n = counts[o] || 0;
      var isAccess = o === "Access";
      var row = document.createElement("div");
      row.className = "bar-row" + (isAccess ? " bar-row--access" : "");
      row.innerHTML =
        '<span class="bar-row__lbl">' + esc(o) + "</span>" +
        '<span class="bar-track"><span class="bar-fill" style="width:' +
        (n / max * 100).toFixed(1) + '%"></span></span>' +
        '<span class="bar-row__n">' + n + (isAccess && n === 0 ? " — never" : "") + "</span>";
      els.bars.appendChild(row);
    });
    els.barsNote.textContent =
      "Bars show breach findings; an obligation can appear in more than one decision. " +
      "The Access Obligation row is highlighted because it stands at zero.";
  }

  /* --- Access spotlight: list every Access-tagged case --- */
  function renderAccessList(records) {
    var access = records.filter(function (r) { return r.obligations.indexOf("Access") !== -1; });
    if (!access.length || !els.accessList) return;
    els.accessList.innerHTML = "";
    access.sort(function (a, b) { return (b.year || 0) - (a.year || 0); });
    access.forEach(function (r) {
      var li = document.createElement("li");
      li.innerHTML =
        "<strong>" + esc(FINDING_LABEL[r.finding] || r.finding) + "</strong> · " +
        (r.year || "—") + " — " +
        '<a href="' + esc(r.detailUrl) + '" target="_blank" rel="noopener">' + esc(r.title) + "</a>";
      els.accessList.appendChild(li);
    });
  }

  /* --- Filter population --- */
  function populateFilters(records) {
    var obls = {};
    records.forEach(function (r) { r.obligations.forEach(function (o) { obls[o] = true; }); });
    OBLIGATION_ORDER.forEach(function (o) {
      if (obls[o]) els.fObligation.appendChild(opt(o, o));
    });
    var years = {};
    records.forEach(function (r) { if (r.year) years[r.year] = true; });
    Object.keys(years).sort().reverse().forEach(function (y) {
      els.fYear.appendChild(opt(y, y));
    });
  }
  function opt(value, label) {
    var o = document.createElement("option");
    o.value = value; o.textContent = label; return o;
  }

  function bindFilters(records) {
    ["fObligation", "fType", "fFinding", "fYear"].forEach(function (k) {
      els[k].addEventListener("change", function () { render(records); });
    });
    els.fSearch.addEventListener("input", function () { render(records); });
    els.fReset.addEventListener("click", function () {
      els.fObligation.value = ""; els.fType.value = ""; els.fFinding.value = "";
      els.fYear.value = ""; els.fSearch.value = ""; render(records);
    });
  }

  /* --- Render the table for the current filter state --- */
  function render(records) {
    var ob = els.fObligation.value, ty = els.fType.value, fi = els.fFinding.value,
        yr = els.fYear.value, q = els.fSearch.value.trim().toLowerCase();

    var rows = records.filter(function (r) {
      if (ob && r.obligations.indexOf(ob) === -1) return false;
      if (ty && r.type !== ty) return false;
      if (fi && r.finding !== fi) return false;
      if (yr && String(r.year) !== yr) return false;
      if (q && r.title.toLowerCase().indexOf(q) === -1) return false;
      return true;
    });

    els.count.textContent = rows.length + " of " + records.length + " cases" +
      (ob ? " · " + ob : "") +
      (ob === "Access" && !fi ? " — none are breach findings" : "");

    if (!rows.length) {
      els.body.innerHTML = '<tr><td colspan="6" class="ix-empty">No cases match these filters.</td></tr>';
      return;
    }

    var html = rows.map(function (r) {
      var tags = r.obligations.map(function (o) {
        return '<span class="tag' + (o === "Access" ? " tag--access" : "") + '">' + esc(o) + "</span>";
      }).join(" ");
      var breachClass = r.finding === "breach" ? "pill--breach"
        : r.finding === "no breach" ? "pill--ok" : "pill--neutral";
      var incident = r.dataBreachIncident && r.finding === "undertaking"
        ? ' <span class="tag tag--muted">data-breach incident</span>' : "";
      return "<tr>" +
        '<td class="ix-title">' + esc(r.title) + "</td>" +
        "<td>" + (r.type === "Commission's Decision" ? "Decision" : "Undertaking") + "</td>" +
        '<td class="ix-tags">' + tags + incident + "</td>" +
        '<td><span class="pill ' + breachClass + '">' + esc(FINDING_LABEL[r.finding] || r.finding) + "</span></td>" +
        "<td>" + (r.year || "—") + "</td>" +
        '<td><a class="ix-src" href="' + esc(r.detailUrl) + '" target="_blank" rel="noopener">PDPC&nbsp;↗</a></td>' +
        "</tr>";
    }).join("");
    els.body.innerHTML = html;
  }
})();
