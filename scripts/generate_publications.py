"""Build an article library, text exports and a feed with explicit review status."""
from datetime import datetime
from email.utils import format_datetime
from html import escape as e
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
from generate_review_drafts import ROOT, template, safe_url
from generate_lessons import update_sitemap
from render_daily_spotlight import available_stories

BASE = "https://davidwpace.github.io/open-biomedical-resource-center/"

def add_existing_article_tools(destination, path, title):
    target = destination / path
    # Unit callers may build only exports; prepare_pages checks every linked page.
    if not target.exists():
        return
    page = target.read_text()
    if 'id="reading"' in page:
        raise ValueError("Article already has a reading wrapper")
    sample = template(title, "", "../", article_path=path)
    controls = sample[sample.index('<div aria-label="Read aloud">'):sample.index('<main id="reading">')]
    page = page.replace("</head>", '<link rel="canonical" href="' + BASE + path + '"><link rel="stylesheet" href="../assets/publications.css"><script src="../assets/listen.js" defer></script><script src="../assets/publications.js" defer></script></head>', 1)
    page = re.sub(r"(<main\b[^>]*>)", lambda m: controls + m[1] + '<div id="reading">', page, count=1)
    page = page.replace("</main>", "</div></main>", 1)
    page = page.replace("</nav>", '<a href="../articles.html">All articles</a></nav>', 1)
    target.write_text(page)


def story_text(s, status, url):
    lines = ["# " + s["title"], "", status, "",
             "Prepared for David W. Pace Sr. with AI assistance. Original discoveries retain their source attribution.",
             "", "Original discovery: " + str(s["original_year"]), "", s["hook"], "", s["intro"]]
    for c in s["chapters"]:
        lines += ["", "## " + c["title"], "", c["body"], "", "Reasoning: " + c["takeaway"], "", "Supporting source: " + c["source"]]
    lines += ["", "## Try a source check", "", s.get("tool_task", ""), "", s.get("tool_limitation", ""), "", "## Sources"]
    for source in s["sources"]:
        safe_url(source["url"])
        lines += ["", "- [" + source["id"] + "] " + (source.get("label") or source.get("title") or source["id"]) + ": " + source["url"]]
    return "\n".join(lines + ["", "Canonical article: " + url, "", "Public science education. No clinical advice.", ""])


def manuscript_body(s):
    ids = {x["id"] for x in s["sources"]}
    def paragraph(text):
        def cite(match):
            keys = [x.strip() for x in match[1].split(",")]
            if any(key not in ids for key in keys):
                raise ValueError("Unknown manuscript citation")
            return " ".join('<a href="#source-' + key + '">[' + key + ']</a>' for key in keys)
        return "<p>" + re.sub(r"\[([A-Z]\d+(?:,\s*[A-Z]\d+)*)\]", cite, e(text)) + "</p>"
    body = '<p class="eyebrow">EoD · MANUSCRIPT DRAFT</p><h1>' + e(s["title"]) + '</h1><p>By ' + e(s["author"]) + ' · Prepared ' + e(s["prepared_on"]) + ' · Published for review ' + e(s["published_for_review_on"]) + '</p><p class="warning"><strong>PUBLIC MANUSCRIPT DRAFT — UNAPPROVED.</strong> AI-assisted; editorial approval and independent review are pending.</p>'
    body += "".join(paragraph(p) for p in s["paragraphs"])
    body += '<h2>Sources and scope</h2><p>' + e(s["provenance"]) + '</p><ul>'
    for x in s["sources"]:
        if not re.fullmatch(r"[A-Z]\d+", x["id"]):
            raise ValueError("Invalid manuscript source identifier")
        body += '<li id="source-' + x["id"] + '"><a href="' + safe_url(x["url"]) + '">' + e(x["label"]) + '</a></li>'
    return body + '</ul><p><a href="' + safe_url(s["review_url"]) + '">Suggest a correction or source-backed annotation</a></p>'


