# Open Biomedical Resource Center

**Discover tools. Connect knowledge. Advance research.**

A public, mobile-friendly directory of biomedical research resources, including New Approach Methodologies (NAMs), cancer genomics, drug discovery, cellular simulations, literature, clinical trials, imaging, and open analysis software.

**Status:** First static-site MVP • **Seed catalog:** 41 resources across 7 areas • **Catalog last checked:** October 27, 2026.

## Preview and hosting

The site is intentionally **HTML + CSS + JavaScript with no build dependencies**.

- Open [index.html](index.html) with a local HTTP server, for example `python3 -m http.server 8000` from the repo root, then visit `http://localhost:8000`. (Opening `index.html` as a `file://` URL may block loading the JSON data.)
- **GitHub Pages:** Repository **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save**. The published URL is expected to have the pattern `https://davidwpace.github.io/open-biomedical-resource-center/` **only after GitHub Pages is enabled and the first deployment succeeds**.
- This is a public directory. It does not require a backend, account, cookies, analytics, or personal information.

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
data/resources.json             Source-of-truth catalog (41 records)
docs/RESOURCE_CATALOG.md       Human-readable initial catalog
docs/WEBSITE_BLUEPRINT.md      MVP requirements and roadmap
docs/SOURCE_POLICY.md          Access labels, provenance, review policy
docs/PROJECT_CONTEXT.md        New-chat / Codex handoff and decisions
docs/WORKFLOWS.md              Evidence-aware interdisciplinary research workflows
scripts/validate_catalog.py    Offline data-quality checks
.github/ISSUE_TEMPLATE/        Community suggestions
```

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
