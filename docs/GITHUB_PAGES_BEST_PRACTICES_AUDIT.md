# GitHub Pages best-practice audit

**Reviewed:** 2026-10-27  
**Repository:** https://github.com/davidwpace/open-biomedical-resource-center  
**Expected Pages URL:** https://davidwpace.github.io/open-biomedical-resource-center/  
**Method:** Reviewed repository metadata/source, GitHub Actions history and deployment job logs, and current GitHub/Google primary documentation. This is a configuration/source review, **not** a completed live browser, screen-reader, Lighthouse or penetration test.

## Executive summary

**Recommendation:** Continue using GitHub Pages for the public read-only directory. Do not add a paid backend or a JavaScript framework simply for discoverability. Correct release gating, source-to-HTML generation, accessibility/performance testing and site-owner search verification before expanding into real MCP hosting.

**Confirmed today:**
- Public repository; default branch `main`; Pages enabled; no repository homepage URL set; no topics set.
- Approximate repository size reported by GitHub: 144 KB (not a measured site transfer size).
- Latest inspected Pages deployment run #40601256383: build, deployment, and reporting jobs all **successful**. Logs show evaluated URL `https://davidwpace.github.io/open-biomedical-resource-center/`.
- Latest inspected catalog has **42 records**. JavaScript directory, static `catalog.html`, public JSON, `openapi.json`, `llms.txt`, and sitemap exist.
- The `Validate public directory` workflow has completed successfully for the latest inspected repo revision.
- Repository-level **rulesets API reports `[]`**. GitHub's branch-protection endpoint returned 403 to the current integration, so branch protection **could not be confirmed**.
- The GitHub repository API reports `license.spdx_id = NOASSERTION`, although a file named `LICENSE` contains an MIT license statement followed by custom caveat text; confirm the intended legal treatment before presenting license claims broadly.
- Live site could not be independently loaded by this research environment. A successful deployment does not replace a real browser + status/headers check.

## Priorities

| Priority | Finding | Best-practice change | Acceptance criteria |
|---|---|---|---|
| P0 | **Build and deployment are independent of validation.** Publishing from `main` can proceed while the separate check fails. | Protect `main` with required passing checks and PR review, or switch to a custom Pages deployment workflow with `needs: validate`, restricted permissions and `github-pages` environment. | Intentionally malformed catalog cannot reach live site. |
| P0 | **No measured real-user page test.** Source and CI checks are not proof of live function. | Run manual mobile/desktop smoke tests and an automated browser smoke test against deployed site. | Home, catalog, JSON, AI access, copy/download, search and keyboard nav all function from public URL. |
| P1 | **Static `catalog.html` is generated separately from JSON.** CI checks that IDs/official links are in HTML, but cannot detect all stale descriptions or access fields. | Generate `catalog.html` deterministically from `data/resources.json` and fail CI if generated output differs. | A single source of truth; adding or correcting a resource updates all public presentation automatically. |
| P1 | **Publishing from repository root exposes more than site assets.** Public metadata is fine, but source/docs/test scripts are unnecessary in publication payload. | Consider deploying a built `dist/` artifact containing an explicit allowlist of public files via custom Pages Actions; no urgent migration for current public-only repo. | Pages artifact includes only intended public files; repository continues preserving source and documentation. |
| P1 | **Discoverability requires people-first content beyond just metadata.** | Verify site with Google Search Console and submit sitemap; add distinct useful resource/guide pages over time with helpful titles, relevant questions, citations, and original summaries. | Search Console can inspect sitemap and known URLs; new pages have meaningful metadata and unique content. |
| P1 | **A11y/performance still require measurement.** | Add axe/Playwright or equivalent browser accessibility checks and Lighthouse mobile/desktop review. | No major keyboard/contrast/label errors; no horizontal scrolling; essential directory accessible without JS via `catalog.html`. |
| P1 | **Third-party research data and licenses vary.** | Maintain source provenance, provider verification dates, license distinctions and medical evidence disclaimers. | Site does not imply free commercial rights or clinically proven efficacy; source updates tracked. |
| P2 | **GitHub repository metadata is sparse.** | Add an accurate repo description, topics such as `biomedical-research`, `research-resources`, `nams`, `open-science`, and set homepage URL *after live verification*. | Repository is clearly described and navigable from GitHub search and profile. |
| P2 | **Custom-domain strategy not yet decided.** | Optional memorable domain later; verify ownership via GitHub account settings, use correct DNS, enable HTTPS and update all canonical URLs, JSON-LD, sitemap and OpenAPI server URL together. | No split/duplicate canonical site; HTTPS enforced; ownership TXT record retained. |
| P2 | **GitHub Actions supply-chain hardening.** `actions/checkout@v4` uses a major tag rather than a full immutable commit SHA. | Keep least-privilege `permissions: contents: read` and pin third-party actions to audited full SHAs for stricter release integrity. | Workflow dependencies and permissions are reproducible and reviewed. |