def render(destination):
    today = datetime.now(ZoneInfo("America/Chicago")).date()
    drafts = json.loads((ROOT / "data/review_drafts.json").read_text())["records"]
    originals = available_stories(json.loads((ROOT / "data/stories.json").read_text())["stories"], today)
    ms = json.loads((ROOT / "data/manuscript_drafts.json").read_text())
    if ms.get("publication_class") != "public_manuscript_draft":
        raise ValueError("Explicit manuscript draft classification required")
    entries, texts, paths = [], {}, set()
    for item in drafts:
        s = item["story"]
        path = "review-drafts/" + s["slug"] + ".html"
        entries.append(dict(slug=s["slug"], title=s["title"], intro=s["intro"], topic=s["topic"],
                            status="Public review draft", kind="draft", path=path, source_record=item["issue_url"],
                            source_snapshot_sha256=item.get("source_snapshot_sha256")))
        texts[s["slug"]] = story_text(s, "PUBLIC REVIEW DRAFT — editorial approval and independent review pending.", BASE + path)
    for s in originals:
        path = "stories/" + s["slug"] + ".html"
        add_existing_article_tools(destination, path, s["title"])
        entries.append(dict(slug=s["slug"], title=s["title"], intro=s["intro"], topic=s["topic"],
                            status="Published educational story", kind="story", path=path, published_on=s["published_on"]))
        texts[s["slug"]] = story_text(s, "Published educational story. This status does not claim journal peer review.", BASE + path)
    for s in ms["records"]:
        slug = s["slug"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError("Invalid manuscript slug")
        path = "articles/" + slug + ".html"
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(template(s["title"], manuscript_body(s), "../", article_path=path))
        paths.add(path)
        entries.append(dict(slug=slug, title=s["title"], intro=s["intro"], topic="Evolution on Demand",
                            status="Public manuscript draft", kind="draft", path=path,
                            prepared_on=s["prepared_on"], published_on=s["published_for_review_on"]))
        lines = ["# " + s["title"], "By " + s["author"],
                 "PUBLIC MANUSCRIPT DRAFT — editorial approval and independent review pending.",
                 s["provenance"]] + s["paragraphs"] + ["## Sources"]
        lines += ["- [" + x["id"] + "] " + x["label"] + ": " + x["url"] for x in s["sources"]]
        texts[slug] = "\n\n".join(lines + ["Canonical article: " + BASE + path, ""])
    entries.sort(key=lambda x: (x["kind"] != "draft", x["title"].casefold()))
    if len({x["slug"] for x in entries}) != len(entries):
        raise ValueError("Duplicate slug across article collections")
    cards = []
    for x in entries:
        x["url"] = BASE + x["path"]
        x["export_path"] = "exports/" + x["slug"] + ".md"
        target = destination / x["export_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(texts[x["slug"]])
        paths.add(x["export_path"])
        cards.append('<article class="article-card" data-kind="' + x["kind"] + '" data-search="' + e((x["title"] + " " + x["topic"]).casefold(), quote=True) + '"><p class="eyebrow">' + e(x["status"]) + '</p><h2><a data-article-url href="' + x["path"] + '">' + e(x["title"]) + '</a></h2><p>' + e(x["intro"]) + '</p><div class="card-links"><a href="' + x["path"] + '">Read' + (" / listen" if x["kind"] == "draft" else "") + ' →</a><a download href="' + x["export_path"] + '">Download text</a></div></article>')
    count = sum(x["kind"] == "draft" for x in entries)
    body = '<p class="eyebrow">DAVID W. PACE SR. · OPEN BIOMED</p><h1>Ideas worth examining.<br>Articles ready to share.</h1><p class="lede">Read the evidence, listen to the story, and help improve the explanation.</p><p>' + str(len(entries)) + ' articles · ' + str(count) + ' published for review · ' + str(len(entries)-count) + ' existing educational stories.</p><p class="collection-note">Public drafts are labeled clearly. Publication here does not mean they have completed independent review.</p><div class="publication-tools"><button data-action="copy-all-links">Copy all article links</button><a download href="exports/all-articles.md">Download all articles</a><a href="articles-feed.xml">Follow the article feed</a></div><p id="publication-status" role="status"></p><div class="article-filters"><label for="article-search">Find an article</label><input id="article-search" type="search" placeholder="Search title or topic"><label for="article-kind">Show</label><select id="article-kind"><option value="all">All articles</option><option value="draft">Published for review</option><option value="story">Existing stories</option></select></div><p id="article-count" role="status">' + str(len(entries)) + ' articles shown</p><section class="article-grid" aria-label="Article library">' + "".join(cards) + '</section><section class="next-step"><h2>From prepared draft to public article</h2><p>Owner-authored, source-linked discovery drafts join this library through the existing daily publishing build. Each article keeps its review status, sources and annotation link.</p><p>Use <strong>Copy article</strong> on a draft to reuse its formatted text in a newsletter or another publisher. Publishing there remains a separate action in that service.</p><p><a href="review.html">Help review an article</a> · <a href="stories.html">Interactive discovery lessons</a> · <a download href="article-links.txt">Download all article links</a></p></section>'
    (destination / "articles.html").write_text(template("Article library", body, ""))
    paths.add("articles.html")
    (destination / "exports/all-articles.md").write_text("\n\n---\n\n".join(texts[x["slug"]] for x in entries))
    paths.add("exports/all-articles.md")
    (destination / "article-links.txt").write_text("\n\n".join(x["title"] + "\n" + x["status"] + "\n" + x["url"] for x in entries) + "\n")
    paths.add("article-links.txt")
    (destination / "data/publications.json").write_text(json.dumps({"publication_statement": "Publication and independent review are separate statuses.", "articles": entries}, ensure_ascii=False, indent=2) + "\n")
    paths.add("data/publications.json")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for k, v in {"title": "Open Biomed — all articles and public drafts", "link": BASE + "articles.html", "description": "Public research drafts and educational stories. Every entry states its review status."}.items():
        ET.SubElement(channel, k).text = v
    for x in entries:
        item = ET.SubElement(channel, "item")
        for k, v in {"title": "[" + x["status"] + "] " + x["title"], "link": x["url"], "guid": x["url"], "description": x["status"] + ". " + x["intro"]}.items():
            ET.SubElement(item, k).text = v
        if x.get("published_on"):
            ET.SubElement(item, "pubDate").text = format_datetime(datetime.fromisoformat(x["published_on"]).replace(tzinfo=ZoneInfo("America/Chicago")))
    ET.indent(rss)
    (destination / "articles-feed.xml").write_bytes(ET.tostring(rss, encoding="utf-8", xml_declaration=True))
    paths.add("articles-feed.xml")
    update_sitemap(destination, {p for p in paths if p.endswith(".html")} | {x["path"] for x in entries})
    print(f"PUBLICATIONS: {len(entries)} articles; {count} public drafts; text exports and status-labeled feed")
    return paths

