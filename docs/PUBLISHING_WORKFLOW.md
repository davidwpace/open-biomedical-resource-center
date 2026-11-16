# Publishing prepared articles

The public home for the collection is [All articles](https://davidwpace.github.io/open-biomedical-resource-center/articles.html).

## The everyday workflow

1. Prepare a source-linked discovery-story draft in the existing GitHub issue format.
2. The existing daily build imports complete, owner-authored drafts and publishes them for open review.
3. Read or listen from the article library. Use **Copy article**, **Share**, or **Download Markdown** to reuse a draft elsewhere.

Publication does not confer editorial approval or independent peer review. The approved-story feed and interactive-lesson gates retain their existing requirements. All-article RSS explicitly labels public drafts.

The author requested publication of all prepared articles on November 16, 2026. The initial collection contains eight discovery-story drafts, the prepared EoD manuscript subsection *Biological Compilation and the Amplified Individual*, and two existing educational stories.

## What is automatic

The existing workflow's main-branch, manual and daily runs call `scripts/sync_prepared_articles.py --fetch` before building. This reads public GitHub issues from this repository. Intake requires:

- owner-authored issue metadata and an EDITORIAL DRAFT title;
- exactly one structured story record with editorial status `draft`;
- a safe, unique slug, narrative chapters and HTTPS sources;
- a valid source reference for every chapter.

Existing curated records are retained. New intake records preserve a source-issue hash, preparation date, update timestamp and build-inclusion date. A build-inclusion date is not asserted to be a first-publication date. Other issues, patient files and internal research reports are outside this intake.

Scheduled runner execution is best effort. A failed validation prevents a new deployment; the prior live release remains available. GitHub Actions **Validate public directory → Run workflow → main** can run the same process on demand.

## What is available

- `articles.html`: one searchable collection, with clear publication/review status.
- Article pages: listening, copy, share, source links, annotations and print controls.
- `exports/<slug>.md`: reusable article text with sources and status.
- `exports/all-articles.md`: the complete text bundle.
- `article-links.txt`: every article URL.
- `articles-feed.xml`: all articles, including labeled public drafts.
- `feed.xml`: the existing approved/legacy-story feed, excluding review drafts.
- `data/publications.json`: the publication index and available source provenance.

Copy uses formatted HTML where the browser permits it, then plain text or selection-copy fallback. Share uses the device share sheet where available, then copies the canonical link. Listening uses browser speech support; actual voices depend on the reader's device.

## Reusing an article with another publisher

Open the article, select **Copy article**, paste into the destination editor, and inspect the preview before publishing there. The copy preserves the review notice and sources. Downloads provide a fallback when clipboard access is unavailable.

The current integration publishes to the author's existing website. It does not submit to OpenAI, post to a newsletter service, email subscribers, or obtain editorial acceptance from another publisher.

## Publication checks

The build checks intake behavior, review status, exports/feed consistency, internal links and source anchors. Browser QA exercises mobile layouts, searching, filtering, copying, share fallback and listening event wiring. The live HTTPS check verifies the deployed collection, new articles, feed and export bundle. These checks establish software/publication behavior, not independent scientific review.

