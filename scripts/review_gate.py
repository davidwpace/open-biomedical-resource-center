#!/usr/bin/env python3
"""Mechanical editorial safeguards for NEW public scientific stories.

This is a STRUCTURED-RECORD checker, not an AI reviewer or a fact checker.
An editor must compare claims with original sources and assess any expert
credentials. GitHub Issues are public, and a recorded URL is not proof of review.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
LEGACY = {"penicillin", "insulin"}
GITHUB_PREFIX = "https://github.com/davidwpace/open-biomedical-resource-center/"
EVIDENCE = {"historical", "peer_reviewed", "preprint", "mixed"}
RISK = {"educational", "preclinical", "clinical"}
ACCEPTED = {"supported", "qualified"}


def _handle(value: object) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,37})", value))


def _public_review_url(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith(GITHUB_PREFIX):
        return False
    tail = value[len(GITHUB_PREFIX):]
    return bool(re.fullmatch(r"(?:issues|pull)/[1-9][0-9]*", tail))


def evaluate_story(story: dict) -> list[str]:
    """Return failed prerequisites before a new approved story can be published."""
    errors = []
    slug = story.get("slug", "<missing slug>")
    status = story.get("editorial_status", "")
    if status == "draft":
        return errors
    if status == "" and slug in LEGACY:
        return errors  # Prior publication; not falsely labeled as externally reviewed.
    if status != "approved":
        return [f"{slug}: a new story must explicitly be approved or remain a draft"]

    review = story.get("review")
    if not isinstance(review, dict):
        return [f"{slug}: approved story lacks recorded human editorial review"]
    editor = review.get("editorial_approver")
    if not _handle(editor):
        errors.append(f"{slug}: editorial_approver must be a public GitHub handle")
    if review.get("editorial_decision") != "approve":
        errors.append(f"{slug}: no approving editorial decision")
    if not _public_review_url(review.get("review_url")):
        errors.append(f"{slug}: missing link to public evidence review Issue/PR")
    if review.get("conflicts_disclosed") is not True:
        errors.append(f"{slug}: editor must record conflicts disclosure")
    try:
        reviewed = date.fromisoformat(review["reviewed_on"])
        if reviewed != date.fromisoformat(story["reviewed_on"]):
            errors.append(f"{slug}: human review date and story review date differ")
    except (KeyError, TypeError, ValueError):
        errors.append(f"{slug}: invalid review date")
    evidence = review.get("evidence_class")
    if evidence not in EVIDENCE:
        errors.append(f"{slug}: missing evidence classification")
    risk = review.get("risk_tier")
    if risk not in RISK:
        errors.append(f"{slug}: missing scientific-risk tier")

    sources = {s.get("id") for s in story.get("sources", []) if isinstance(s, dict)}
    chapters = story.get("chapters", [])
    checks = review.get("claim_checks")
    if not isinstance(checks, list):
        checks = []
    checked = set()
    for i, claim in enumerate(checks):
        if not isinstance(claim, dict):
            errors.append(f"{slug}: claim check {i} is not an object")
            continue
        idx = claim.get("chapter")
        if not isinstance(idx, int) or isinstance(idx, bool) or not 0 <= idx < len(chapters):
            errors.append(f"{slug}: invalid chapter index in claim check {i}")
            continue
        checked.add(idx)
        if claim.get("source_id") not in sources:
            errors.append(f"{slug}: claim check {i} references nonexistent source")
        if claim.get("assessment") not in ACCEPTED:
            errors.append(f"{slug}: claim check {i} is not supported/qualified")
        if not isinstance(claim.get("source_location"), str) or len(claim["source_location"].strip()) < 6:
            errors.append(f"{slug}: claim check {i} lacks a specific source location")
        if not isinstance(claim.get("limitation"), str) or len(claim["limitation"].strip()) < 10:
            errors.append(f"{slug}: claim check {i} lacks an explicit limitation")
    if checked != set(range(len(chapters))):
        errors.append(f"{slug}: each chapter needs at least one source-located claim check")

    ai = review.get("ai_assistance")
    if not isinstance(ai, dict) or not isinstance(ai.get("used"), bool):
        errors.append(f"{slug}: disclose whether AI assisted with drafting/review")
    elif ai["used"] and not str(ai.get("tool", "")).strip():
        errors.append(f"{slug}: disclose the AI tool used")

    if risk == "clinical":
        expert = review.get("independent_expert_review")
        if not isinstance(expert, dict):
            errors.append(f"{slug}: clinical interpretation needs independent expert review")
        else:
            if expert.get("decision") != "approve":
                errors.append(f"{slug}: clinical expert did not approve")
            if not _handle(expert.get("reviewer")) or expert.get("reviewer") == editor:
                errors.append(f"{slug}: independent expert GitHub account must differ from editor")
            if not _public_review_url(expert.get("review_url")):
                errors.append(f"{slug}: expert review needs public audit link")
            if not str(expert.get("declared_expertise", "")).strip():
                errors.append(f"{slug}: expert must declare relevant expertise")
            if expert.get("conflicts_disclosed") is not True:
                errors.append(f"{slug}: expert must disclose conflicts")
    return errors


def validate_stories(records: list[dict]) -> tuple[list[str], int, int]:
    problems = []
    legacy = approved = 0
    for story in records:
        problems.extend(evaluate_story(story))
        if story.get("editorial_status") == "approved":
            approved += 1
        elif story.get("slug") in LEGACY and not story.get("editorial_status"):
            legacy += 1
    return problems, legacy, approved


def main() -> int:
    stories = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))["stories"]
    errors, legacy, approved = validate_stories(stories)
    if errors:
        for problem in errors:
            print("ERROR:", problem)
        print(f"FAIL: {len(errors)} editorial review prerequisite(s)")
        return 1
    print(f"REVIEW GATE PASSED: {legacy} legacy educational stories, {approved} new approvals with review records.")
    print("Note: structural checks do not verify source truth, actual reviewer identity or expertise.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
