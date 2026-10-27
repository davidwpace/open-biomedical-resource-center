# Resource Center Website — MVP blueprint

## Mission
Build a public, mobile-first searchable directory connecting researchers, students, caregivers, patient advocates and AI agents to credible *free or clearly cost-labeled* biomedical research resources. Broad biomedical scope, not a patient-specific clinical dashboard. Start with the bundled `resources.json` as the source of truth.

## First release (MVP)
- Search across name, description and tags; case-insensitive.
- Filter by category, access class (free / mixed / commercial educational), and priority.
- Resource cards show purpose, access/limitations, official link and verification date.
- Resource detail pages show appropriate use cases, data/API availability, official citation, provenance and known restrictions.
- Preset workflows: Learning NAMs, Sarcoma/rare-cancer discovery, Target hypothesis, Virtual lab, Clinical-trial evidence, Publish findings.
- Clear distinction between public data, restricted data, free code, compute quotas and commercial laboratory services.
- Visible “research & education; not medical advice” warning where necessary.
- Community submission form can initially open a GitHub issue (manual editorial approval); no account backend in v1.
- Accessible responsive design; keyboard navigation; WCAG-friendly contrast and text.

## Design/content approach
Simple modern light UI, with category navigation, search-first hero, compact cards, “free access” status in plain text, no deceptive ratings, and source links. Evidence and verification should be auditable; classify research source versus tools/services. No need for AI assistant or live API integration in phase one.

## Low-cost build
Recommended: TypeScript + Vite + React for a static SPA, using resources.json locally. Alternatively static Astro for good SEO and individual resource pages. Publish with GitHub Pages (public repo) or Cloudflare Pages free tier. Use GitHub Issues for submissions and GitHub Actions for link checks. Build in a new standalone repository, keeping case-specific files and PHI elsewhere.

## Data discipline
- Keep `resource` as the unit of data; never equate tool with experiment or published evidence.
- Strict unique stable ids; record verification date and official source.
- All links must point to external official properties, no ungrounded claims.
- Maintain resource owners' attribution and licensing; do not bulk mirror papers, site text or protected data.
- Track separate badges/metadata: access, licensing, API, clinical applicability, validation and compute needs.
- Hide unsupported claims; use an explicit "unknown" state.
- New submissions require source citation, content review, and confirmation before listing.
- Do not put any identifiable clinical data in the public repository or hosted app.

## Phase two
Add deep-link curated searches, saved workflow collections and resource comparison. Only later evaluate live federated APIs with rate limiting, caching, provenance and licensing review. A restricted/private patient-data component, if ever built, must be separate with explicit informed consent and robust security design.

## Suggested repository structure
```
biomedical-resource-center/
  README.md
  data/resources.json
  src/
  public/
  docs/WEB_BLUEPRINT.md
  docs/SOURCE_POLICY.md
  .github/workflows/check-links.yml
```

## Acceptance criteria
1. Every bundled resource appears once and can be filtered by category and access status.
2. Search can find tools by name and domain tags, e.g., “neurons”, “sarcoma”, “model”, “trial”.
3. Free-vs-paid notes are always visible, not hidden behind a click.
4. On mobile, resource cards are readable and launch official links clearly.
5. All records display provenance link and date.
6. Zero actual patient-identifying information appears in source control or built assets.
