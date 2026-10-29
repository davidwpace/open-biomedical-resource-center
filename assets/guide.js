"use strict";
(() => {
  const $ = (id) => document.getElementById(id);
  const notice = $("guideNotice");
  const grid = $("choiceGrid");
  const goals = $("goalChoices");
  const stepOne = $("stepOne");
  const stepTwo = $("stepTwo");
  const result = $("result");
  let choices = [];
  let resources = [];
  let active = null;
  function element(tag, className, text) {
    const e = document.createElement(tag);
    if (className) e.className = className;
    if (text != null) e.textContent = text;
    return e;
  }
  function safeUrl(value) {
    try {
      const u = new URL(value, location.href);
      return ["https:","http:"].includes(u.protocol) ? u.href : "#";
    } catch { return "#"; }
  }
  function scrollToSection(section, focusId) {
    section.hidden = false;
    section.scrollIntoView({behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto":"smooth",block:"start"});
    const focus = $(focusId);
    if (focus) focus.focus({preventScroll:true});
  }
  function reset() {
    active = null;
    stepTwo.hidden = true;
    result.hidden = true;
    stepOne.hidden = false;
    notice.textContent = "Choose what you already know. If you only have a question, that's plenty.";
    scrollToSection(stepOne,"know-title");
  }
  function pickChoice(choice) {
    active = choice;
    goals.replaceChildren();
    choice.options.forEach((option) => {
      const button = element("button","goal-choice");
      button.type = "button";
      button.append(element("strong","",option.label),element("span","", "We'll choose one useful resource and a first action."));
      button.addEventListener("click",()=>showResult(option));
      goals.append(button);
    });
    stepOne.hidden = true;
    result.hidden = true;
    $("goal-title").textContent = "You know " + choice.label.toLowerCase() + ". What would you like to learn?";
    notice.textContent = "Good start. Just one more choice.";
    scrollToSection(stepTwo,"goal-title");
  }
  function showResult(option) {
    const resource = resources.find(x=>x.id===option.resource_id);
    if (!resource) {
      notice.textContent = "That tool could not be found in our catalog. Try another path.";
      return;
    }
    stepTwo.hidden = true;
    $("toolName").textContent = resource.name;
    $("toolWhy").textContent = option.why;
    $("firstAction").textContent = option.action;
    $("toolLimit").textContent = option.caution;
    $("toolTerms").textContent = "Provider access: " + resource.access + ". Catalog notes: " + resource.limitations;
    const a = $("toolLink");
    a.href = safeUrl(option.special_url || resource.official_url);
    a.textContent = (option.special_label || "Open "+resource.name) + " ↗";
    if (a.href.startsWith(location.origin) || a.href.includes("github.io/open-biomedical-resource-center")) {
      a.removeAttribute("target");
    } else {
      a.target="_blank";
    }
    notice.textContent = "You found a starting point. Nice work.";
    scrollToSection(result,"result-title");
  }
  $("startOver").addEventListener("click",reset);
  $("changeClue").addEventListener("click",reset);
  Promise.all([
    fetch("data/tool_routes.json").then(r=>{if(!r.ok)throw Error("Route data unavailable");return r.json();}),
    fetch("data/resources.json").then(r=>{if(!r.ok)throw Error("Catalog unavailable");return r.json();})
  ]).then(([routes,catalog]) => {
    if (!Array.isArray(routes.choices) || !Array.isArray(catalog.resources))throw Error("Data format error");
    choices = routes.choices;
    resources = catalog.resources;
    grid.replaceChildren();
    for (const choice of choices) {
      const button = element("button","choice");
      button.type="button";
      button.append(element("span","choice-icon",choice.icon),element("strong","",choice.label),element("span","",choice.sub));
      button.addEventListener("click",()=>pickChoice(choice));
      grid.append(button);
    }
  }).catch(() => {
    notice.textContent="The interactive guide is unavailable right now. You can still choose a discovery story or the full directory below.";
  });
})();
