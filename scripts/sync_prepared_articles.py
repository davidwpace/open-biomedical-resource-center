#!/usr/bin/env python3
"""Import owner-authored public discovery drafts without granting editorial approval."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "davidwpace/open-biomedical-resource-center"
OWNER = "davidwpace"


def validate_story(story):
    if story.get("editorial_status") != "draft":
        raise ValueError("Only explicit editorial drafts can enter this intake")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(story.get("slug", ""))):
        raise ValueError("Invalid article slug")
    for name in ("title", "hook", "intro", "topic"):
        if not isinstance(story.get(name), str) or not story[name].strip():
            raise ValueError("Missing article field: " + name)
    if type(story.get("original_year")) is not int:
        raise ValueError("An explicit historical year is required")
    sources = story.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("Sources are required")
    ids = set()
    for source in sources:
        sid = source.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", sid) or sid in ids:
            raise ValueError("Invalid or duplicate source id")
        ids.add(sid)
        url = urlsplit(str(source.get("url", "")))
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            raise ValueError("Sources must use ordinary HTTPS URLs")
    chapters = story.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        raise ValueError("Narrative chapters are required")
    for chapter in chapters:
        if chapter.get("source") not in ids:
            raise ValueError("A chapter refers to an absent source")
        for key in ("title", "body", "takeaway"):
            if not isinstance(chapter.get(key), str) or not chapter[key].strip():
                raise ValueError("Incomplete narrative chapter")
    return story


def extract_story(body):
    candidates = []
    for block in re.findall(r"\x60{3}(?:json)?\s*\n(.*?)\x60{3}", body or "", re.S):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "editorial_status" in value and "chapters" in value:
            candidates.append(value)
    if len(candidates) != 1:
        raise ValueError("Exactly one structured story is required")
    return validate_story(candidates[0])


def import_issues(data, issues, *, as_of=None):
    if data.get("publication_class") != "public_review_draft":
        raise ValueError("Public-review classification required")
    result = json.loads(json.dumps(data))
    records = result["records"]
    seen_numbers = {r["issue_number"] for r in records}
    seen_slugs = {r["story"]["slug"] for r in records}
    added, held = [], []
    as_of = as_of or datetime.now(ZoneInfo("America/Chicago")).date().isoformat()
    for issue in sorted(issues, key=lambda x: x.get("number", 0)):
        if issue.get("pull_request") or "EDITORIAL DRAFT" not in issue.get("title", "").upper():
            continue
        number = issue["number"]
        # Existing curated snapshots remain authoritative; never replace them from an issue.
        if number in seen_numbers:
            continue
        if issue.get("user", {}).get("login") != OWNER:
            held.append({"issue": number, "reason": "Not an owner-authored discovery draft"})
            continue
        if issue.get("html_url") != f"https://github.com/{REPOSITORY}/issues/{number}":
            held.append({"issue": number, "reason": "Unexpected source repository"})
            continue
        try:
            story = extract_story(issue.get("body", ""))
            if story["slug"] in seen_slugs:
                raise ValueError("Duplicate slug")
        except ValueError as exc:
            held.append({"issue": number, "reason": str(exc)})
            continue
        body_hash = hashlib.sha256(issue["body"].encode()).hexdigest()
        records.append({
            "issue_number": number,
            "issue_url": issue["html_url"],
            "source_snapshot_sha256": body_hash,
            "source_updated_at": issue.get("updated_at"),
            "prepared_on": issue.get("created_at", "")[:10],
            "included_in_build_on": as_of,
            "snapshot_note": "Published for open review at the owner's request. Source and figure checks, editorial approval, and independent peer review remain pending.",
            "story": story,
        })
        seen_numbers.add(number)
        seen_slugs.add(story["slug"])
        added.append(story["slug"])
    return result, added, held


def fetch_issues():
    issues = []
    for page in range(1, 11):
        url = f"https://api.github.com/repos/{REPOSITORY}/issues?state=open&per_page=100&page={page}"
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "OBRC-ArticlePublisher"}
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError("Unexpected GitHub issue response")
        issues.extend(batch)
        if len(batch) < 100:
            return issues
    raise ValueError("Issue pagination exceeded the explicit intake limit")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fetch", action="store_true", help="Read public owner-authored discovery issues")
    group.add_argument("--issues-json", type=Path, help="Use an already fetched GitHub issue-list snapshot")
    parser.add_argument("--destination", type=Path, default=ROOT / "data/review_drafts.json")
    args = parser.parse_args()
    issues = fetch_issues() if args.fetch else json.loads(args.issues_json.read_text())
    data, added, held = import_issues(json.loads(args.destination.read_text()), issues)
    args.destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"imported": added, "held": held, "publication_class": data["publication_class"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

