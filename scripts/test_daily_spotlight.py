#!/usr/bin/env python3
"""Regression tests for source-reviewed daily-feature scheduling."""
from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_daily_spotlight import available_stories, daily_choice, render_spotlight  # noqa: E402


def sample(slug="sample", status="approved", published="2026-11-01"):
    return {
        "slug": slug,
        "editorial_status": status,
        "published_on": published,
        "reviewed_on": "2026-11-01",
        "title": "Example",
        "intro": "A verified educational sample",
        "original_year": 1900,
        "sources": [{"label": "Primary", "url": "https://example.org/1"},
                    {"label": "Secondary", "url": "https://example.org/2"}],
        "chapters": [{}, {}, {}],
    }


class TestDailySpotlight(unittest.TestCase):
    def test_future_story_does_not_show(self):
        self.assertEqual(available_stories([sample(published="2099-01-01")], date(2026, 11, 8)), [])

    def test_draft_not_featured(self):
        self.assertEqual(available_stories([sample(status="draft")], date(2026, 11, 8)), [])

    def test_new_story_must_be_approved(self):
        with self.assertRaisesRegex(ValueError, "explicit editorial_status"):
            available_stories([sample(status="")], date(2026, 11, 8))

    def test_approved_story_requires_review_date(self):
        s = sample()
        s["reviewed_on"] = ""
        with self.assertRaisesRegex(ValueError, "review date"):
            available_stories([s], date(2026, 11, 8))

    def test_missing_citations_fail(self):
        s = sample()
        s["sources"] = [{"url": "https://example.org"}]
        with self.assertRaisesRegex(ValueError, "Insufficient"):
            available_stories([s], date(2026, 11, 8))

    def test_selection_is_deterministic(self):
        stories = [sample(slug="b"), sample(slug="a")]
        first = daily_choice(stories, date(2026, 11, 8))
        repeat = daily_choice(list(reversed(stories)), date(2026, 11, 8))
        self.assertEqual(first["slug"], repeat["slug"])

    def test_current_reviewed_legacy_stories_generate_page(self):
        with TemporaryDirectory() as d:
            output = Path(d)
            assets = render_spotlight(output, today=date(2026, 11, 8))
            self.assertEqual(assets, {"today.html", "data/today.json"})
            html = (output / "today.html").read_text(encoding="utf-8")
            self.assertIn("Featured today", html)
            self.assertIn("2026-11-08", html)
            self.assertTrue((output / "data/today.json").is_file())


if __name__ == "__main__":
    unittest.main()
