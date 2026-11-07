#!/usr/bin/env python3
"""Regression tests for public science editorial sign-off prerequisites."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_gate import evaluate_story


def sample():
    return {
        "slug": "new-story", "editorial_status": "approved",
        "reviewed_on": "2026-11-07",
        "chapters": [{"body": "First"}, {"body": "Second"}, {"body": "Third"}],
        "sources": [{"id": "primary"}, {"id": "institution"}],
        "review": {
            "editorial_approver": "@research-editor",
            "editorial_decision": "approve",
            "reviewed_on": "2026-11-07",
            "review_url": "https://github.com/davidwpace/open-biomedical-resource-center/issues/11",
            "conflicts_disclosed": True,
            "evidence_class": "peer_reviewed", "risk_tier": "educational",
            "ai_assistance": {"used": True, "tool": "Model A (assistive only)"},
            "claim_checks": [
                {"chapter": i, "source_id": "primary", "assessment": "supported",
                 "source_location": "Figure 3B, page 8", "limitation": "Only one particular study cohort."}
                for i in range(3)
            ]
        }
    }


class ReviewGateTests(unittest.TestCase):
    def test_reviewed_educational_story(self):
        self.assertEqual(evaluate_story(sample()), [])

    def test_missing_editorial_review_fails(self):
        x=sample(); x.pop("review")
        self.assertTrue(any("lacks recorded" in m for m in evaluate_story(x)))

    def test_draft_ignores_approval_gate(self):
        x=sample(); x["editorial_status"]="draft"; x.pop("review")
        self.assertEqual(evaluate_story(x), [])

    def test_legacy_stays_eligible_without_false_peer_review_claim(self):
        x=sample(); x["slug"]="penicillin"; x.pop("editorial_status"); x.pop("review")
        self.assertEqual(evaluate_story(x), [])

    def test_unknown_new_story_without_status_fails(self):
        x=sample(); x.pop("editorial_status")
        self.assertTrue(any("explicitly be approved" in m for m in evaluate_story(x)))

    def test_each_chapter_needs_claim_support(self):
        x=sample(); x["review"]["claim_checks"].pop()
        self.assertTrue(any("each chapter" in m for m in evaluate_story(x)))

    def test_invalid_source_cannot_pass(self):
        x=sample(); x["review"]["claim_checks"][0]["source_id"]="nonexistent"
        self.assertTrue(any("nonexistent source" in m for m in evaluate_story(x)))

    def test_clinical_story_requires_different_expert(self):
        x=sample(); x["review"]["risk_tier"]="clinical"
        self.assertTrue(any("independent expert" in m for m in evaluate_story(x)))
        x["review"]["independent_expert_review"]={
            "reviewer":"@research-editor", "decision":"approve",
            "review_url":"https://github.com/davidwpace/open-biomedical-resource-center/issues/12",
            "declared_expertise":"Cancer biology", "conflicts_disclosed":True
        }
        self.assertTrue(any("differ from editor" in m for m in evaluate_story(x)))
        x["review"]["independent_expert_review"]["reviewer"]="@independent-expert"
        self.assertEqual(evaluate_story(x), [])

    def test_no_review_without_ai_disclosure(self):
        x=sample(); x["review"].pop("ai_assistance")
        self.assertTrue(any("disclose whether AI" in m for m in evaluate_story(x)))

    def test_no_unsupported_claim(self):
        x=sample(); x["review"]["claim_checks"][1]["assessment"]="unsupported"
        self.assertTrue(any("not supported/qualified" in m for m in evaluate_story(x)))


if __name__=="__main__":
    unittest.main()
