# Open Biomedical Resource Center

**Discover tools. Connect knowledge. Advance research.**

A public, mobile-friendly directory of biomedical research resources, including New Approach Methodologies (NAMs), cancer genomics, drug discovery, cellular simulations, literature, clinical trials, imaging, and open analysis software.

**Status:** First static-site MVP • **Seed catalog:** 42 resources across 7 areas • **Catalog last checked:** October 27, 2026.

## Preview and hosting

The site is intentionally **HTML + CSS + JavaScript with no build dependencies**.

- Open [index.html](index.html) with a local HTTP server, for example `python3 -m http.server 8000` from the repo root, then visit `http://localhost:8000`. (Opening `index.html` as a `file://` URL may block loading the JSON data.)
- **GitHub Pages:** Repository **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save**. The published URL is expected to have the pattern `https://davidwpace.github.io/open-biomedical-resource-center/` **only after GitHub Pages is enabled and the first deployment succeeds**.
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
data/resources.json             Source-of-truth catalog (42 records)
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
