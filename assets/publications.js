(() => {
  "use strict";
  const status = document.getElementById("publication-status");
  const announce = (text) => { if (status) status.textContent = text; };
  const canonical = () => document.querySelector('link[rel="canonical"]')?.href || location.href.split("#")[0];
  async function copy(text, html) {
    if (navigator.clipboard) {
      if (html && window.ClipboardItem && navigator.clipboard.write) {
        try {
          await navigator.clipboard.write([new ClipboardItem({
            "text/plain": new Blob([text], {type: "text/plain"}),
            "text/html": new Blob([html], {type: "text/html"})
          })]);
          return;
        } catch (_) { /* A plain-text copy remains useful when rich copy is unavailable. */ }
      }
      try { await navigator.clipboard.writeText(text); return; } catch (_) { /* Try the browser's selection copy. */ }
    }
    const area = document.createElement("textarea");
    area.value = text; area.readOnly = true;
    area.style.cssText = "position:fixed;left:-10000px;top:0";
    document.body.append(area); area.select();
    let ok = false;
    try { ok = document.execCommand("copy"); } finally { area.remove(); }
    if (!ok) throw new Error("Copy is unavailable. Use the download link.");
  }
  document.addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    try {
      const action = button.dataset.action;
      if (action === "print") { window.print(); return; }
      if (action === "share" && navigator.share) {
        await navigator.share({title: document.querySelector("h1")?.innerText || document.title, url: canonical()});
        announce("Share sheet opened."); return;
      }
      if (action === "copy-article") {
        const reading = document.getElementById("reading");
        const clone = reading.cloneNode(true);
        clone.querySelectorAll("a[href]").forEach((a) => { a.href = new URL(a.getAttribute("href"), canonical()).href; });
        const credit = "\n\nCanonical article: " + canonical();
        const source = document.createElement("p");
        const a = document.createElement("a"); a.href = canonical(); a.textContent = "Canonical article";
        source.append(a); clone.append(source);
        await copy(reading.innerText + credit, clone.innerHTML);
        announce("Article copied with its review status and sources. Paste it into your publisher.");
      } else if (action === "copy-all-links") {
        const links = [...document.querySelectorAll("[data-article-url]")].map((a) => a.textContent.trim() + "\n" + a.href);
        await copy(links.join("\n\n"));
        announce("Copied all " + links.length + " article links.");
      } else {
        await copy(canonical());
        announce(action === "share" ? "Sharing is unavailable here; the article link was copied." : "Article link copied.");
      }
    } catch (error) {
      announce(error.name === "AbortError" ? "Sharing canceled." : (error.message || "Use the download link to save this article."));
    }
  });
  const search = document.getElementById("article-search");
  const kind = document.getElementById("article-kind");
  if (search && kind) {
    const cards = [...document.querySelectorAll(".article-card")];
    const filter = () => {
      const query = search.value.trim().toLocaleLowerCase();
      let shown = 0;
      cards.forEach((card) => {
        const visible = (!query || card.dataset.search.includes(query)) && (kind.value === "all" || card.dataset.kind === kind.value);
        card.hidden = !visible; shown += Number(visible);
      });
      document.getElementById("article-count").textContent = shown + (shown === 1 ? " article shown" : " articles shown");
    };
    search.addEventListener("input", filter); kind.addEventListener("change", filter);
  }
})();

