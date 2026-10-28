# BioDiscovery Lab 001 — BRAF V600 melanoma educational evidence journey

**Status:** MVP prototype, published as a static GitHub Pages asset when deployment succeeds.
**Preview path:** [lab/braf-melanoma.html](../lab/braf-melanoma.html)  
**Public URL:** https://davidwpace.github.io/open-biomedical-resource-center/lab/braf-melanoma.html
**Research source check:** October 27, 2026

## User benefit

A person with no coding or specialist biomedical training can open one page and:
1. Follow a five-chapter narrated story of how BRAF became a research clue and clinical target.
2. Switch between three qualitative BRAF → MEK → ERK pathway explanations.
3. Follow four independently verifiable scientific-resource links.
4. Mark sources they personally reviewed and export a Markdown evidence report to share with an AI.

The demo does not generate synthetic measurement results or claim to perform real biological experiments.

## Verified official sources

- **Open Targets, BRAF ENSG00000157764:** https://platform.opentargets.org/target/ENSG00000157764 — Target, pathway, and drug-development context. Protein kinase with MAP2K1 relationship.
- **DepMap Data Explorer 2:** https://depmap.org/portal/data_explorer_2/ — Public CRISPR gene-effect and disease/model-context exploration. Demo does **not** retrieve, run, or quantify DepMap experiments.
- **Human Protein Atlas, BRAF:** https://www.proteinatlas.org/ENSG00000157764-BRAF — Protein and RNA expression in normal and cancer tissues. Expression is not a safety prediction.
- **National Cancer Institute PDQ melanoma treatment:** https://www.cancer.gov/types/skin/hp/melanoma-treatment-pdq — BRAF V600E and V600K clinical contexts and BRAF–MEK inhibitor trial evidence. BRAF-inhibitor use should not be generalized to BRAF-wild-type melanoma.

## Evidence classification

| Element | Type | Limitation |
|---|---|---|
| BRAF→MEK→ERK flow chart | Simplified qualitative teaching schematic | Not a biological network model or dynamics simulation |
| BRAF V600 signaling explanation | Research-supported mechanistic concept | Does not cover all variants or cancers |
| Normal tissue expression | Linked published tissue atlas data | Not a clinically validated harm/side-effect estimate |
| DepMap checkpoint | External source/link and proposed analysis path | No data imported; no quantitative claims |
| NCI targeted-treatment background | Clinical evidence in specified melanoma contexts | Not a personalized treatment suggestion |
| Report/download | User-generated educational notes with source links | Not automatically externally validated or a new discovery |

## First-visitor narrated story (added after usability feedback)

The primary hero action now opens **"Let me show you how scientists found it"**—a five-chapter, one-step-at-a-time walkthrough with Back/Next buttons, visible chapter progress and the option to skip straight to the scientific sources.

| Chapter | Visitor question / historical finding | Actual source |
|---|---|---|
| 1. The question | Could a cancer have a recurring, actionable change? | Framing, not an original experimental finding |
| 2. The clue (2002) | Davies et al. identified BRAF somatic missense mutations in **66% of malignant melanoma samples examined** | [Nature 2002, DOI 10.1038/nature00766](https://doi.org/10.1038/nature00766) |
| 3. The mechanism | Some BRAF V600 mutations activate BRAF→MEK→ERK signaling in defined contexts | Simplified pathway diagram, not a quantitative simulation |
| 4. The clinical test (2011) | BRIM-3 randomized **675** advanced BRAF V600E melanoma patients to vemurafenib or dacarbazine; **48% vs 5% confirmed response rates** in original report | [NEJM 2011, DOI 10.1056/NEJMoa1103782](https://doi.org/10.1056/NEJMoa1103782) and [NCI PDQ](https://www.cancer.gov/types/skin/hp/melanoma-treatment-pdq) |
| 5. Your turn | Follow present-day public sources and document what you actually checked | Linked Open Targets, DepMap, Human Protein Atlas, NCI |

**Interpretation safeguards:**
- The original 2002 mutation proportion is *within the study samples*, not a present-day population estimate.
- The 2011 trial response rates are historical, **not cure, overall survival, or today's standard-of-care comparison**; the treatment was associated with side effects and resistance.
- The modern websites featured in the evidence section are for today's visitor, not a historical claim that 2002/2011 teams accessed them.
- The 48% and 5% bars reproduce the original publication's percentages; no synthetic patient values.
- Source-review progress now appears *after* the walkthrough, where it belongs.
- The exported report includes the 2002 and 2011 original publications, with limitations.

**Phone usability acceptance check:** First tap should be "Walk me through the discovery", then tap **Next** through five chapters, interact with the pathway when prompted, follow "Back to the narrated walkthrough", inspect the clinical trial comparison, and finally use "Explore the research tools." Test the Back button, chapter numbering and report on Android. Avoid forcing a modal tutorial.

## Technical design

- Self-contained page plus static `demo.css` and `demo.js`.
- No cloud runtime, API key, login, third-party JavaScript, cookies or tracking.
- Schematic buttons are native HTML radio controls and provide explanatory, labeled text.
- Native checkboxes update accessible progress status.
- Report is generated on demand in the visitor's browser; text is copied to clipboard or downloaded as Markdown.
- No localStorage or remote persistence. Do not enter patient information.
- Responsive mobile-first adaptations and `prefers-reduced-motion` consideration.
- Source URLs can be checked independently and are not proxy-imported.

## User acceptance test on phone

1. From the published URL, read the heading and tap **Start the investigation**.
2. Tap the three scenarios; compare narrative text and the changes in the pathway node colors.
3. Open each official source in a separate tab and return; manually check a source reviewed.
4. Confirm the progress reaches **4 of 4** only when all four checkboxes are selected.
5. Type a **non-sensitive** research question and tap **Download evidence report**; inspect the Markdown file.
6. Tap **Copy for my AI**; paste into a new Gemini or ChatGPT conversation. If clipboard permission is missing, the page should show text-selection fallback.
7. Verify readability on narrow mobile screens and that external links work.
8. Optional: disable JavaScript and confirm ordinary source links remain available (interactions intentionally require JS).

## Current known limits and future potential

- Proof of a useful and credible guided experience, **not** proof of a novel drug discovery.
- No real-time source retrieval, trial search, graph calculation, CRISPR scoring or model training.
- Next extension: small versioned sample from DepMap with explicit citation, licenses, methodology and an honest quantitative chart, only when the data are actually retrieved and validated.
- Later: cloud-hosted read-only MCP or API, subject to security/rate limiting and user permission.
- Add browser-based accessibility and mobile smoke tests to CI once a suitable test runner is configured.