## Current infrastructure: keep vs change

### Keep
- Static HTML/CSS/JS, direct relative asset paths, public JSON data, accessible HTML fallback.
- Project-site path-aware URLs: `/open-biomedical-resource-center/` rather than assumption of domain root.
- Zero client-side API secrets and no public patient-level data.
- `.nojekyll` for this static source.
- Descriptive plain-language messaging and direct links to original research providers.
- Machine-readable access via normal HTTP without forcing a specific assistant.

### Change before broad public launch
1. Gate production on completed validation. Two independently successful workflows are **not** a release gate.
2. Test published pages with a real browser and network request; record HTTP response codes and essential assets.
3. Make `catalog.html` generated from JSON; detect out-of-sync output in CI.
4. Ensure `main` changes are reviewed via pull requests and required checks; check actual branch rule availability before changing workflow.
5. Add basic automated accessibility and regression coverage.
6. Check repository license detection and avoid extending our code license to third-party data or authors' model weights.

### Improve as the directory grows
- Add genuine explanatory guides keyed to user problems and reliable sources; avoid thousands of thin or automatically rephrased SEO pages.
- Use a clean site-only publication artifact and remove unnecessary repository assets from Pages when switching to Actions.
- Consider a brand domain once stable and desirable; reserve migration work for when canonical paths are ready.
- Track broken links at modest intervals respecting providers' rate limits and Terms. Logs and link checks are not scientific verification.
- Consider versioned catalog snapshots, `ETag` handling and a real read-only MCP worker only when the benefit justifies upkeep.

## Release configurations

### Option A — least disruption (current stage)
Keep **Settings → Pages → Deploy from a branch → main → /(root)**. Adopt branch protection/ruleset for `main`, require the `Catalog & syntax checks` job (exact check name verified against Actions), require at least one review when collaborators join, disallow force-push/delete, and use short-lived feature branches/PRs. This protects changes before merge, but GitHub Pages still publishes from the branch after merge. **Avoid a settings lockout** by confirming a PR can pass the exact required check.

### Option B — production maturity
Choose **Settings → Pages → Source: GitHub Actions**. Use a build/validation job and a deploy job with `needs: build`, `permissions: contents: read, pages: write, id-token: write`, and a protected `github-pages` environment. Build an explicit `dist` artifact. Stop deployment when validation fails. **Do not switch source until the new deployment workflow is ready**, or there may be a temporary publish outage.

Official example: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Search/agent discovery specifics

- Google can render JavaScript but some agents cannot, so `catalog.html` should remain a complete HTML source with links, not only browser-rendered cards. https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Existing `sitemap.xml` is appropriate. Search Console submission is a discovery hint, **not** a ranking or indexing guarantee. https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- The `llms.txt` convention is optional; it is **not** evidence that Gemini, ChatGPT or other assistants will automatically discover or call our catalog.
- OpenAPI documents a static HTTP GET file; it is **not** an MCP endpoint. A real hosted MCP service would require backend execution, security, bounded inputs, provenance and rate limiting.
- For the current `github.io` project URL, a file at `/open-biomedical-resource-center/robots.txt` does not configure host-root `/robots.txt`. Prefer sitemap submission via Search Console and human-readable links.
- No AI assistant should claim it fetched a file or modified a registry without a real read/write confirmation.
- Prioritize research benefits to visitors over technical feature lists; describe biomedical conclusions and uncertainty accurately.

## Pages constraints

GitHub publishes static assets with optional build tooling. GitHub-documented limits currently include **1 GB published site size**, **100 GB/month soft bandwidth**, **10 builds/hour soft limit** (exception for custom Actions workflow builds), and **10-minute deployment timeout**. Recommended source-repo size is up to 1 GB. The current tiny directory is far below those thresholds, but they matter if model weights or large datasets are considered.

GitHub Pages is public-facing even when the source repository is private in plans that allow private repo Pages, and is inappropriate for hosting confidential patient records or sensitive transactions. No proprietary licensed datasets should be mirrored merely because the public directory lists them.

## Domain/HTTPS

Our project currently uses `https://davidwpace.github.io/open-biomedical-resource-center/`. No custom domain has been configured via `CNAME` in the inspected repository source; repo metadata currently does not expose a homepage URL. Before setting a custom domain, verify ownership in GitHub settings to reduce domain takeover risk; avoid wildcard DNS. GitHub Pages supports HTTPS and HTTPS enforcement. Then update canonical tags, sitemap URLs, JSON-LD and public API server URL to the new origin. Test redirection and preserve stable links.

References:
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://docs.github.com/en/actions/reference/security/secure-use
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
