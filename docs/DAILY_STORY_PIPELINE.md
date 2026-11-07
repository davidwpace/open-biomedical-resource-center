# Daily Discovery Stories — Automation and Editorial Controls

**Implemented:** November 7, 2026

## Two complementary automated processes

**1. Daily candidate research:** A recurring ChatGPT task named Discovery Story Research researches one historical or timely scientific discovery, compares original papers and trusted institutional sources, avoids duplicate topics, and prepares a clearly marked editorial draft. When connector access permits, it may create a GitHub Issue with public sources. It must not merge or publish unreviewed research.

**2. Daily published spotlight:** The existing validated GitHub Pages workflow now has a daily 8:17 AM America/Chicago schedule (plus existing push/PR/manual triggers). It renders a date-stamped [Today’s Discovery](https://davidwpace.github.io/open-biomedical-resource-center/today.html) page and machine-readable metadata from already published, source-linked stories. The generator has no model access, no API key, and no user data.

**Critical distinction:** Daily featured does NOT mean a breakthrough occurred that day, or that a NEW article will necessarily be published every morning. Initially, it rotates the two existing long-form landmark stories. The BRAF lab remains available in the library.

## Scientific approval gate

- New story candidates begin as clearly labeled drafts, preferably in GitHub Issues, not directly on public site pages.
- Verify original discoveries, dates, study designs, numerical claims, source accessibility, limitations and alternatives.
- Choose a public resource from the real catalog and provide one simple checkable task explaining why that tool fits.
- To publish: create a short story HTML page; include at least two official/original source URLs; add a matching entry in data/stories.json with editorial_status set to approved, reviewed_on, published_on, original_year, and the required chapter/tool fields.
- Do not add future stories to the static archive until their public pages are eligible; the release package intentionally excludes draft and future-dated story assets.
- A human owner/editor should review the research and merge through a tested GitHub pull request. A string reading approved in JSON cannot independently prove scientific credibility.
- Avoid private case data and PHI in GitHub or public stories.

## Automated release safety

- The daily GitHub Actions job executes catalog checks, source/story consistency checks, Python story tests and a strict allowlisted static-artifact build.
- The date-based feature rotates predictably among eligible stories and includes historical discovery and editorial-review dates.
- New entries with missing approval status fail; drafts and future-dated entries are excluded.
- The deployed website updates only after all required checks pass; a post-deploy HTTPS test checks published files.
- The manual GitHub Actions workflow_dispatch option remains available if a scheduled run is delayed.
- GitHub schedules are best-effort, can be delayed or occasionally dropped, and public-repository schedules can be disabled after 60 days of inactivity. See https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule.

## What is still needed for a genuinely new story EVERY day?

A **pre-reviewed publishing queue** containing enough stories for upcoming dates. The daily research task can help build that backlog; editors must validate sources before publication. Future work can render approved articles and their archive automatically from structured metadata and release them by scheduled date. Until then, the pipeline reliably provides a daily FEATURE from the existing library, not a guaranteed new independent breakthrough every day.

Other future enhancements: Atom/RSS feed, novice testing, source link monitoring, subject filters, and an explicit expert-review process. Evidence quality takes precedence over the publishing calendar.
