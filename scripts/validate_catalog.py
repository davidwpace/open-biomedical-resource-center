#!/usr/bin/env python3
"""Offline schema and content checks for the Open Biomedical Resource Center."""
from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "resources.json"
REQUIRED = {
    "id", "name", "category", "official_url", "access",
    "integration", "purpose", "limitations",
    "official_verification_url", "priority", "tags", "verified_on"
}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate() -> int:
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        print(f"ERROR: cannot read catalog: {exc}")
        return 1

    resources = data.get("resources")
    if not isinstance(resources, list) or not resources:
        print("ERROR: resources must be a non-empty list")
        return 1

    errors = []
    ids = set()
    for idx, record in enumerate(resources, 1):
        prefix = f"record {idx}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: expected object")
            continue
        missing = REQUIRED - record.keys()
        if missing:
            errors.append(f"{prefix}: missing {', '.join(sorted(missing))}")
        rid = record.get("id")
        if not isinstance(rid, str) or not SLUG.fullmatch(rid):
            errors.append(f"{prefix}: invalid slug {rid!r}")
        if rid in ids:
            errors.append(f"{prefix}: duplicate ID {rid!r}")
        ids.add(rid)
        for field in ["name", "category", "purpose", "access", "limitations", "integration"]:
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{prefix}: empty or invalid {field}")
        for field in ["official_url", "official_verification_url"]:
            value = record.get(field)
            url = urlparse(value) if isinstance(value, str) else None
            if not url or url.scheme != "https" or not url.netloc:
                errors.append(f"{prefix}: {field} must be an HTTPS URL")
        if not isinstance(record.get("tags"), list) or not all(isinstance(t, str) and t.strip() for t in record["tags"]):
            errors.append(f"{prefix}: tags must be nonempty strings in an array")
        if record.get("priority") not in {"P1", "P2", "P3"}:
            errors.append(f"{prefix}: priority must be P1/P2/P3")
        from datetime import date
        stamp = record.get("verified_on")
        try:
            if not isinstance(stamp, str) or not DATE.fullmatch(stamp):
                raise ValueError()
            date.fromisoformat(stamp)
        except ValueError:
            errors.append(f"{prefix}: invalid verified_on date")
    for problem in errors:
        print(f"ERROR: {problem}")
    if errors:
        print(f"FAILED: {len(errors)} issue(s) across {len(resources)} records")
        return 1
    counts = Counter(x["category"] for x in resources)
    print(f"OK: {len(resources)} records, {len(counts)} categories, all IDs unique")
    for name, count in sorted(counts.items()):
        print(f"  {name}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
