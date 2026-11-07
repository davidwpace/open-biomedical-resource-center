"use strict";
(() => {
  const steps = Array.from(document.querySelectorAll(".lesson-step"));
  if (!steps.length) return;
  const back = document.getElementById("step-back");
  const next = document.getElementById("step-next");
  const status = document.getElementById("progress-label");
  const bar = document.getElementById("progress-track");
  const fill = document.getElementById("progress-fill");
  const task = document.getElementById("research-task");
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const choicesMade = new Array(steps.length).fill("");
  let index = 0;
  if (!back || !next || !status || !bar || !fill || !task) return;
  function focusStep(node, headingSelector) {
    node.scrollIntoView({behavior: motion.matches ? "auto" : "smooth", block:"start"});
    const h = node.querySelector(headingSelector);
    if (h) h.focus({preventScroll:true});
  }
  function show(i, focus) {
    index = Math.min(Math.max(0, i), steps.length - 1);
    steps.forEach((step, j) => { step.hidden = j !== index; });
    status.textContent = "Step " + (index + 1) + " of " + steps.length;
    bar.setAttribute("aria-valuenow", String(index + 1));
    fill.style.width = (100 * (index + 1) / steps.length) + "%";
    back.disabled = index === 0;
    next.textContent = index === steps.length - 1 ? "Try a real research tool ↓" : "Next clue →";
    if (focus) focusStep(steps[index], "h2");
  }
  steps.forEach((step, i) => {
    const answer = step.querySelector(".choice-feedback");
    step.querySelectorAll(".reason-choice").forEach((button) => {
      button.setAttribute("aria-pressed","false");
      button.addEventListener("click", () => {
        step.querySelectorAll(".reason-choice").forEach((b) => b.setAttribute("aria-pressed","false"));
        button.setAttribute("aria-pressed","true");
        choicesMade[i] = button.textContent.trim();
        if (answer) {
          const label = button.dataset.quality === "supported" ? "Evidence-aligned reasoning: " : "Needs a closer look: ";
          answer.textContent = label + button.dataset.feedback;
          answer.hidden = false;
        }
        const reveal = step.querySelector(".evidence-reveal");
        const toggle = step.querySelector(".reveal-evidence");
        if (reveal && toggle) { reveal.hidden = false; toggle.setAttribute("aria-expanded","true"); }
      });
    });
    const toggle = step.querySelector(".reveal-evidence");
    const evidence = step.querySelector(".evidence-reveal");
    if (toggle && evidence) {
      toggle.addEventListener("click", () => {
        const open = evidence.hidden;
        evidence.hidden = !open;
        toggle.setAttribute("aria-expanded", String(open));
        toggle.textContent = open ? "Hide the evidence ↑" : "Show what the evidence supports ↓";
      });
    }
  });
  back.addEventListener("click", () => show(index - 1, true));
  next.addEventListener("click", () => {
    if (index < steps.length - 1) show(index + 1, true);
    else focusStep(task, "h2");
  });
  show(0, false);

  function notes() {
    const title = document.getElementById("lesson-title")?.textContent.trim() || "Discovery lesson";
    const parts = ["OPEN BIOMED · LEARNING NOTES", title, "Educational source-checking exercise — not an experimental replication or clinical advice.", ""];
    steps.forEach((step,i) => {
      parts.push("STEP " + (i + 1) + ": " + (step.querySelector("h2")?.textContent.trim() || ""));
      parts.push("My choice: " + (choicesMade[i] || "Not selected"));
      parts.push("What the evidence supports: " + (step.querySelector(".evidence-reveal p")?.textContent.trim() || ""));
      const source = step.querySelector(".evidence-reveal a");
      if (source) parts.push("Source: " + source.href);
      parts.push("");
    });
    parts.push("MY SOURCE-CHECK TASK", task.querySelector(".task-panel p")?.textContent.trim() || "");
    const tool = task.querySelector("a.lab-primary");
    if (tool) parts.push("Tool: " + tool.href);
    parts.push("Caution: " + (task.querySelector(".lab-caution")?.textContent.trim() || ""));
    parts.push("These notes were created locally in my browser. No answer was submitted to the site.");
    return parts.join("\n");
  }
  const feedback = document.getElementById("report-status");
  const download = document.getElementById("download-notes");
  const copy = document.getElementById("copy-notes");
  if (download) download.addEventListener("click",() => {
    const blob = new Blob([notes()],{type:"text/plain;charset=utf-8"});
    const address = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = address; a.download = "my-discovery-learning-notes.txt";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(address), 1000);
    if (feedback) feedback.textContent = "Notes generated on this device. Nothing was uploaded.";
  });
  if (copy) copy.addEventListener("click",async() => {
    try {
      await navigator.clipboard.writeText(notes());
      if (feedback) feedback.textContent = "Learning notes copied.";
    } catch {
      if (feedback) feedback.textContent = "Copy unavailable in this browser. Use Download learning notes instead.";
    }
  });
  const aiButton = document.getElementById("copy-ai-prompt");
  const aiArea = document.getElementById("ai-prompt-text");
  const aiStatus = document.getElementById("ai-prompt-status");
  const aiDetails = document.getElementById("ai-manual");
  if (aiButton && aiArea) {
    aiButton.addEventListener("click", async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error("Clipboard not available");
        await navigator.clipboard.writeText(aiArea.value);
        if (aiStatus) aiStatus.textContent = "Lesson-specific prompt copied. Paste it into your own AI chat.";
      } catch {
        if (aiDetails) aiDetails.open = true;
        aiArea.focus(); aiArea.select();
        if (aiStatus) aiStatus.textContent = "Copy was unavailable. Your prompt is selected; use your device's Copy command.";
      }
    });
  }
})();
