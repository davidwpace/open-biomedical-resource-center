#!/usr/bin/env python3
"""Validate static human/AI discovery files against the public resource catalog."""
from __future__ import annotations
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://davidwpace.github.io/open-biomedical-resource-center/"


class ListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = set()

    def handle_starttag(self, tag, attrs):
        vals = dict(attrs)
        if tag == "article" and vals.get("id"):
            self.ids.add(vals["id"])
        if tag == "a" and vals.get("href"):
            self.links.add(vals["href"])


def validate():
    errors = []
    catalog = json.loads((ROOT / "data/resources.json").read_text(encoding="utf-8"))
    resources = catalog["resources"]
    ids = {r["id"] for r in resources}

    # Every beginner route must point to a real curated resource, never a guessed tool.
    guide = json.loads((ROOT / "data/tool_routes.json").read_text(encoding="utf-8"))
    if len(guide.get("choices", [])) < 6:
        errors.append("Tool finder has too few beginner entry points")
    seen = set()
    for choice in guide.get("choices", []):
        if choice.get("id") in seen:
            errors.append(f"Duplicate guide choice: {choice.get('id')}")
        seen.add(choice.get("id"))
        if len(choice.get("options", [])) < 1:
            errors.append(f"Guide choice has no goals: {choice.get('id')}")
        for option in choice.get("options", []):
            if option.get("resource_id") not in ids:
                errors.append(f"Guide references missing resource: {option.get('resource_id')}")
            if not all(option.get(k) for k in ("why", "action", "caution")):
                errors.append(f"Guide route missing plain-language explanation: {choice.get('id')}")
    start = (ROOT / "start.html").read_text(encoding="utf-8")
    for value in ("id=\"choiceGrid\"", "id=\"goalChoices\"", "id=\"toolLink\"", "guide.js", "guide.css"):
        if value not in start:
            errors.append(f"Guide page missing: {value}")
    for value in ("assets/guide.js", "assets/guide.css", "assets/story.js", "assets/story.css"):
        if not (ROOT / value).is_file():
            errors.append(f"Missing beginner asset: {value}")

    # New stories are sourced and prerendered as accessible HTML, not invented at runtime.
    stories_data = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))
    slugs = set()
    story_index = (ROOT / "stories.html").read_text(encoding="utf-8")
    for story in stories_data.get("stories", []):
        slug = story.get("slug")
        if slug in slugs:
            errors.append(f"Duplicate discovery story: {slug}")
        slugs.add(slug)
        if not slug or not slug.replace("-", "").isalnum():
            errors.append(f"Invalid story slug: {slug}")
            continue
        path = ROOT / "stories" / (slug + ".html")
        if not path.exists():
            errors.append(f"Missing prerendered story: {path}")
            continue
        rendered = path.read_text(encoding="utf-8")
        if "stories/" + slug + ".html" not in story_index:
            errors.append(f"Story archive missing: {slug}")
        if story.get("resource_id") not in ids:
            errors.append(f"Story references nonexistent resource: {slug}")
        if len(story.get("chapters", [])) < 3 or len(story.get("sources", [])) < 2:
            errors.append(f"Insufficient chapters or evidence: {slug}")
        for source in story.get("sources", []):
            if not source.get("url", "").startswith("https://") or source["url"] not in rendered:
                errors.append(f"Story source missing from rendered page: {slug}")
        if story.get("tool_url") not in rendered:
            errors.append(f"Story first-action link missing: {slug}")
    if "lab/braf-melanoma.html" not in story_index:
        errors.append("Story archive missing the BRAF lab")

    html = (ROOT / "catalog.html").read_text(encoding="utf-8")
    parser = ListingParser()
    parser.feed(html)
    missing = ids - parser.ids
    extra = parser.ids - ids
    if missing:
        errors.append(f"HTML catalog missing IDs: {sorted(missing)}")
    if extra:
        errors.append(f"HTML catalog has unknown IDs: {sorted(extra)}")
    for r in resources:
        if r["official_url"] not in parser.links:
            errors.append(f"Missing official link for {r['id']}")

    openapi = json.loads((ROOT / "openapi.json").read_text(encoding="utf-8"))
    if "/data/resources.json" not in openapi.get("paths", {}):
        errors.append("OpenAPI does not declare public JSON endpoint")
    if openapi.get("servers", [{}])[0].get("url") != BASE:
        errors.append("OpenAPI server base URL mismatch")

    lab = (ROOT / "lab/braf-melanoma.html").read_text(encoding="utf-8")
    for marker in ('id="story-guide"', 'id="storyNext"', 'id="storyBack"',
                   'data-story-step="0"', 'data-story-step="1"', 'data-story-step="2"',
                   'data-story-step="3"', 'data-story-step="4"',
                   'https://doi.org/10.1038/nature00766',
                   'https://doi.org/10.1056/NEJMoa1103782',
                   '48%', '5%', 'Back to the narrated walkthrough'):
        if marker not in lab:
            errors.append(f"Guided BRAF story missing: {marker}")
    demo_js = (ROOT / "lab/demo.js").read_text(encoding="utf-8")
    for marker in ('function showStoryStep(', 'storyNext', 'storyBack',
                   '## Historical discovery milestones'):
        if marker not in demo_js:
            errors.append(f"Lab guide script missing: {marker}")
    for required in ('demo.js', 'demo.css', 'id="downloadReport"', 'id="copyReport"',
                     'https://www.cancer.gov/types/skin/hp/melanoma-treatment-pdq',
                     'https://depmap.org/portal/data_explorer_2/',
                     'https://platform.opentargets.org/target/ENSG00000157764',
                     'https://www.proteinatlas.org/ENSG00000157764-BRAF'):
        if required not in lab:
            errors.append(f"Lab missing asset or source: {required}")
    for asset in ('lab/demo.js', 'lab/demo.css'):
        if not (ROOT / asset).is_file():
            errors.append(f"Missing lab file: {asset}")
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if 'lab/braf-melanoma.html' not in index:
        errors.append("Homepage does not link to the BioDiscovery Lab")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    agent = (ROOT / "agent-access.html").read_text(encoding="utf-8")
    for marker in ('id="copyCatalog"', 'id="downloadCatalog"', 'id="manualCopy"', 'data/resources.json'):
        if marker not in agent:
            errors.append(f"AI access page is missing portable fallback: {marker}")
    for target in ("catalog.html", "agent-access.html", "data/resources.json", "llms.txt"):
        if target not in index:
            errors.append(f"Home page does not link to {target}")
    for target in ("catalog.html", "data/resources.json", "openapi.json"):
        if target not in llms or target not in agent:
            errors.append(f"Agent documentation does not expose {target}")
    tree = ET.parse(ROOT / "sitemap.xml")
    locs = {node.text for node in tree.iter() if node.tag.endswith("}loc")}
    for target in ("", "catalog.html", "agent-access.html", "lab/braf-melanoma.html", "start.html", "stories.html", "stories/penicillin.html", "stories/insulin.html"):
        if BASE + target not in locs:
            errors.append(f"Missing sitemap location: {target or '(homepage)'}")
    for loc in locs:
        path = urlparse(loc).path.removeprefix("/open-biomedical-resource-center/")
        target = ROOT / (path or "index.html")
        if not target.is_file():
            errors.append(f"Sitemap points at nonexistent file {target}")

    if errors:
        for e in errors:
            print("ERROR:", e)
        print(f"FAILED: {len(errors)} discovery issue(s)")
        return 1
    print(f"OK: {len(resources)} unique catalog pages mapped into static HTML, JSON, OpenAPI, llms.txt and sitemap")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
