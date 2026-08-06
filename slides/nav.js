(function () {
  /* =========================
     CONFIG — edit here only
     ========================= */

  const SCHOOL = "LMU Munich";
  const AUTHOR = "Climate Change Statistics SoSe 2026 ·  Neural Hydrology";
  const DATE_TEXT = "2026-07-14";

  const SECTIONS = [
    "Introduction",
    "Background",
    "Research gap",
    "Methodology",
    "Results",
    "Discussion",
    "References"
  ];

  /* =========================
     Build HEADER (top nav)
     ========================= */

  const header = document.createElement("div");
  header.id = "top-nav";
  header.classList.add("is-hidden"); // hidden on title slide

  header.innerHTML = `
    <div class="nav-center">
      ${SECTIONS.map(
        (s, i) =>
          `<a href="#" data-sec="${s}">${s}</a>${
            i < SECTIONS.length - 1 ? `<span class="sep">|</span>` : ``
          }`
      ).join("")}
    </div>
  `;


  document.body.appendChild(header);

  const navLinks = Array.from(header.querySelectorAll("a[data-sec]"));

  // Prevent anchor clicks from breaking Reveal navigation
  navLinks.forEach((a) =>
    a.addEventListener("click", (e) => e.preventDefault())
  );

  function highlightSection(name) {
    navLinks.forEach((a) =>
      a.classList.toggle("active", a.dataset.sec === name)
    );
  }

  /* =========================
     Build FOOTER
     ========================= */

  const footer = document.createElement("div");
  footer.id = "slide-footer";
  footer.classList.add("is-hidden"); // hidden on title slide

  footer.innerHTML = `
    <div class="left footer-logo">
      <img src="${window.NAV_LOGO_SRC || 'logo.png'}" alt="LMU Munich logo">
    </div>
    <div class="center">${AUTHOR}</div>
    <div class="right"></div>
  `;

  document.body.appendChild(footer);

  const footerSectionLabel = footer.querySelector("#footer-section");

  /* =========================
     Reveal.js integration
     ========================= */

  function updateUI() {
  if (!window.Reveal) return;

  const indices = Reveal.getIndices();
  const hIndex = indices.h ?? 0;
  const currentSlide = Reveal.getCurrentSlide();

  const sectionName =
    currentSlide?.getAttribute("data-section") ||
    currentSlide?.querySelector("[data-section]")?.getAttribute("data-section") ||
    "";

  /* =========================
     Hide header/footer on Cover slide
     ========================= */
  if (sectionName === "Cover") {
    header.classList.add("is-hidden");
    footer.classList.add("is-hidden");
    return;
  }

  /* =========================
     Show header/footer on normal slides
     ========================= */
  header.classList.remove("is-hidden");
  footer.classList.remove("is-hidden");

  /* =========================
     Highlight active section
     ========================= */
  highlightSection(sectionName);
}


  /* =========================
     Init
     ========================= */

  function init() {
    if (!window.Reveal) {
      console.warn("Reveal.js not found");
      return;
    }

    // Run once when Reveal is ready
    Reveal.on("ready", updateUI);

    // Run on every slide change
    Reveal.on("slidechanged", updateUI);

    // Fallback: run once immediately
    updateUI();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
