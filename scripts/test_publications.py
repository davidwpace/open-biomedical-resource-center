import copy
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from generate_review_drafts import ROOT
from generate_publications import render
from sync_prepared_articles import import_issues, OWNER, REPOSITORY

FENCE = chr(96) * 3
def issue_body(story):
    return FENCE + "json\n" + json.dumps(story) + "\n" + FENCE

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "data/review_drafts.json").read_text())
        self.story = copy.deepcopy(self.data["records"][0]["story"])
        self.story["slug"] = "new-owner-story"
        self.issue = {"number": 999, "title": "EDITORIAL DRAFT — New story",
                      "user": {"login": OWNER}, "html_url": f"https://github.com/{REPOSITORY}/issues/999",
                      "body": issue_body(self.story),
                      "created_at": "2026-11-16T09:00:00Z", "updated_at": "2026-11-16T09:00:00Z"}

    def test_intake_is_idempotent_and_does_not_approve(self):
        first, added, held = import_issues(self.data, [self.issue], as_of="2026-11-16")
        second, again, held_again = import_issues(first, [self.issue], as_of="2026-11-17")
        self.assertEqual(added, ["new-owner-story"])
        self.assertEqual(held, [])
        self.assertEqual(again, [])
        self.assertEqual(first, second)
        self.assertEqual(second["records"][-1]["story"]["editorial_status"], "draft")
        self.assertEqual(len(second["records"][-1]["source_snapshot_sha256"]), 64)
        self.assertNotIn("published_on", second["records"][-1]["story"])

    def test_nonowner_and_wrong_repository_are_held(self):
        for issue in [dict(self.issue, user={"login": "someone-else"}), dict(self.issue, html_url="https://github.com/another/repo/issues/999")]:
            result, added, held = import_issues(self.data, [issue])
            self.assertEqual(added, [])
            self.assertEqual(result, self.data)
            self.assertEqual(len(held), 1)

    def test_incomplete_and_approval_claiming_inputs_are_held(self):
        for change in [{"editorial_status": "approved"}, {"sources": []}, {"slug": "../private"}, {"chapters": [{"title":"No source"}]}]:
            issue = dict(self.issue, body=issue_body(dict(self.story, **change)))
            result, added, held = import_issues(self.data, [issue])
            self.assertEqual(added, [])
            self.assertEqual(len(held), 1)

    def test_existing_curated_record_cannot_be_overwritten(self):
        issue = dict(self.issue, number=self.data["records"][0]["issue_number"])
        result, added, held = import_issues(self.data, [issue])
        self.assertEqual(result, self.data)
        self.assertEqual(added, [])

    def test_exports_feed_and_manifest_agree_and_keep_review_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            (dest / "data").mkdir()
            (dest / "sitemap.xml").write_text((ROOT / "sitemap.xml").read_text())
            paths = render(dest)
            entries = json.loads((dest / "data/publications.json").read_text())["articles"]
            feed = ET.parse(dest / "articles-feed.xml").getroot().findall("./channel/item")
            self.assertEqual(len(feed), len(entries))
            self.assertEqual(len({x["slug"] for x in entries}), len(entries))
            for entry, item in zip(entries, feed):
                text = (dest / entry["export_path"]).read_text()
                self.assertIn(entry["title"], text)
                self.assertIn(entry["url"], text)
                self.assertIn(entry["status"], item.findtext("title"))
                self.assertIn(entry["export_path"], paths)
                if entry["kind"] == "draft":
                    self.assertIn("review pending", text)
            self.assertIn("EoD", (dest / "articles/biological-compilation-amplified-individual.html").read_text())

    def test_manuscript_text_is_preserved_and_citations_link_to_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            (dest / "data").mkdir()
            (dest / "sitemap.xml").write_text((ROOT / "sitemap.xml").read_text())
            render(dest)
            text = (dest / "articles/biological-compilation-amplified-individual.html").read_text()
            self.assertIn("A tape measure does not become less useful", text)
            self.assertIn('href="#source-R1"', text)
            self.assertIn('id="source-R1"', text)
            self.assertIn("FDA documents cited here are drafts", text)

if __name__ == "__main__":
    unittest.main()

