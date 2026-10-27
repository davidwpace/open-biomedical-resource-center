# Open Biomedical Resource Center — Discovery and AI Integration

Updated 2026-10-27.

## Philosophy

Visitors may find this resource center using ChatGPT, Gemini, Claude, Copilot, search engines or their own private agent. The center should be **provider agnostic**: it offers reliable, easy-to-read public metadata and official source links, rather than requiring use of a proprietary built-in AI.

We prioritize making resources useful to **humans and their agents** before implementing another conversation interface. The website benefits-first headline and plain-language content should remain accessible to everyone.

## Current discoverability endpoints (static GitHub Pages)

Public project base (once GitHub Pages deployment succeeds):

`https://davidwpace.github.io/open-biomedical-resource-center/`

- **Public JSON metadata:** `data/resources.json`. Returns all 42 resource records; filter on the client. No key, search endpoint, backend, authentication, or personalized recommendations. Resource data and descriptions are editorial, not scientific validations.
- **Plain HTML directory:** `catalog.html`. All 42 resource summaries appear in the HTML itself without JavaScript, suitable for search indexing and readers that cannot execute JavaScript. Each has an anchor (resource ID).
- **For AI assistants:** `agent-access.html`. Plain-language use, API example and limitations.
- **Optional llms.txt:** `llms.txt`. Provides links for clients that look for or are provided this file, **not** a universally adopted search-crawler standard and not an instruction hierarchy overriding users or source policies.
- **Read-only OpenAPI:** `openapi.json`. Describes ONLY `GET /data/resources.json`. It is not an executable search service, hosted model, MCP server, or Agent2Agent endpoint.
- **XML sitemap:** `sitemap.xml`. Lists stable public pages; can be manually submitted to search engines by a verified site owner.
- **Semantic markup:** homepage `WebSite` / `CollectionPage` and catalog `DataCatalog` / `Dataset` describing our own curated metadata, **not** asserting ownership or licenses over external biomedical datasets.
- **Source repo:** https://github.com/davidwpace/open-biomedical-resource-center

Because this is a GitHub Pages **project** site under a path prefix, bots that look only at domain-root paths like `https://davidwpace.github.io/llms.txt` may not find the project-level file automatically. We publish links in HTML and README and can use a custom domain later. A `robots.txt` in a project subdirectory would NOT set crawl policy for the host root, so avoid representing a project-local robots file as globally effective.

## Agent onboarding (minimal)

1. Read or retrieve `data/resources.json`.
2. For each relevant entry, use `name`, `purpose`, `tags`, `category`, `access`, `limitations`, `official_url`, `verified_on`.
3. Select official links relevant to a user query; do not assume an external URL can be consumed by an agent connector without independent user consent or provider support.
4. Distinguish publicly viewable materials, licensed noncommercial models, computational costs, controlled-access human data, and commercial research products.
5. Tell the user what is known, what remains hypothetical, and where independent biological or clinical validation would be required.
6. Cite the original provider and review current primary sources if possible; never claim a medical intervention is effective based solely on this directory.

## Future integrations (optional, not yet live)

### Search / detail MCP server

A **real remote MCP server** would need a running HTTP endpoint accepting protocol requests, not a JSON document hosted on static Pages. If demand warrants it, a small serverless worker could expose read-only tools:

- `search_resources({query, category?, access?})` — filter catalog records.
- `get_resource({id})` — retrieve a stable record and provider provenance.
- `list_research_paths()` — help find linked research workflows.

Controls: strict rate limits, input limits, HTTPS, Origin validation, repository-backed immutable version or ETag, no PHI, no scraping paid data, audit policy, no unverifiable clinical claims, independent reviews.

### Agent2Agent (A2A) server

A2A Agent Cards describe a **live remote agent**, its protocols and endpoints. Do not publish a false `.well-known/agent-card.json` claiming capabilities we do not operate. A real A2A service may be added later if agent-to-agent collaboration provides clear user benefit.

### Search engine visibility

Web pages and Google-friendly structured data improve crawlability, not guaranteed ranking or model indexing. Public links from reputable communities, authentic content, descriptive titles, site ownership verification and a submitted sitemap are likely more useful than keyword stuffing. Do not promise AI assistants will automatically ingest or recommend this site.

## Maintenance

- Update the `resources.json` dataset first, then rebuild `catalog.html` as HTML static output to avoid stale listings.
- Validate `sitemap.xml` and discovery files in CI.
- Follow original source owners' terms; never redistribute third-party databases or model weights without their permissions.
- Keep project public, without patient records, keys or sensitive user inputs.
