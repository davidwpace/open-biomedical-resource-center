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

    index = (ROOT / "index.html").read_text(encoding="utf-8")
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
    for target in ("", "catalog.html", "agent-access.html"):
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
