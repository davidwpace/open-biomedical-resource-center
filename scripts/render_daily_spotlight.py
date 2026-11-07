#!/usr/bin/env python3
"""Render a daily *featured* discovery from reviewed stories.

This is an unattended presentation scheduler, NOT an AI fact-checker. It only
features stories that have passed the repository's editorial publication gate.
The resulting page is generated in the deployment artifact and does not commit
or publish an unreviewed story.
"""
from __future__ import annotations

import json
from datetime import date
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://davidwpace.github.io/open-biomedical-resource-center/"
# These were already public before the approval field was introduced.
# All future additions MUST explicitly be approved and dated.
LEGACY_PUBLISHED = {"penicillin", "insulin"}


def available_stories(records: list[dict], today: date) -> list[dict]:
    eligible = []
    slugs: set[str] = set()
    for item in records:
        slug = item.get("slug", "")
        if not slug or not slug.replace("-", "").isalnum() or slug in slugs:
            raise ValueError(f"Invalid or repeated story slug: {slug!r}")
        slugs.add(slug)
        status = item.get("editorial_status", "")
        if status not in {"approved", "draft", ""}:
            raise ValueError(f"Unrecognized story status for {slug}: {status!r}")
        if status == "draft":
            continue
        if status == "" and slug not in LEGACY_PUBLISHED:
            raise ValueError(f"New story {slug!r} requires explicit editorial_status")
        if status == "approved" and not item.get("reviewed_on"):
            raise ValueError(f"Approved story {slug!r} lacks a review date")
        pub = date.fromisoformat(item["published_on"])
        if pub > today:
            continue
        if len(item.get("sources", [])) < 2 or len(item.get("chapters", [])) < 3:
            raise ValueError(f"Insufficient published evidence for {slug}")
        for src in item["sources"]:
            if not src.get("url", "").startswith("https://"):
                raise ValueError(f"Invalid source URL for {slug}")
        eligible.append(item)
    return eligible


def daily_choice(stories: list[dict], today: date) -> dict:
    if not stories:
        raise ValueError("No eligible reviewed stories to feature")
    stories = sorted(stories, key=lambda s: s["slug"])
    # Give an approved, newly published article its first-day spotlight.
    # A future-dated story stays out of this published collection until due.
    new_today = [s for s in stories if date.fromisoformat(s["published_on"]) == today]
    if new_today:
        return sorted(new_today, key=lambda s: s["slug"])[0]
    # Otherwise rotate existing approved articles predictably.
    anchor = date(2026, 11, 8)
    index = (today - anchor).days % len(stories)
    return stories[index]


def render_spotlight(destination: Path, *, today: date | None = None) -> set[str]:
    if today is None:
        today = datetime.now(ZoneInfo("America/Chicago")).date()
    data = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))
    eligible = available_stories(data["stories"], today)
    selected = daily_choice(eligible, today)
    slug = selected["slug"]
    target = f"stories/{slug}.html"
    # Only existing, source-backed public stories may appear in daily rotation.
    if not (destination / target).is_file() and not (ROOT / target).is_file():
        raise ValueError(f"Approved story missing published HTML: {target}")
    title = escape(selected["title"])
    description = escape(selected["intro"])
    hook = escape(selected["hook"])
    tool = escape(selected["tool_title"])
    why = escape(selected["tool_why"])
    task = escape(selected["tool_task"])
    caveat = escape(selected["tool_limitation"])
    topic = escape(selected["topic"])
    source_items = "\n".join(
        f'<li><a href="{escape(src["url"], quote=True)}" rel="noopener noreferrer" target="_blank">{escape(src["label"])} ↗</a></li>'
        for src in selected["sources"][:3]
    )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Today’s featured research discovery from the Open Biomedical Resource Center. One question, a documented science story, and a small research task.">
<link rel="canonical" href="{BASE}today.html">
<script src="assets/theme.js"></script><link rel="stylesheet" href="assets/story.css"><link rel="stylesheet" href="assets/theme.css">
<title>Today's Discovery — Open Biomedical Resource Center</title></head>
<body>
<a class="skip" href="#main">Skip to today's story</a>
<header class="bar"><a class="brand" href="index.html">✳ OPEN BIOMED · RESOURCE CENTER</a><nav aria-label="Site navigation"><a href="stories.html">All stories</a><a href="start.html">Find a tool</a></nav></header>
<main class="container" id="main">
<section class="index-hero">
<span class="eyebrow">TODAY'S FEATURED DISCOVERY · {today.isoformat()}</span>
<h1>One question can change what we know.</h1>
<p>Here is a research story to explore today. <strong>Featured today doesn't mean newly discovered today.</strong> We select from previously published, source-linked educational stories.</p>
</section>
<section class="story-box" aria-labelledby="featured-title">
<div class="story-head"><span class="story-num">{topic} · ORIGINAL DISCOVERY: {escape(str(selected["original_year"]))}</span>
<h2 id="featured-title">{title}</h2><p>{description}</p></div>
<div class="story-inner">
<div class="intro-line"><strong>?</strong><span>{hook}</span></div>
<a class="main-cta" href="learn/{slug}.html">Try the interactive investigation →</a> <a class="secondary-cta" href="{target}">Read the original story →</a>
</div>
</section>
<section class="lesson" aria-labelledby="task-title">
<span class="story-num">ONE SMALL TASK · YOUR TURN</span><h2 id="task-title">Try one real research step.</h2>
<p><strong>Why {tool}?</strong> {why}</p>
<div class="mission"><span class="mission-number">1</span><div><strong>What to do first</strong><p>{task}</p></div></div>
<p class="limit"><strong>Important limit:</strong> {caveat}</p>
<a class="secondary-cta" href="{escape(selected["tool_url"],quote=True)}" rel="noopener noreferrer" target="_blank">Open {tool} ↗</a>
</section>
<section class="sources"><span class="story-num">CHECK THE SOURCES</span><h2>Where the evidence comes from</h2><ul>{source_items}</ul>
<p class="disclaimer">Original scientific discovery: {escape(str(selected["original_year"]))}. Story source review: {escape(selected["reviewed_on"])}. Featured date: {today.isoformat()}. These are different dates. Educational content is not clinical guidance. The source pages may change; confirm details with their publishers.</p>
<a class="secondary-cta" href="stories.html">Browse the full story library</a></section>
</main><footer class="footer"><strong>OPEN BIOMED RESOURCE CENTER</strong><p>A daily selection from a reviewed story library. No claim of a new biomedical breakthrough is made by featuring an older study today.</p><a href="index.html">Return to the Center</a></footer>
</body></html>"""
    destination.mkdir(parents=True, exist_ok=True)
    page = destination / "today.html"
    page.write_text(html, encoding="utf-8")
    meta = destination / "data" / "today.json"
    meta.parent.mkdir(parents=True, exist_ok=True)
    meta.write_text(json.dumps({
        "date_local": today.isoformat(),
        "timezone": "America/Chicago",
        "type": "daily_feature_from_published_library",
        "slug": slug,
        "title": selected["title"],
        "original_year": selected["original_year"],
        "reviewed_on": selected["reviewed_on"],
        "url": BASE + target,
        "not_new_discovery": True,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"FEATURED: {slug} for {today.isoformat()} ({len(eligible)} approved/legacy eligible stories)")
    return {"today.html", "data/today.json"}


if __name__ == "__main__":
    render_spotlight(ROOT / "dist")
