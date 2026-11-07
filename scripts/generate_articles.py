#!/usr/bin/env python3
"""Build date-gated educational articles from editorially approved public records.

This code does not research, author, peer-review or approve discoveries. It
reuses source-reviewed content supplied in data/stories.json after the separate
editorial gate. GitHub is public; records here are not confidential embargoes.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

from generate_lessons import validate_lesson, update_sitemap
from render_daily_spotlight import LEGACY_PUBLISHED, available_stories
from review_gate import evaluate_story

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://davidwpace.github.io/open-biomedical-resource-center/"


def e(s: object) -> str:
    return escape(str(s), quote=True)


def article_page(story: dict) -> str:
    slug = story["slug"]
    if slug in LEGACY_PUBLISHED:
        raise ValueError("Preserve the already authored legacy story pages")
    problems = evaluate_story(story)
    if problems:
        raise ValueError("Invalid editorial approval: " + "; ".join(problems))
    validate_lesson(story, None)
    chapters = []
    sources = {x["id"]: x for x in story["sources"]}
    for n, chapter in enumerate(story["chapters"], start=1):
        source = sources[chapter["source"]]
        chapters.append(f'''<section class="story-chapter" aria-labelledby="chapter-{n}">
          <span class="story-num">{e(chapter["kicker"])} · {n}/{len(story["chapters"])}</span>
          <h3 id="chapter-{n}">{e(chapter["title"])}</h3>
          <p>{e(chapter["body"])}</p>
          <div class="takeaway"><strong>Here's the evidence limit:</strong> {e(chapter["takeaway"])}</div>
          <p class="chapter-source"><a href="{e(source["url"])}" rel="noopener noreferrer" target="_blank">
          Open supporting source: {e(source["label"])} ↗</a></p>
        </section>''')
    source_rows = "".join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["label"])} ↗</a> <small>{e(s.get("kind","Original or official source"))}</small></li>' for s in story["sources"])
    review = story["review"]
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(story["intro"])}">
<link rel="canonical" href="{BASE}stories/{slug}.html">
<script src="../assets/theme.js"></script><link rel="stylesheet" href="../assets/story.css">
<link rel="stylesheet" href="../assets/theme.css">
<title>{e(story["title"])} — Open Biomedical Resource Center</title></head>
<body><a class="skip" href="#main">Skip to research story</a>
<header class="bar"><a class="brand" href="../index.html">✳ OPEN BIOMED · RESOURCE CENTER</a>
<nav aria-label="Navigation"><a href="../learn.html">Interactive lessons</a><a href="../stories.html">All stories</a></nav></header>
<main id="main" class="container">
<section class="hero"><span class="eyebrow">REVIEWED EDUCATIONAL STORY · {e(story["original_year"])}</span>
<h1>{e(story["title"])}</h1><p>{e(story["intro"])}</p>
<div class="pill-row"><span class="pill">{e(story["topic"])}</span><span class="pill">Original sources</span><span class="pill">Public-source exercise</span></div>
<a class="main-cta" href="../learn/{slug}.html">Try the interactive investigation →</a></section>
<div class="intro-line"><strong>?</strong><span>{e(story["hook"])}</span></div>
<section class="story-box" aria-labelledby="story-title"><div class="story-head">
<span class="story-num">FOLLOW THE HISTORICAL EVIDENCE</span>
<h2 id="story-title">What did researchers actually find?</h2></div>
<div class="story-inner">{''.join(chapters)}</div></section>
<section class="lesson"><span class="story-num">ONE SOURCE-CHECKING TASK</span>
<h2>Take the next step yourself</h2><p><strong>Why {e(story["tool_title"])}?</strong> {e(story["tool_why"])}</p>
<div class="mission"><span class="mission-number">1</span><div><strong>Try this</strong><p>{e(story["tool_task"])}</p></div></div>
<p class="limit"><strong>Important boundary:</strong> {e(story["tool_limitation"])}</p>
<a class="main-cta" href="{e(story["tool_url"])}" target="_blank" rel="noopener noreferrer">Open {e(story["tool_title"])} ↗</a>
<details><summary>What should a careful reader find?</summary><p>{e(story["tool_answer"])}</p></details></section>
<section class="sources"><h2>Source trail and review status</h2><ol>{source_rows}</ol>
<p class="disclaimer">Historical discovery: {e(story["original_year"])} · Story source review: {e(story["reviewed_on"])}
· Website publication date: {e(story["published_on"])}. This is an editorially approved educational article,
not a claim of journal peer review or independently replicated clinical benefit.
<a href="{e(review["review_url"])}" target="_blank" rel="noopener noreferrer">Read public editorial review record ↗</a>.
Do not use this educational content as patient-specific medical advice.</p></section></main>
<footer class="footer"><a href="../learn.html">Explore the interactive lesson</a><a href="../review.html">Challenge the evidence</a>
<p>Public scientific education. Source availability and conclusions may change.</p></footer>
</body></html>'''


def append_archive_cards(index_html: str, approved_new: list[dict]) -> str:
    marker = '</section>\n<p class="disclaimer">'
    if marker not in index_html:
        raise ValueError("The story archive's insertion marker changed")
    cards = []
    for story in approved_new:
        slug = story["slug"]
        cards.append(f'''<article class="story-card"><span class="story-category">{e(story["topic"])}</span>
<div class="year">Original discovery {e(story["original_year"])} · Published {e(story["published_on"])}</div>
<h2><a href="learn/{slug}.html">{e(story["title"])}</a></h2>
<p>{e(story["intro"])}</p><a href="stories/{slug}.html">Read the source-backed story →</a></article>''')
    return index_html.replace(marker, "".join(cards) + marker, 1)


def render_articles(destination: Path, *, today: date | None = None, records: list[dict] | None = None) -> set[str]:
    """Generate only approved, date-eligible new articles; keep two authored legacy ones."""
    if today is None:
        today = datetime.now(ZoneInfo("America/Chicago")).date()
    if records is None:
        data = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))
        records = data["stories"]
    eligible = available_stories(records, today)
    new = sorted((story for story in eligible if story["slug"] not in LEGACY_PUBLISHED),key=lambda s:s["slug"])
    outputs = set()
    for story in new:
        filename = f"stories/{story['slug']}.html"
        page = destination / filename
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(article_page(story), encoding="utf-8")
        outputs.add(filename)
    archive_path = destination / "stories.html"
    archive_path.write_text(append_archive_cards(archive_path.read_text(encoding="utf-8"), new), encoding="utf-8")
    update_sitemap(destination, outputs)
    print(f"ARTICLES: published {len(new)} new approved date-eligible article page(s)")
    return outputs


if __name__ == "__main__":
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        output = Path(t)
        shutil.copyfile(ROOT / "stories.html", output / "stories.html")
        shutil.copyfile(ROOT / "sitemap.xml", output / "sitemap.xml")
        print(render_articles(output))
