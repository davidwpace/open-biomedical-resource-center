# Open Biomedical Resource Center

**Discover tools. Connect knowledge. Advance research.**

A public, mobile-friendly directory of biomedical research resources, including New Approach Methodologies (NAMs), cancer genomics, drug discovery, cellular simulations, literature, clinical trials, imaging, and open analysis software.

**Status:** First static-site MVP • **Seed catalog:** 43 resources across 7 areas • **Original catalog checked:** October 27, 2026 • **Latest addition:** November 6, 2026.

## Publication safety

**Active since November 6, 2026:** GitHub Actions validates the source catalog,
discovery pages, JavaScript syntax, privacy warnings and internal links before
deploying a deliberately allowlisted static site artifact. The deployment job
requires a successful validation job, and the latest verified deployment was
[run #42172821542](https://github.com/davidwpace/open-biomedical-resource-center/actions/runs/42172821542).
Pull requests are validated without publishing.

The `PAGES_ACTIONS_READY=true` repository variable acts as a release switch.
The `main` branch is **not yet protected**; the repository owner can add a rule
requiring the exact `Catalog & syntax checks` status before merging, to stop
unreviewed or failing changes reaching `main`. See
[docs/PUBLISHING_SAFETY.md](docs/PUBLISHING_SAFETY.md) for the remaining
hardening instructions. Do not commit sensitive records or credentials.

## Scientific Review Panel — public pilot

The [open review invitation](review.html) accepts source-backed challenges and reviewer interest through two public GitHub Issue forms. The structured review criteria distinguish original citation checking, methodological assessment, adversarial evidence searches, translational safety, and reproducibility/education. The new `scripts/review_gate.py` enforces recorded human editorial review with per-chapter evidence locators before **new** `editorial_status: approved` articles can publish. Clinical interpretations additionally require a separate independent expert-review record. The two legacy historic stories remain accessible without retrospective claims of external peer review.

**Current limitation:** The five AI review roles are defined but NOT being run as five independent model services. Automated metadata checks do not authenticate expert credentials, prove scientific validity, or constitute journal peer review. See [Scientific Review Panel policy](docs/SCIENTIFIC_REVIEW_PANEL.md).

## Preview and hosting

The site is intentionally **HTML + CSS + JavaScript with no build dependencies**.

- Open [index.html](index.html) with a local HTTP server, for example `python3 -m http.server 8000` from the repo root, then visit `http://localhost:8000`. (Opening `index.html` as a `file://` URL may block loading the JSON data.)
- **GitHub Pages:** Publishing is already configured through **GitHub Actions**. The confirmed deployment URL is https://davidwpace.github.io/open-biomedical-resource-center/. Use **Actions → Validate public directory** to inspect validation and deployment history; do not switch back to branch publishing unless intentionally rolling back.
- This is a public directory. It does not require a backend, account, cookies, analytics, or personal information.

## AI and search-engine discovery (provider agnostic)

The public catalog can be read by **ChatGPT, Claude, Gemini, Copilot, web search, coding agents, or other user-chosen assistants** with appropriate web access; none of them is required or officially integrated. No paid model backend or agent-specific account is needed to read this directory.

- **All resource details as accessible HTML:** [catalog.html](catalog.html)
- **Public catalog JSON:** [data/resources.json](data/resources.json) · [direct raw GitHub JSON](https://raw.githubusercontent.com/davidwpace/open-biomedical-resource-center/main/data/resources.json)
- **Instructions for other agents:** [agent-access.html](agent-access.html)
- **Optional AI navigation:** [llms.txt](llms.txt) (an emerging convention, not a promise of indexing)
- **Read-only OpenAPI description:** [openapi.json](openapi.json) (static GET endpoint only)
- **Search sitemap:** [sitemap.xml](sitemap.xml)
- **Design limitations and integration roadmap:** [docs/AI_DISCOVERY.md](docs/AI_DISCOVERY.md)

The site includes machine-readable Schema.org metadata for the **directory's own catalog**, not a claim of ownership over providers' biomedical datasets.

**Important:** A static JSON file is **not** an MCP server or Agent2Agent service. There is no tool-calling backend, chat service, dynamic search endpoint, or clinical analysis service. We may build a genuine, safely hosted, read-only MCP server later if demand warrants one. Discovery is possible, but automatic indexing or recommendation by any individual AI provider is not guaranteed.

Because GitHub Pages uses a project subpath, `llms.txt` lives below `/open-biomedical-resource-center/`, not automatically at the host domain root. The HTML and README link to it explicitly. Search Console ownership and sitemap submission are separate, optional launch steps.

## Start here: beginner tool finder, landmark stories and safe contributions

**The first click is now simple:** [Find my starting tool](start.html). People choose what they already know (question, condition, gene, molecule, imaging, experimental data, or interest in helping) and one research goal. The site recommends **one resource**, gives the reason, a first verification task, and a methodological limitation. No personal data input or AI subscription.

- [Live tool finder](https://davidwpace.github.io/open-biomedical-resource-center/start.html)
- [Routing data](data/tool_routes.json) (7 situations / 14 paths, all linked to IDs in the 43-resource catalog)
- [Discovery story archive](stories.html): historical landmark stories about penicillin and insulin, plus the more detailed BRAF-melanoma walkthrough
- [Story metadata](data/stories.json): editorial review dates, historical event years, cited institutions, linked modern resource and a mini source-check task
- [Start a safe public contribution](contribute.html), or [read the public-only policy](CONTRIBUTING.md)
- [Live contribution hub](https://davidwpace.github.io/open-biomedical-resource-center/contribute.html)

**Important distinction:** The story publication date does not imply that the historical finding happened recently. External data and medical conclusions require independent review; the challenge tasks are educational and do not run patient-specific experiments. The public GitHub submission forms **must never** receive medical cases, images, lab results, private records or identifiable/indirectly identifying details.

We aim for concise text and clear calls to action on mobile, so beginners can focus on the science instead of learning navigation jargon. More accurate story pages are added through editorial review, not automatic AI news publication.

## Try the BioDiscovery Lab (free interactive prototype)

A visitor can investigate a documented **BRAF V600 melanoma** signaling example in a mobile-friendly guided page: [BioDiscovery Lab 001](lab/braf-melanoma.html). It includes a qualitative BRAF→MEK→ERK schematic, four links to scientific evidence sources, self-marked checkpoints and a shareable/downloadable Markdown evidence report.

- Published address after Pages deployment: https://davidwpace.github.io/open-biomedical-resource-center/lab/braf-melanoma.html
- Source and evidence boundaries: [docs/BIODISCOVERY_LAB_001.md](docs/BIODISCOVERY_LAB_001.md).
- It is **not** an experimental drug-discovery engine, quantitative simulation or personalized medical tool. No DepMap CRISPR results are calculated or imported by this demo.
- No API key, AI subscription, user account, or backend required. Visitors can paste the report into their own AI assistant.

## What the site can do

- Search name, description, tags, and access notes.
- Filter by seven research disciplines and by free / limited / commercial access.
- Sort resources, inspect official source and verification date, and open official websites.
- Share a filtered search with URL parameters.
- Browse guided discovery paths for cell models, cancer biology, drug targets, and virtual experiments.
- Suggest additional tools using GitHub Issues (editorial review required).

## Repository contents

```
index.html                      Static website
assets/styles.css               Responsive design
assets/app.js                   Directory rendering, filters, research pathways
data/resources.json             Source-of-truth catalog (43 records)
docs/RESOURCE_CATALOG.md       Human-readable initial catalog
docs/WEBSITE_BLUEPRINT.md      MVP requirements and roadmap
docs/SOURCE_POLICY.md          Access labels, provenance, review policy
docs/PROJECT_CONTEXT.md        New-chat / Codex handoff and decisions
docs/WORKFLOWS.md              Evidence-aware interdisciplinary research workflows\ndocs/AI_DISCOVERY.md           Agent discovery conventions and integration roadmap
docs/HI_TPH_RESEARCH_PROFILE.md Verified TCR–pHLA ML research resource guide
scripts/validate_catalog.py    Offline data-quality checks
.github/ISSUE_TEMPLATE/        Community suggestions
```

## Recent addition

**Hi-TPH (October 27, 2026):** A peer-reviewed TCR–peptide–HLA binding dataset and protein language model benchmark. [Original repository](https://github.com/Jiadong001/Hi-TpH) · [Paper](https://doi.org/10.1038/s43588-026-01073-y) · [Research profile](docs/HI_TPH_RESEARCH_PROFILE.md). Publicly accessible under noncommercial conditions; predicted binding is not a validated cancer treatment.

## Contribute a resource

[Create a resource suggestion](https://github.com/davidwpace/open-biomedical-resource-center/issues/new) with its official website, purpose, access limits, licensing information, and evidence of current availability.

Do not submit identifiable health records, protected information, proprietary documents, or confidential tokens. Contributions are editorially reviewed before inclusion.

## Data and safety

This project is for **research discovery and education**, not medical advice, diagnostic testing, clinical decision-making, or a validated in silico experiment. A directory listing is **not** an endorsement, scientific validation, or warranty of suitability.

Free-to-view is not necessarily free-to-download, free-to-compute, or free-to-reuse commercially. Each original provider's licenses, terms, attribution requirements, access controls, and clinical/research restrictions remain in force. Listings may become outdated after their recorded check date.

The directory itself contains **no patient records** and should remain separate from clinical case management and any privacy-sensitive system.

## Development

Run the data check:

```sh
python3 scripts/validate_catalog.py
```

The website avoids third-party runtime dependencies by design. Changes can be proposed via pull requests. Keep stable resource IDs, verify additions against official documentation, update `verified_on` only when actually rechecked, and follow [the source policy](docs/SOURCE_POLICY.md).

## License

Original source code is offered under the [MIT License](LICENSE); third-party research resources and their content are **not** relicensed here. Curated metadata may include resource names and descriptions whose rights remain with their respective owners. See [SOURCE_POLICY.md](docs/SOURCE_POLICY.md) for reuse and provenance details.
