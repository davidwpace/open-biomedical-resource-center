#!/usr/bin/env python3
"""Turn approved discovery metadata into no-login interactive lessons.

Only existing published, source-linked stories and the previously published
BRAF demonstration may enter this build. This module does NOT certify scientific
truth or set editorial approval. It creates static HTML from already curated
material; no model calls, credentials, network, telemetry, or patient data.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

from render_daily_spotlight import available_stories

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://davidwpace.github.io/open-biomedical-resource-center/"
SAFE_THEMES = {"mold", "pancreas", "dna"}
LEGACY_CASES = {"braf-melanoma"}
SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def e(value: object) -> str:
    return escape(str(value), quote=True)


def _require_https(url: object, what: str) -> str:
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ValueError(f"{what} needs an HTTPS URL")
    return url


def learning_records(today: date) -> list[dict]:
    catalog = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))
    stories = available_stories(catalog["stories"], today)
    # The BRAF lab was already publicly documented and published before a
    # generic lesson generator existed; do not allow unknown extra cases
    # to bypass the human editorial review gate in stories.json.
    cases = json.loads((ROOT / "data/lesson_cases.json").read_text(encoding="utf-8"))["cases"]
    if {c["slug"] for c in cases} != LEGACY_CASES:
        raise ValueError("Lesson-case adaptations must match previously published BRAF lab only")
    for case in cases:
        if case.get("source_type") != "previously_published_lab_adaptation":
            raise ValueError("Case is not a previously published lab adaptation")
        if case.get("original_demo") != "lab/braf-melanoma.html":
            raise ValueError("Unexpected BRAF demonstration source")
        if not (ROOT / case["original_demo"]).is_file():
            raise ValueError("Referenced original BRAF demonstration does not exist")
        if date.fromisoformat(case["published_on"]) <= today:
            stories.append(case)
    return sorted(stories, key=lambda s: s["slug"])


def all_activities() -> dict:
    data = json.loads((ROOT / "data/lesson_activities.json").read_text(encoding="utf-8"))
    return data["by_slug"]


def validate_lesson(record: dict, activities: list[dict] | None) -> None:
    slug = record["slug"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError(f"Unsafe lesson slug: {slug!r}")
    if record.get("theme", "") not in SAFE_THEMES:
        raise ValueError(f"{slug}: unknown visual motif")
    if not record.get("intro") or not record.get("hook"):
        raise ValueError(f"{slug}: missing beginner introduction or question")
    chapters = record.get("chapters", [])
    sources = record.get("sources", [])
    if len(chapters) < 3 or len(sources) < 2:
        raise ValueError(f"{slug}: insufficient chapters or published evidence")
    source_ids = set()
    for source in sources:
        source_ids.add(source["id"])
        _require_https(source["url"], f"{slug} source")
    for n, chapter in enumerate(chapters):
        for field in ("title", "body", "takeaway", "source"):
            if not chapter.get(field):
                raise ValueError(f"{slug}: chapter {n} missing {field}")
        if chapter["source"] not in source_ids:
            raise ValueError(f"{slug}: chapter {n} cites missing source")
    _require_https(record.get("tool_url"), f"{slug} tool")
    for field in ("tool_title", "tool_why", "tool_task", "tool_answer", "tool_limitation"):
        if not str(record.get(field, "")).strip():
            raise ValueError(f"{slug}: missing public source-check task field {field}")
    if activities is not None:
        if len(activities) != len(chapters):
            raise ValueError(f"{slug}: activity/chapter count must match")
        for i, item in enumerate(activities):
            if not item.get("question") or len(item.get("choices", [])) < 2:
                raise ValueError(f"{slug}: interactive checkpoint {i} incomplete")
            counts = [choice.get("quality") for choice in item["choices"]]
            if counts.count("supported") != 1 or any(x not in {"supported", "overclaim"} for x in counts):
                raise ValueError(f"{slug}: checkpoint {i} must have one evidence-supported choice")
            if any(not (ch.get("text") and ch.get("feedback")) for ch in item["choices"]):
                raise ValueError(f"{slug}: checkpoint {i} has a missing explanation")


def illustration(theme: str) -> str:
    if theme == "mold":
        return ('<div class="lesson-illustration illustration-mold" role="img" '
                'aria-label="Conceptual petri dish: a mold spot near an area without bacterial dots; not a photograph of the historic experiment.">'
                '<span class="dish"><i class="moldspot"></i><i class="clearzone"></i></span>'
                '<span class="illustration-note">SCHEMATIC · NOT HISTORIC EXPERIMENTAL DATA</span></div>')
    if theme == "pancreas":
        return ('<div class="lesson-illustration illustration-flow" role="img" '
                'aria-label="Conceptual sequence: pancreas, insulin signal, blood sugar regulation.">'
                '<span>Pancreas</span><b aria-hidden="true">→</b><span>Insulin</span><b aria-hidden="true">→</b>'
                '<span>Blood sugar</span><small>SIMPLIFIED BIOLOGY · NOT CLINICAL DATA</small></div>')
    return ('<div class="lesson-illustration illustration-flow illustration-dna" role="img" '
            'aria-label="Conceptual path from a gene alteration through a pathway to a clinical research question.">'
            '<span>BRAF change</span><b aria-hidden="true">→</b><span>Cell signaling</span><b aria-hidden="true">→</b>'
            '<span>Test a hypothesis</span><small>SCHEMATIC · NOT AN ACTUAL PATIENT MODEL</small></div>')


def page(record: dict, activities: list[dict] | None) -> str:
    validate_lesson(record, activities)
    slug = record["slug"]
    chapters = record["chapters"]
    src_map = {src["id"]: src for src in record["sources"]}
    parts = []
    for i, chapter in enumerate(chapters):
        source = src_map[chapter["source"]]
        activity = activities[i] if activities is not None else None
        if activity:
            choices = "".join(
                '<button type="button" class="reason-choice" data-quality="%s" '
                'data-feedback="%s">%s</button>' %
                (e(c["quality"]), e(c["feedback"]), e(c["text"]))
                for c in activity["choices"]
            )
            question = (f'<fieldset class="challenge"><legend>{e(activity["question"])}</legend>'
                        f'<div class="reason-choices">{choices}</div>'
                        '<p class="choice-feedback" role="status" aria-live="polite" hidden></p></fieldset>')
        else:
            question = ('<p class="reflection">Before revealing the evidence, ask yourself: '
                        'what did the researchers actually observe, and what remains uncertain?</p>')
        parts.append(f'''<section class="lesson-step" id="stage-{i+1}" data-step="{i}" aria-labelledby="stage-title-{i+1}">
          <span class="lesson-kicker">STEP {i+1} OF {len(chapters)} · {e(chapter["kicker"])}</span>
          <h2 id="stage-title-{i+1}" tabindex="-1">{e(chapter["title"])}</h2>
          <p class="stage-context">{e(chapter["body"])}</p>
          {question}
          <button class="reveal-evidence" type="button" aria-expanded="false">Show what the evidence supports <span aria-hidden="true">↓</span></button>
          <div class="evidence-reveal" hidden>
            <strong>What the evidence supports</strong><p>{e(chapter["takeaway"])}</p>
            <a href="{e(source["url"])}" target="_blank" rel="noopener noreferrer">Inspect the supporting source: {e(source["label"])} ↗</a>
          </div>
        </section>''')
    sources = "".join(
        f'<li><a href="{e(src["url"])}" rel="noopener noreferrer" target="_blank">{e(src["label"])} ↗</a>'
        f' <small>{e(src.get("kind", "Research source"))}</small></li>'
        for src in record["sources"]
    )
    original = "An earlier published BioDiscovery Lab" if slug == "braf-melanoma" else "An already published landmark discovery story"
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(record["intro"])}">
<meta name="theme-color" content="#103947">
<link rel="canonical" href="{BASE}learn/{slug}.html">
<link rel="stylesheet" href="../assets/lesson.css">
<script src="../assets/lesson.js" defer></script>
<title>{e(record["title"])} — Interactive Discovery Lab</title></head>
<body>
<a class="skip" href="#main">Skip to the discovery</a>
<header class="lab-header"><a class="brand" href="../index.html">✳ OPEN BIOMED · RESOURCE CENTER</a>
<nav aria-label="Learning navigation"><a href="../learn.html">All lessons</a><a href="../stories.html">Discovery stories</a></nav></header>
<main id="main" class="lab-container">
<section class="lab-hero" aria-labelledby="lesson-title">
<div class="lab-eyebrow">INTERACTIVE DISCOVERY · {e(record["topic"])}</div>
<h1 id="lesson-title">{e(record["title"])}</h1>
<p>{e(record["intro"])}</p>
<div class="lab-stats"><span>4 short decisions</span><span>Real original sources</span><span>No signup or patient data</span></div>
{illustration(record["theme"])}
<div class="central-question"><span class="lab-eyebrow">THE QUESTION</span><strong>{e(record["hook"])}</strong></div>
<a class="lab-primary" href="#journey">Begin the investigation <span aria-hidden="true">↓</span></a>
</section>
<section class="lab-journey" id="journey" aria-labelledby="journey-title">
<div class="lab-progress"><div><span class="lab-eyebrow">FOLLOW THE EVIDENCE</span>
<h2 id="journey-title">What would you conclude?</h2></div>
<div class="lab-progress-status"><span id="progress-label" role="status" aria-live="polite">Step 1 of {len(chapters)}</span>
<div class="progress-track" role="progressbar" aria-valuemin="1" aria-valuemax="{len(chapters)}" aria-valuenow="1"
aria-label="Discovery progress" id="progress-track"><div id="progress-fill" style="width:{100/len(chapters):.0f}%"></div></div></div></div>
{''.join(parts)}
<div class="stage-controls"><button id="step-back" type="button" class="lab-secondary" disabled>← Previous clue</button>
<button id="step-next" type="button" class="lab-primary">Next clue →</button></div>
</section>
<section class="lab-tool" id="research-task" aria-labelledby="research-title">
<div class="lab-eyebrow">YOUR TURN · A REAL PUBLIC RESEARCH TOOL</div>
<h2 id="research-title" tabindex="-1">Can you check a fact yourself?</h2>
<p><strong>Why this tool?</strong> {e(record["tool_why"])}</p>
<div class="task-panel"><span aria-hidden="true">1</span><div><strong>Your small task</strong>
<p>{e(record["tool_task"])}</p></div></div>
<a class="lab-primary" href="{e(record["tool_url"])}" rel="noopener noreferrer" target="_blank">Open {e(record["tool_title"])} ↗</a>
<details class="answer"><summary>Check the expected finding (after you try)</summary>
<p>{e(record["tool_answer"])}</p></details>
<p class="lab-caution"><strong>Important limit:</strong> {e(record["tool_limitation"])}</p>
</section>
<section class="research-wrap" id="report" aria-labelledby="report-title">
<div class="lab-eyebrow">SAVE WHAT YOU LEARNED</div><h2 id="report-title">Your evidence trail</h2>
<p>You can save your choices and source links as a simple text report. It stays on your device; no answers are sent to us.</p>
<div class="report-actions"><button type="button" id="download-notes" class="lab-primary">Download learning notes</button>
<button type="button" id="copy-notes" class="lab-secondary">Copy notes</button><p role="status" aria-live="polite" id="report-status"></p></div>
</section>
<section class="research-sources" aria-labelledby="sources-title">
<div class="lab-eyebrow">VERIFY THE ORIGINAL EVIDENCE</div><h2 id="sources-title">What can we check?</h2>
<ol>{sources}</ol>
<p><strong>Dates matter:</strong> Original research era {e(record["original_year"])}; educational source review {e(record["reviewed_on"])}. Modern tools are learning aids—not tools necessarily used by historical investigators.</p>
<p class="source-boundary">{original}. This interactive lesson reconstructs the logic from public sources, not a hands-on recreation of the original laboratory experiment. It is educational, not clinical guidance, and not an independent expert endorsement.</p>
</section>
</main>
<footer class="lab-footer"><a href="../learn.html">Explore another discovery</a><a href="../review.html">Challenge the science</a><p>Open Biomedical Resource Center · No private medical information collected.</p></footer>
<noscript><p class="noscript">All stages and sources are visible without JavaScript; interactive questions and download controls require JavaScript.</p></noscript>
</body></html>'''


def archive(records: list[dict]) -> str:
    cards = []
    for record in records:
        slug = record["slug"]
        cards.append(f'''<article class="lesson-card">
<span class="lab-eyebrow">{e(record["topic"])} · {e(record["original_year"])}</span>
<h2>{e(record["title"])}</h2><p>{e(record["intro"])}</p>
<a href="learn/{slug}.html">Start the interactive investigation →</a></article>''')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Learn science by investigating real breakthroughs. Make predictions, check evidence and try free research tools.">
<link rel="canonical" href="{BASE}learn.html"><link rel="stylesheet" href="assets/lesson.css">
<title>Interactive Discovery Lessons — Open Biomedical Resource Center</title></head>
<body><a class="skip" href="#main">Skip to lessons</a>
<header class="lab-header"><a class="brand" href="index.html">✳ OPEN BIOMED · RESOURCE CENTER</a>
<nav aria-label="Site"><a href="today.html">Today's story</a><a href="stories.html">Stories</a><a href="index.html">Home</a></nav></header>
<main class="lab-container" id="main"><section class="lab-hero">
<div class="lab-eyebrow">LEARN BY DOING · INTERACTIVE DISCOVERY LESSONS</div>
<h1>Don't just read about a breakthrough. <em>Think like an investigator.</em></h1>
<p>Notice a clue. Make a prediction. Check what researchers actually tested. Try one safe, public-data research task—no science degree needed.</p>
<div class="lab-stats"><span>{len(records)} investigations</span><span>Original scientific sources</span><span>Free and no signup</span></div>
</section><section class="lesson-grid" aria-label="Available interactive investigations">{''.join(cards)}</section>
<section class="archive-note"><h2>These are learning reconstructions, not new discoveries</h2>
<p>Each lesson separates the original finding from later interpretations and modern tools. An answer explains what evidence supports, but no lesson replaces clinical judgment or hands-on supervised laboratory training.</p>
<a href="review.html">Help verify scientific claims →</a></section></main>
<footer class="lab-footer"><a href="index.html">Resource Center home</a><a href="contribute.html">Contribute a public source</a></footer>
</body></html>'''


def update_sitemap(destination: Path, new_pages: set[str]) -> None:
    path = destination / "sitemap.xml"
    tree = ET.parse(path)
    root = tree.getroot()
    ET.register_namespace("", SITEMAP_NAMESPACE)
    tag = "{" + SITEMAP_NAMESPACE + "}"
    existing = {el.text for el in root.iter(tag + "loc")}
    for page_path in sorted(new_pages):
        url = BASE + page_path
        if url not in existing:
            entry = ET.SubElement(root, tag + "url")
            ET.SubElement(entry, tag + "loc").text = url
            ET.SubElement(entry, tag + "changefreq").text = "weekly"
    tree.write(path, encoding="utf-8", xml_declaration=True)


def render_lessons(destination: Path, *, today: date | None = None) -> set[str]:
    if today is None:
        today = datetime.now(ZoneInfo("America/Chicago")).date()
    records = learning_records(today)
    activities = all_activities()
    known = {r["slug"] for r in records}
    extras = set(activities) - known
    if extras:
        raise ValueError(f"Activities for unapproved or unavailable stories: {sorted(extras)}")
    destination.mkdir(parents=True, exist_ok=True)
    outputs = {"learn.html"}
    (destination / "learn.html").write_text(archive(records), encoding="utf-8")
    for record in records:
        slug = record["slug"]
        filename = f"learn/{slug}.html"
        file = destination / filename
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(page(record, activities.get(slug)), encoding="utf-8")
        outputs.add(filename)
    update_sitemap(destination, outputs)
    print(f"LESSONS: generated {len(records)} approved/previously published investigations")
    return outputs


if __name__ == "__main__":
    import shutil
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "sitemap.xml", out / "sitemap.xml")
    render_lessons(out)
