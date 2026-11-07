"use strict";
(() => {
  const feedback = document.getElementById("copy-status");
  for (const button of document.querySelectorAll("[data-copy-target]")) {
    button.addEventListener("click", async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      if (!(target instanceof HTMLTextAreaElement)) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
        await navigator.clipboard.writeText(target.value);
        if (feedback) feedback.textContent = "Prompt copied. Paste it into the AI assistant you choose.";
      } catch {
        target.focus(); target.select();
        if (feedback) feedback.textContent = "Copy is unavailable. The prompt is selected—use your device's Copy command.";
      }
    });
  }
})();
