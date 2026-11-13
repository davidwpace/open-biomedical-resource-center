"""Publish explicitly unapproved public research drafts, separate from approved lessons."""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parent.parent

def safe_url(value):
    value=str(value or "")
    if urlsplit(value).scheme!="https": raise ValueError("HTTPS source URL required")
    return escape(value,quote=True)

def render(destination, data=None):
    data=data or json.loads((ROOT/"data/review_drafts.json").read_text())
    if data.get("publication_class")!="public_review_draft":raise ValueError("Draft classification required")
    paths=set();cards=[]
    for item in data["records"]:
        s=item["story"];slug=s["slug"]
        if s.get("editorial_status")!="draft" or not re.fullmatch(r"[a-z0-9-]+",slug):raise ValueError("Only explicit drafts with safe slugs")
        if not s.get("chapters") or not s.get("sources"):raise ValueError("Draft needs its source-linked narrative")
        name="review-drafts/"+slug+".html";cards.append('<li><a href="'+name+'">'+escape(s["title"])+'</a> — public review draft</li>')
        sources={x["id"]:x for x in s["sources"]}
        body='<h1>'+escape(s["title"])+'</h1><p class="warning"><strong>PUBLIC REVIEW DRAFT — UNAPPROVED.</strong> This is an AI-assisted historical explanation awaiting source/figure checks and human annotations. Publication here does not imply editorial approval or peer review.</p>'
        body+='<p><a href="'+safe_url(item["issue_url"])+'">Read the full draft package and add a source-backed annotation</a></p>'
        body+='<p>'+escape(s["hook"])+'</p><p>'+escape(s["intro"])+'</p>'
        for chapter in s["chapters"]:
            sid=chapter.get("source")
            if sid not in sources: raise ValueError("Unknown chapter source")
            body+='<section><h2>'+escape(chapter["title"])+'</h2><p>'+escape(chapter["body"])+'</p><p><strong>Reasoning:</strong> '+escape(chapter["takeaway"])+'</p><a href="#source-'+escape(sid)+'">Source and verification link</a></section>'
        body+='<h2>What still needs checking</h2><p>'+escape(item["snapshot_note"])+'</p><p>Check original methods, tables, attribution and dates. Challenge a specific claim with a source and locator. Historical dates are separate from this draft’s publication and review dates.</p>'
        body+='<h2>Try a public source check</h2><p>'+escape(s.get("tool_task",""))+'</p><p>'+escape(s.get("tool_limitation",""))+'</p>'
        if s.get("tool_url"):body+='<a href="'+safe_url(s["tool_url"])+'">'+escape(s.get("tool_title","Open tool"))+'</a>'
        body+='<h2>Sources</h2><ul>'
        for sid,source in sources.items():
            body+='<li id="source-'+escape(sid)+'"><a href="'+safe_url(source.get("url"))+'">'+escape(source.get("label") or source.get("title") or sid)+'</a></li>'
        body+='</ul>'
        page=template(s["title"],body,"../")
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page);paths.add(name)
    body='<h1>Read, listen and help review</h1><p>These five historical research drafts are publicly readable for review. They remain separate from approved lessons. Corrections and source-backed annotations are welcome.</p><ul>'+"".join(cards)+'</ul>'
    (destination/"review-drafts.html").write_text(template("Public review drafts",body,""))
    paths.add("review-drafts.html")
    return paths

def template(title,body,prefix):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+' — Open review</title><link rel="stylesheet" href="'+prefix+'assets/theme.css"><script src="'+prefix+'assets/theme.js"></script><script src="'+prefix+'assets/listen.js" defer></script><style>body{font:18px/1.7 system-ui,sans-serif;max-width:850px;margin:auto;padding:24px}a{color:#166b64}section{margin:36px 0}.warning{border-left:5px solid #a66b11;padding:16px;background:#fff4da;color:#493818}button{font:inherit;padding:9px 16px;margin:5px 4px 5px 0}nav{margin-bottom:20px}p{overflow-wrap:anywhere}@media(prefers-color-scheme:dark){a{color:#65cdbd}}</style></head><body><nav><a href="'+prefix+'index.html">Home</a> · <a href="'+prefix+'review.html">Human review invitation</a> · <a href="'+prefix+'review-drafts.html">All review drafts</a></nav><div aria-label="Read aloud"><button id="listen">Listen</button><button id="pause">Pause / resume</button><button id="stop">Stop</button><p id="speech-status" role="status">Use Listen for a spoken version. Voice availability depends on your browser and device.</p></div><main id="reading">'+body+'</main><footer><p>Historical science education. No clinical advice. No personal information is collected.</p></footer></body></html>'
