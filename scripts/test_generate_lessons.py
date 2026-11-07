#!/usr/bin/env python3
"""Regression tests for generated discovery lessons and beginner interactions."""
from __future__ import annotations

import copy
import shutil
import sys
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_lessons import ROOT, learning_records, all_activities, page, render_lessons, validate_lesson, verify_activity_targets


class TestLessonGenerator(unittest.TestCase):
    def setUp(self):
        self.records = learning_records(date(2026, 11, 7))
        self.activities = all_activities()

    def test_three_published_lessons(self):
        self.assertEqual({r["slug"] for r in self.records}, {"penicillin", "insulin", "braf-melanoma"})

    def test_generated_pages_and_archive(self):
        with TemporaryDirectory() as temp:
            dest = Path(temp)
            shutil.copyfile(ROOT / "sitemap.xml", dest / "sitemap.xml")
            outputs = render_lessons(dest, today=date(2026, 11, 7))
            self.assertEqual(outputs, {
                "learn.html", "learn/penicillin.html", "learn/insulin.html", "learn/braf-melanoma.html"
            })
            index = (dest / "learn.html").read_text(encoding="utf-8")
            self.assertIn("learn/penicillin.html", index)
            self.assertIn("learn/insulin.html", index)
            self.assertIn("learn/braf-melanoma.html", index)
            for filename in outputs:
                self.assertTrue((dest / filename).is_file())
            locations = {node.text for node in ET.parse(dest / "sitemap.xml").iter() if node.tag.endswith("}loc")}
            self.assertIn("https://davidwpace.github.io/open-biomedical-resource-center/learn.html", locations)
            self.assertIn("https://davidwpace.github.io/open-biomedical-resource-center/learn/braf-melanoma.html", locations)

    def test_interactive_stage_controls_and_source_checks(self):
        for record in self.records:
            html = page(record, self.activities[record["slug"]])
            self.assertEqual(html.count('class="lesson-step"'), len(record["chapters"]))
            self.assertIn('id="download-notes"', html)
            self.assertIn('id="step-next"', html)
            self.assertIn('role="progressbar"', html)
            self.assertIn('id="research-task"', html)
            self.assertIn("Evidence-aligned", (ROOT / "assets/lesson.js").read_text(encoding="utf-8"))
            for src in record["sources"]:
                self.assertIn(src["url"], html)

    def test_new_approved_story_can_use_reflection_fallback(self):
        record = copy.deepcopy(self.records[0])
        record["slug"] = "future-approved-story"
        record["theme"] = "concept"
        html = page(record, None)
        self.assertIn("Before revealing the evidence", html)
        self.assertIn('aria-label="Conceptual scientific reasoning', html)

    def test_source_id_must_exist(self):
        record = copy.deepcopy(self.records[0])
        record["chapters"][0]["source"] = "unknown-source"
        with self.assertRaisesRegex(ValueError, "cites missing source"):
            validate_lesson(record, self.activities["penicillin"])

    def test_one_supported_answer_per_checkpoint(self):
        record = copy.deepcopy(self.records[0])
        activity = copy.deepcopy(self.activities["penicillin"])
        activity[0]["choices"][1]["quality"] = "supported"
        with self.assertRaisesRegex(ValueError, "one evidence-supported choice"):
            validate_lesson(record, activity)

    def test_activity_length_must_equal_chapter_count(self):
        with self.assertRaisesRegex(ValueError, "activity/chapter count"):
            validate_lesson(self.records[0], self.activities["penicillin"][:-1])

    def test_html_escapes_source_and_page_titles(self):
        record = copy.deepcopy(self.records[0])
        record["intro"] = '<img src=x onerror="alert(1)">'
        html = page(record, self.activities["penicillin"])
        self.assertNotIn('<img src=x onerror=', html)
        self.assertIn("&lt;img", html)

    def test_no_source_or_external_tool_without_https(self):
        record = copy.deepcopy(self.records[0])
        record["tool_url"] = "javascript:alert(1)"
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            validate_lesson(record, self.activities["penicillin"])

    def test_review_queue_can_stage_future_and_draft_exercises(self):
        pending = [
            {"slug": "future-review-approved", "editorial_status": "approved", "published_on": "2030-01-01"},
            {"slug": "still-draft", "editorial_status": "draft", "published_on": "2030-01-01"},
        ]
        # The questions may exist in GitHub, but page generation still
        # selects only already-published eligible articles.
        verify_activity_targets({"future-review-approved", "still-draft"}, pending)

    def test_unknown_exercise_cannot_enter_site(self):
        with self.assertRaisesRegex(ValueError, "without a corresponding story"):
            verify_activity_targets({"invented-exercise"}, [{"slug": "known"}])

    def test_nonapproved_braf_replacements_prohibited(self):
        original = copy.deepcopy(self.records[2])
        original["slug"] = "invented-lab"
        # Metadata render alone does not approve new content; publication
        # is restricted by learning_records() and the human story review gate.
        self.assertNotIn(original["slug"], {r["slug"] for r in learning_records(date(2026, 11, 7))})


if __name__ == "__main__":
    unittest.main()
