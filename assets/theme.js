"use strict";
(() => {
  const root = document.documentElement;
  const key = "openbiomed-theme-v1";
  let stored = null;
  try {
    const value = window.localStorage.getItem(key);
    if (value === "dark" || value === "light") stored = value;
  } catch { /* Optional user preference storage may be blocked. */ }
  const system = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : {matches:false};
  const current = () => stored || (system.matches ? "dark" : "light");
  const apply = () => {
    root.dataset.theme = current();
    root.style.colorScheme = current();
    const btn = document.getElementById("color-theme-toggle");
    if (btn) {
      const next = current() === "dark" ? "light" : "dark";
      btn.textContent = (next === "dark" ? "☾ Dark mode" : "☀ Light mode");
      btn.setAttribute("aria-label", "Switch to " + next + " mode");
      btn.title = "Change the website color scheme";
    }
  };
  apply(); // Early enough to avoid a light-theme flash for dark-mode visitors.
  const makeButton = () => {
    if (document.getElementById("color-theme-toggle")) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "color-theme-toggle";
    button.id = "color-theme-toggle";
    button.addEventListener("click", () => {
      stored = current() === "dark" ? "light" : "dark";
      try { window.localStorage.setItem(key, stored); } catch { /* Persistence optional. */ }
      apply();
    });
    document.body.appendChild(button);
    apply();
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", makeButton, {once:true});
  else makeButton();
  if (system.addEventListener) system.addEventListener("change", () => { if (!stored) apply(); });
})();
