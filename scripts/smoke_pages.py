#!/usr/bin/env python3
"""Check that the real GitHub Pages HTTPS site serves this validated release.

Run after actions/deploy-pages completes. The script requests only the site's
public static files and sends no credentials or patient information.
"""
from __future__ import annotations

import hashlib
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_FILES = (
    "index.html",
    "catalog.html",
    "start.html",
    "stories.html",
    "contribute.html",
    "review.html",
    "agent-access.html",
    "lab/braf-melanoma.html",
    "data/resources.json",
)
EXPECTED_PREFIX = "https://davidwpace.github.io/open-biomedical-resource-center/"


def get_page(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "OpenBiomedicalResourceCenter-DeploymentCheck/1.0"})
    with urlopen(request, timeout=12) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP status {response.status}")
        return response.read()


def run(base_url: str) -> int:
    url = base_url.rstrip("/") + "/"
    if not url.startswith(EXPECTED_PREFIX) or url != EXPECTED_PREFIX:
        print(f"ERROR: unexpected Pages URL: {url}", file=sys.stderr)
        return 1

    # Confirm files served by the public host are the *exact bytes* checked by
    # our CI. This detects stale or mismatched releases, not just 200 responses.
    for attempt in range(1, 6):
        problems: list[str] = []
        for name in PUBLIC_FILES:
            expected = (ROOT / name).read_bytes()
            target_url = urljoin(url, name)
            try:
                actual = get_page(target_url)
                if hashlib.sha256(actual).digest() != hashlib.sha256(expected).digest():
                    problems.append(f"{name}: public bytes do not yet match this commit")
                else:
                    print(f"OK: {name} ({len(actual):,} bytes)")
            except (HTTPError, URLError, OSError, TimeoutError, RuntimeError) as exc:
                problems.append(f"{name}: {type(exc).__name__}: {exc}")
        if not problems:
            print("PUBLIC HTTPS SMOKE CHECK PASSED: all files match the validated source.")
            return 0
        print(f"Public-site verification attempt {attempt}/5: {len(problems)} issue(s)")
        for problem in problems:
            print("  ", problem)
        if attempt < 5:
            time.sleep(6)

    print("ERROR: The public GitHub Pages site did not match the validated commit.", file=sys.stderr)
    print("A Pages deploy action can succeed while the public cache is still updating.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: smoke_pages.py https://davidwpace.github.io/open-biomedical-resource-center/", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(run(sys.argv[1]))
