#!/usr/bin/env python3
"""Verify future reviewed stories publish exactly when eligible, without hand-written pages."""
from __future__ import annotations

import copy
import json
import shutil
import sys
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_articles import ROOT, article_page, render_articles
from render_daily_spotlight import daily_choice


def approved_example():
    original = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))["stories"][0]
    s = copy.deepcopy(original)
    s["slug"] = "reviewed-demo-test"
    s["editorial_status"] = "approved"
    s["reviewed_on"] = "2026-11-07"
    s["published_on"] = "2026-11-09"
    s["review"] = {
        "editorial_approver": "@test-editor",
        "editorial_decision": "approve",
        "review_url": "https://github.com/davidwpace/open-biomedical-resource-center/issues/13",
        "conflicts_disclosed": True,
        "reviewed_on": "2026-11-07",
        "evidence_class": "historical",
        "risk_tier": "educational",
        "ai_assistance": {"used": False},
        "claim_checks": [
            {"chapter":i,"source_id":ch["source"],"assessment":"qualified",
             "source_location":"Original named publication, paragraph 4",
             "limitation":"Historical experiment limits later conclusions."}
            for i,ch in enumerate(s["chapters"])
        ]
    }
    return s


class ApprovedArticleQueueTests(unittest.TestCase):
    def setUp(self):
        self.story = approved_example()

    def destination(self, path):
        dest = Path(path)
        shutil.copyfile(ROOT / "stories.html",dest / "stories.html")
        shutil.copyfile(ROOT / "sitemap.xml",dest / "sitemap.xml")
        return dest

    def test_not_published_before_approved_date(self):
        with TemporaryDirectory() as t:
            out = self.destination(t)
            added = render_articles(out,today=date(2026,11,8),records=[self.story])
            self.assertEqual(added,set())
            self.assertNotIn("reviewed-demo-test", (out / "stories.html").read_text())
            self.assertFalse((out / "stories/reviewed-demo-test.html").exists())

    def test_publish_approved_article_and_archive_when_due(self):
        with TemporaryDirectory() as t:
            out = self.destination(t)
            added = render_articles(out,today=date(2026,11,9),records=[self.story])
            self.assertEqual(added,{"stories/reviewed-demo-test.html"})
            article=(out/"stories/reviewed-demo-test.html").read_text()
            index=(out/"stories.html").read_text()
            self.assertIn("learn/reviewed-demo-test.html",index)
            self.assertIn("stories/reviewed-demo-test.html",index)
            self.assertIn("../assets/theme.js",article)
            self.assertIn("Open supporting source",article)
            self.assertIn(self.story["review"]["review_url"],article)
            urls=[e.text for e in ET.parse(out/"sitemap.xml").iter() if e.tag.endswith("}loc")]
            self.assertIn("https://davidwpace.github.io/open-biomedical-resource-center/stories/reviewed-demo-test.html",urls)

    def test_invalid_record_cannot_be_published(self):
        fake = copy.deepcopy(self.story)
        fake.pop("review")
        with self.assertRaisesRegex(ValueError,"editorial review"):
            article_page(fake)

    def test_draft_always_excluded(self):
        fake=copy.deepcopy(self.story)
        fake["editorial_status"]="draft"
        with TemporaryDirectory() as t:
            added=render_articles(self.destination(t),today=date(2026,11,10),records=[fake])
            self.assertEqual(added,set())

    def test_html_escaping_for_new_content(self):
        fake=copy.deepcopy(self.story)
        fake["intro"]='<script>alert("bad")</script>'
        result=article_page(fake)
        self.assertNotIn('<script>alert("bad")</script>',result)
        self.assertIn('&lt;script&gt;',result)

    def test_newly_due_story_gets_first_feature(self):
        old=copy.deepcopy(self.story)
        old["slug"]="older-story"
        old["published_on"]="2026-11-06"
        self.assertEqual(daily_choice([old,self.story], date(2026,11,9))["slug"],self.story["slug"])

    def test_legacy_authored_story_cannot_be_rewritten(self):
        fake=copy.deepcopy(self.story)
        fake["slug"]="penicillin"
        with self.assertRaisesRegex(ValueError,"Preserve"):
            article_page(fake)


if __name__ == "__main__":
    unittest.main()
