# BioDiscovery Lab 001 — BRAF V600 melanoma educational evidence journey

**Status:** MVP prototype, published as a static GitHub Pages asset when deployment succeeds.
**Preview path:** [lab/braf-melanoma.html](../lab/braf-melanoma.html)  
**Public URL:** https://davidwpace.github.io/open-biomedical-resource-center/lab/braf-melanoma.html
**Research source check:** October 27, 2026

## User benefit

A person with no coding or specialist biomedical training can open one page and:
1. Ask how a mutation could reveal a cancer vulnerability.
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
