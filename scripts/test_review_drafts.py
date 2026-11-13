import json,tempfile,unittest
from pathlib import Path
from generate_review_drafts import render,ROOT
from generate_feed import render as feed
class DraftPublicationTests(unittest.TestCase):
    def test_drafts_stay_unapproved_and_escape_content(self):
        d=json.loads((ROOT/"data/review_drafts.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            paths=render(Path(tmp),d)
            self.assertEqual(len(paths),6)
            for p in paths-{ "review-drafts.html" }:
                text=(Path(tmp)/p).read_text();self.assertIn("UNAPPROVED",text);self.assertIn('id="listen"',text);self.assertNotIn('<script>alert',text)
            d["records"][0]["story"]["editorial_status"]="approved"
            with self.assertRaises(ValueError):render(Path(tmp),d)
    def test_feed_excludes_review_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            feed(Path(tmp));text=(Path(tmp)/"feed.xml").read_text()
            self.assertIn("penicillin",text);self.assertNotIn("review-drafts/",text)
