/* PDPC grievance site — progressive enhancement only */
(function () {
  "use strict";

  /* --- Scrollspy: highlight the nav link for the section in view --- */
  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll(".sitenav__links a")
  );
  var byId = {};
  navLinks.forEach(function (a) {
    var id = a.getAttribute("href").replace("#", "");
    byId[id] = a;
  });

  var sections = navLinks
    .map(function (a) { return document.getElementById(a.getAttribute("href").replace("#", "")); })
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    var current = null;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          if (current !== id) {
            if (current && byId[current]) byId[current].classList.remove("is-active");
            if (byId[id]) byId[id].classList.add("is-active");
            current = id;
          }
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
    sections.forEach(function (s) { observer.observe(s); });
  }

  /* --- Expand / collapse all (failures accordion) --- */
  var toggleAll = document.getElementById("toggle-all");
  var accordion = document.getElementById("failures-accordion");
  if (toggleAll && accordion) {
    toggleAll.addEventListener("click", function () {
      var expanded = toggleAll.getAttribute("aria-expanded") === "true";
      var items = accordion.querySelectorAll("details.failure");
      items.forEach(function (d) { d.open = !expanded; });
      toggleAll.setAttribute("aria-expanded", String(!expanded));
      toggleAll.firstChild.nodeValue = expanded ? "Expand all" : "Collapse all";
    });
  }

  /* --- Expand all failures for printing, restore after --- */
  if (accordion) {
    var beforePrint = function () {
      accordion.querySelectorAll("details.failure").forEach(function (d) {
        if (!d.open) { d.dataset.wasClosed = "1"; d.open = true; }
      });
    };
    var afterPrint = function () {
      accordion.querySelectorAll('details.failure[data-was-closed="1"]').forEach(function (d) {
        d.open = false; delete d.dataset.wasClosed;
      });
    };
    if (window.matchMedia) {
      var mql = window.matchMedia("print");
      if (mql.addEventListener) {
        mql.addEventListener("change", function (e) { e.matches ? beforePrint() : afterPrint(); });
      }
    }
    window.addEventListener("beforeprint", beforePrint);
    window.addEventListener("afterprint", afterPrint);
  }
})();
