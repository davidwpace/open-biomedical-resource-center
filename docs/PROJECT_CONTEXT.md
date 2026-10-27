# Project context — portable handoff

**Project:** Open Biomedical Resource Center  
**Repository:** https://github.com/davidwpace/open-biomedical-resource-center  
**Start date:** October 27, 2026

## Origin
The project grew from an investigation of BrainXell's New Approach Methodologies (NAMs) and a search for free biological research tools. Its broader goal is a public discovery hub for researchers, students, independent investigators, patient advocates, and AI research assistants.

The project is **not** specific to any individual's cancer case, despite the historical research motivation. Keep case-specific notes, clinical records, identifiers, diagnoses, and recommendations out of the public repository.

## Core mission
Help people find, understand, compare, and combine trustworthy biomedical resources, including:
1. Human cell models and alternatives to animal testing.
2. Genomics, proteomics, transcriptomics, and molecular pathways.
3. Drug discovery and genetic variant interpretation.
4. Computational biology and virtual laboratories.
5. Literature, clinical trials, and learning.
6. Imaging and pathology.
7. Data analysis, computing, and website infrastructure.

Initial catalog: **42 records in `data/resources.json`**, grouped into 7 research fields. The data file is the source of truth. The original human-readable directory and blueprint are preserved in `docs/`.

## MVP decisions
- Public, readable, mobile-first static website hosted for free when GitHub Pages is enabled.
- No backend, tracking, accounts, payments, or client-private data.
- Search and category/access filters, helpful caveats, official links, recorded verification dates.
- Preset discovery workflows (not AI-generated treatment recommendations).
- No premature API mashups, autonomous experiments, unverified clinical conclusions, or large-scale scraping.
- Original code MIT; third-party resource licensing unaffected.

## Recent resource addition

October 27, 2026: included Hi-TPH, published October 26 in *Nature Computational Science*, as a linked, noncommercial TCR–pHLA research dataset and model suite (see `docs/HI_TPH_RESEARCH_PROFILE.md`). We did **not** fork or copy the original project. Author-reported model improvements remain distinct from clinical efficacy.

## Later phases, after review
- Schema validation and editorial workflow improvements.
- Link-health checks that comply with source terms and rate limits.
- Dedicated searchable resource pages / SEO.
- Data exports, research workflow composition, and supported APIs with provenance.
- Contributions and responsible moderation.
- Optional provenance-aware knowledge graph and federated interoperability.
- Private clinical applications, **if ever implemented**, must remain in a separate, properly governed system.

## Working agreement for future AI agents / Codex
1. Inspect the repository and read `README.md`, `docs/SOURCE_POLICY.md`, and `docs/WEBSITE_BLUEPRINT.md` before modifying anything.
2. Make incremental, tested changes and maintain the existing public-data-only scope.
3. Do not imply that catalog access equals permission to use an API or dataset.
4. Do not overwrite handoff documentation, alter existing IDs, or claim verification without checking.
5. Document limitations and link to official sources; separate hypotheses from evidence.
6. Prefer changes with clear user benefit over complex architecture.
7. Never commit PHI, personal clinical data, API tokens, or private research artifacts.

## Practical next step
Enable GitHub Pages from `main` / `(root)` via repository Settings → Pages. Verify the deployed URL before advertising it as live. Then test search on mobile, evaluate readability, and propose improvements using GitHub Issues.
