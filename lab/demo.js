"use strict";
(() => {
  const $ = (id) => document.getElementById(id);
  const scenarios = Object.freeze({
    normal: {
      label: "USUAL SIGNALING",
      text: "In typical regulated contexts, BRAF relays upstream signaling through MEK and ERK. Feedback and cell context determine how strongly and when the pathway operates.",
      braf: "active", mek: "active", erk: "active", signal: "active"
    },
    mutant: {
      label: "BRAF V600 ALTERATION",
      text: "Certain BRAF V600 alterations can activate MAPK signaling with less dependence on the usual upstream control. This is one mechanism investigated in a defined subset of melanoma, not a general rule for every BRAF variant.",
      braf: "altered", mek: "altered", erk: "altered", signal: ""
    },
    inhibited: {
      label: "PATHWAY-TARGETED TREATMENT CONCEPT",
      text: "In clinically selected BRAF V600 melanoma, BRAF and MEK inhibitors can interrupt susceptible tumor signaling. This is a qualitative mechanism illustration: it cannot predict an individual's response, side effects, or resistance.",
      braf: "inhibited", mek: "inhibited", erk: "inhibited", signal: ""
    }
  });
  const citations = Object.freeze([
    {
      title: "Open Targets — BRAF target profile",
      url: "https://platform.opentargets.org/target/ENSG00000157764",
      claim: "BRAF (ENSG00000157764) is mapped to pathways, drug evidence, and related molecular information.",
      limitation: "Target associations do not independently prove clinical benefit."
    },
    {
      title: "DepMap — Data Explorer 2.0",
      url: "https://depmap.org/portal/data_explorer_2/",
      claim: "DepMap provides public cancer-model data suitable for exploring gene dependency hypotheses.",
      limitation: "No DepMap measurements were downloaded or independently analyzed in this demo."
    },
    {
      title: "Human Protein Atlas — BRAF",
      url: "https://www.proteinatlas.org/ENSG00000157764-BRAF",
      claim: "BRAF tissue and cellular expression can be inspected in normal human tissues.",
      limitation: "Normal expression cannot by itself establish medication safety."
    },
    {
      title: "National Cancer Institute — Melanoma Treatment (PDQ)",
      url: "https://www.cancer.gov/types/skin/hp/melanoma-treatment-pdq",
      claim: "Clinical studies support BRAF/MEK pathway-directed therapies in specified BRAF V600 melanoma contexts.",
      limitation: "Do not extrapolate evidence to untested mutations, cancer types, or individuals."
    }
  ]);
  function setScenario(mode) {
    const s = scenarios[mode] || scenarios.normal;
    $("scenarioLabel").textContent = s.label;
    $("scenarioText").textContent = s.text;
    const parts = ["signal","braf","mek","erk"];
    parts.forEach((part) => {
      const el = $("node-" + part);
      el.classList.remove("active", "altered", "inhibited");
      if (s[part]) el.classList.add(s[part]);
    });
  }
  document.querySelectorAll('input[name="mode"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      if (radio.checked) setScenario(radio.value);
    });
  });
  const reviews = Array.from(document.querySelectorAll("[data-review]"));
  function updateProgress() {
    const count = reviews.filter((item) => item.checked).length;
    $("completedText").textContent = count + " of " + reviews.length + " checkpoints reviewed";
    $("progress").setAttribute("aria-valuenow", String(count));
    $("progressFill").style.width = 100 * count / reviews.length + "%";
  }
  reviews.forEach((input) => input.addEventListener("change", updateProgress));
  function report() {
    const checked = reviews.filter((item) => item.checked).length;
    const mode = document.querySelector('input[name="mode"]:checked')?.value || "normal";
    const note = $("researchQuestion").value.trim();
    const out = [
      "# BioDiscovery Lab 001 — BRAF-mutant melanoma",
      "",
      "Source: Open Biomedical Resource Center",
      "https://davidwpace.github.io/open-biomedical-resource-center/lab/braf-melanoma.html",
      "Evidence links reviewed in site editorial process: October 27, 2026.",
      "My review progress: " + checked + "/" + reviews.length + " sources marked reviewed.",
      "Selected educational scenario: " + scenarios[mode].label,
      "",
      "## Research question",
      "How can molecular target evidence, cancer-model functional data, normal-tissue context and clinical studies be combined to examine the BRAF V600 melanoma example?",
      "",
      "## Known biology (conceptual)",
      "BRAF is part of a signaling chain involving MEK and ERK. Selected BRAF V600 alterations can drive dysregulated MAPK signaling. In certain BRAF V600 melanoma settings, BRAF and MEK inhibitors have clinical evidence.",
      "The pathway illustration is not a quantitative simulation or experimental measurement.",
      "",
      "## Source checkpoints"
    ];
    citations.forEach((source, index) => {
      const state = reviews[index]?.checked ? "Self-marked as reviewed" : "Not marked reviewed";
      out.push("", (index + 1) + ". " + source.title, "   Status: " + state,
        "   URL: " + source.url,
        "   Source-supported context: " + source.claim,
        "   Interpretation boundary: " + source.limitation);
    });
    out.push(
      "",
      "## Suggested reproducible investigation",
      "1. Confirm BRAF variant definitions and melanoma evidence in the original sources.",
      "2. Explore BRAF gene dependency in melanoma cell-line models using current DepMap releases.",
      "3. Stratify the comparison by verified BRAF mutation status, disease lineage and model quality; specify controls.",
      "4. Inspect BRAF expression across normal tissues, noting that expression is not toxicity evidence.",
      "5. Compare experimental-model findings with NCI clinical evidence only within the applicable patient populations.",
      "6. Record dataset versions, sample counts, analysis methods and conflicting findings before making a new claim.",
      "",
      "## Limitations",
      "- No DepMap measurements were retrieved or analyzed by this demo.",
      "- No new biomarker, drug response or therapeutic candidate was discovered.",
      "- The pathway switches illustrate mechanistic concepts, not predicted biological behavior.",
      "- This is educational research, not medical advice or a clinical decision tool.",
      "- Consult original providers for current data, licensing and source limitations.",
      "",
      "## Question to investigate next",
      note || "(Not supplied)",
      "",
      "You can give this report to your preferred AI assistant. Ask it to confirm which linked sources it actually accessed and separate recalled context from retrieved data."
    );
    return out.join("\n");
  }
  function say(message) {
    $("reportMessage").textContent = message;
  }
  function manualCopy(text) {
    $("reportText").value = text;
    $("fallback").hidden = false;
    $("reportText").focus();
    $("reportText").select();
  }
  $("selectReport").addEventListener("click", () => {
    $("reportText").focus(); $("reportText").select();
  });
  $("downloadReport").addEventListener("click", () => {
    const content = report();
    const url = URL.createObjectURL(new Blob([content], {type:"text/markdown;charset=utf-8"}));
    const link = document.createElement("a");
    link.href = url;
    link.download = "biomedical-evidence-lab-braf-melanoma.md";
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 3000);
    say("Your evidence report is ready. Check your browser's downloads.");
  });
  $("copyReport").addEventListener("click", async () => {
    const content = report();
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard not available");
      await navigator.clipboard.writeText(content);
      $("fallback").hidden = true;
      say("Copied the evidence summary. Paste it into your favorite AI assistant.");
    } catch {
      manualCopy(content);
      say("Automatic copying isn't available. Select the text below to copy it manually.");
    }
  });
  setScenario("normal");
  updateProgress();
})();
