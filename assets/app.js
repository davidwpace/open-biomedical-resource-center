"use strict";
(() => {
  const $ = (selector) => document.querySelector(selector);
  const fields = {
    search: $("#search"), category: $("#category"), access: $("#access"),
    sort: $("#sort"), chips: $("#categoryChips"), results: $("#results"),
    count: $("#resultCount"), empty: $("#empty"), error: $("#loadError"),
    dialog: $("#resourceDialog"), detail: $("#detailContent")
  };
  const icons = {
    "NAMs and human models":"◌", "Genomics, transcriptomics and pathways":"⌘",
    "Drug discovery and variant interpretation":"⌬", "Simulation and systems biology":"◈",
    "Literature, trials and education":"▤", "Imaging and pathology":"⬡",
    "Analysis and website infrastructure":"◇"
  };
  let resources = [];
  const clean = (value) => String(value == null ? "" : value);
  const esc = (value) => clean(value).replace(/[&<>"']/g, (char) => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  })[char]);
  const safeUrl = (url) => {
    try { const u = new URL(url); return ["https:", "http:"].includes(u.protocol) ? u.href : "#"; }
    catch { return "#"; }
  };
  function accessGroup(access) {
    const a = clean(access).toLowerCase();
    if (a.includes("commercial research") || a.includes("public learning materials")) return "commercial";
    if (/restricted|controlled|authoriz|quota|limit|varies|fee-based|not supplied free|paywall|academic\/nonprofit|commercial|some |free tier|github free/.test(a)) return "mixed";
    return "free";
  }
  const accessLabel = {free:"Free access", mixed:"Free with conditions", commercial:"Commercial / learning"};
  function getState() {
    return {q: fields.search.value.trim(), category: fields.category.value, access: fields.access.value, sort: fields.sort.value};
  }
  function matches(resource, state) {
    if (state.category !== "all" && resource.category !== state.category) return false;
    if (state.access !== "all" && accessGroup(resource.access) !== state.access) return false;
    const words = state.q.toLocaleLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return true;
    const haystack = [resource.name, resource.purpose, resource.category, resource.tags?.join(" "), resource.access, resource.limitations].join(" ").toLocaleLowerCase();
    return words.every(word => haystack.includes(word));
  }
  function sorted(items, kind) {
    return items.sort((a,b) => {
      if (kind === "name") return a.name.localeCompare(b.name);
      if (kind === "category") return a.category.localeCompare(b.category) || a.name.localeCompare(b.name);
      return a.priority.localeCompare(b.priority) || a.name.localeCompare(b.name);
    });
  }
  function resourceCard(r) {
    const group = accessGroup(r.access);
    return `<article class="resource-card">
      <div class="card-top"><span class="resource-icon" aria-hidden="true">${icons[r.category]||"◇"}</span>
        <span class="access-pill ${group}">${accessLabel[group]}</span></div>
      <p class="card-category">${esc(r.category)}</p>
      <h3>${esc(r.name)}</h3>
      <p class="description">${esc(r.purpose)}</p>
      <div class="card-limit"><strong>Access:</strong> ${esc(r.access)}<br><strong>Note:</strong> ${esc(r.limitations)}</div>
      <div class="card-footer">
        <button class="detail-button" type="button" data-detail="${esc(r.id)}" aria-label="View details for ${esc(r.name)}">View details +</button>
        <a class="official-link" href="${esc(safeUrl(r.official_url))}" target="_blank" rel="noopener noreferrer" aria-label="Open official website for ${esc(r.name)} in a new tab">Official website ↗</a>
      </div>
    </article>`;
  }
  function updateQueryString(state) {
    const url = new URL(window.location.href);
    ["q","category","access","sort"].forEach(k => url.searchParams.delete(k));
    if(state.q) url.searchParams.set("q",state.q);
    if(state.category!=="all") url.searchParams.set("category",state.category);
    if(state.access!=="all") url.searchParams.set("access",state.access);
    if(state.sort!=="recommended") url.searchParams.set("sort",state.sort);
    window.history.replaceState(null,"",url.toString());
  }
  function render() {
    const state = getState();
    const filtered = sorted(resources.filter(r=>matches(r,state)),state.sort);
    fields.results.innerHTML = filtered.map(resourceCard).join("");
    fields.count.textContent = `Showing ${filtered.length} of ${resources.length} resources`;
    fields.empty.hidden = filtered.length > 0;
    fields.chips.querySelectorAll("button[data-category]").forEach(btn => {
      btn.setAttribute("aria-pressed", String(btn.dataset.category === state.category));
    });
    updateQueryString(state);
  }
  function detail(resource) {
    const group = accessGroup(resource.access);
    const rows = [
      ["Field",resource.category],["Access terms",resource.access],["Known limitations",resource.limitations],
      ["Integration",resource.integration],["Research tags",(resource.tags||[]).join(", ")],
      ["Verification date",resource.verified_on || "Not recorded"],
      ["Official source",resource.official_verification_url || resource.official_url],
      ["Catalog priority",resource.priority || "Not assigned"]
    ];
    fields.detail.innerHTML = `<span class="access-pill ${group}">${accessLabel[group]}</span>
      <h2 id="dialogTitle">${esc(resource.name)}</h2><p>${esc(resource.purpose)}</p>
      <dl>${rows.map(([k,v])=>`<div class="detail-info"><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>
      <p><strong>Reminder:</strong> Free access does not automatically permit bulk copying, clinical use, or commercial redistribution. Follow the provider's current terms.</p>
      <div class="dialog-actions"><a class="primary-button" href="${esc(safeUrl(resource.official_url))}" target="_blank" rel="noopener noreferrer">Visit official resource ↗</a><button class="secondary-button" type="button" id="copyResource">Copy resource link</button></div>`;
    const copy = $("#copyResource");
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(resource.official_url);
        copy.textContent = "Copied!";
      } catch {
        copy.textContent = "Select URL above to copy";
      }
    });
    if (typeof fields.dialog.showModal === "function") fields.dialog.showModal();
    else fields.dialog.setAttribute("open","");
  }
  function reset() {
    fields.search.value = "";
    fields.category.value = "all";
    fields.access.value = "all";
    fields.sort.value = "recommended";
    render();
    fields.search.focus();
  }
  function applyUrl() {
    const p = new URLSearchParams(window.location.search);
    fields.search.value = p.get("q")||"";
    if ([...fields.category.options].some(o=>o.value===p.get("category"))) fields.category.value=p.get("category");
    if ([...fields.access.options].some(o=>o.value===p.get("access"))) fields.access.value=p.get("access");
    if ([...fields.sort.options].some(o=>o.value===p.get("sort"))) fields.sort.value=p.get("sort");
  }
  async function init() {
    $("#year").textContent = new Date().getFullYear();
    try {
      const response = await fetch("data/resources.json",{cache:"no-store"});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const json = await response.json();
      if (!Array.isArray(json.resources)) throw new Error("Invalid catalog structure");
      resources = json.resources.filter(r=>r&&r.id&&r.name&&r.official_url);
      $("#heroCount").textContent=String(resources.length);
      const cats=[...new Set(resources.map(r=>r.category))].sort((a,b)=>a.localeCompare(b));
      $("#heroCategories").textContent=String(cats.length);
      cats.forEach(cat=>{
        const option=document.createElement("option");
        option.value=cat;option.textContent=cat;
        fields.category.append(option);
      });
      const categories=[{category:"all",count:resources.length},...cats.map(category=>({category,count:resources.filter(r=>r.category===category).length}))];
      fields.chips.innerHTML=categories.map(({category,count}) => `<button type="button" class="chip" data-category="${esc(category)}" aria-pressed="false">${esc(category==="all"?"All resources":category)} <span>${count}</span></button>`).join("");
      applyUrl();
      render();
    } catch(e) {
      console.error("Resource directory initialization failed",e);
      fields.error.hidden = false;
      fields.count.textContent = "Resource catalog unavailable";
    }
  }
  [fields.search,fields.category,fields.access,fields.sort].forEach(el=>{
    el.addEventListener(el===fields.search?"input":"change",render);
  });
  fields.chips.addEventListener("click",e=>{
    const chip=e.target.closest("button[data-category]");
    if (!chip) return;
    fields.category.value=chip.dataset.category;
    render();
  });
  fields.results.addEventListener("click",e=>{
    const btn=e.target.closest("button[data-detail]");
    if (!btn) return;
    const resource=resources.find(r=>r.id===btn.dataset.detail);
    if (resource) detail(resource);
  });
  document.querySelectorAll(".workflow-link").forEach(btn=>btn.addEventListener("click",()=>{
    fields.search.value=btn.dataset.query||"";
    fields.category.value=btn.dataset.category||"all";
    fields.access.value="all";
    render();
    $("#directory").scrollIntoView({behavior:"smooth"});
    fields.search.focus({preventScroll:true});
  }));
  $("#reset").addEventListener("click",reset);
  $("#emptyReset").addEventListener("click",reset);
  $("#closeDialog").addEventListener("click",()=>fields.dialog.close());
  fields.dialog.addEventListener("click",e=>{if(e.target===fields.dialog) fields.dialog.close()});
  document.addEventListener("keydown",e=>{
    if(e.key==="/"&&!["INPUT","TEXTAREA"].includes(document.activeElement.tagName)&&!fields.dialog.open){
      e.preventDefault();fields.search.focus();
    }
  });
  window.addEventListener("popstate",()=>{applyUrl();render()});
  init();
})();
