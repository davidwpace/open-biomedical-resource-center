#!/usr/bin/env python3
"""Prepare a minimal, verified GitHub Pages artifact from an explicit allowlist.

The public repository is intentionally broader than the published website:
the artifact excludes GitHub workflows, internal documentation and scripts.
No network access or third-party Python dependencies are required.
"""
from __future__ import annotations

import json
import posixpath
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "dist"
PROJECT_PREFIX = "/open-biomedical-resource-center/"
SITE_HOST = "davidwpace.github.io"

PUBLIC = (
    ".nojekyll",
    "index.html",
    "catalog.html",
    "agent-access.html",
    "start.html",
    "stories.html",
    "contribute.html",
    "llms.txt",
    "openapi.json",
    "sitemap.xml",
    "data/resources.json",
    "data/tool_routes.json",
    "data/stories.json",
    "assets/app.js",
    "assets/styles.css",
    "assets/guide.js",
    "assets/guide.css",
    "assets/story.js",
    "assets/story.css",
    "lab/braf-melanoma.html",
    "lab/demo.css",
    "lab/demo.js",
)


class LocalReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        props = dict(attrs)
        if props.get("id"):
            self.ids.add(props["id"])
        if tag in {"a", "link"} and props.get("href"):
            self.refs.append(props["href"])
        if tag in {"img", "script", "iframe", "source"} and props.get("src"):
            self.refs.append(props["src"])


def _safe_path(path: str) -> Path:
    if path.startswith("/") or "\" in path:
        raise ValueError(f"Unexpected absolute or backslash path: {path}")
    normalized = posixpath.normpath(path)
    if normalized in {".", ".."} or normalized.startswith("../"):
        raise ValueError(f"Unsafe path: {path}")
    result = ROOT / normalized
    if result.is_symlink():
        raise ValueError(f"Refusing symbolic link in published assets: {path}")
    if not result.is_file():
        raise ValueError(f"Missing public asset: {path}")
    return result


def _read_story_files() -> list[str]:
    data = json.loads((ROOT / "data/stories.json").read_text(encoding="utf-8"))
    files = []
    for record in data["stories"]:
        slug = record["slug"]
        if not slug or not slug.replace("-", "").isalnum():
            raise ValueError(f"Unsafe story slug: {slug!r}")
        files.append(f"stories/{slug}.html")
    return files


def _resolve_reference(page: str, ref: str) -> tuple[str | None, str | None]:
    """Return the local referenced path and optional fragment, or None for external URLs."""
    parts = urlsplit(ref.strip())
    if parts.scheme and parts.scheme not in {"http", "https"}:
        if parts.scheme in {"mailto", "tel"}:
            return None, None
        raise ValueError(f"{page}: unexpected URL scheme: {ref}")
    if parts.netloc and parts.netloc != SITE_HOST:
        return None, None
    if parts.netloc:
        if not parts.path.startswith(PROJECT_PREFIX):
            raise ValueError(f"{page}: absolute internal URL lacks project prefix: {ref}")
        target = parts.path[len(PROJECT_PREFIX):]
    elif parts.path.startswith("/"):
        if not parts.path.startswith(PROJECT_PREFIX):
            raise ValueError(f"{page}: root path lacks project prefix: {ref}")
        target = parts.path[len(PROJECT_PREFIX):]
    elif parts.path:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page), parts.path))
    else:
        target = page
    if target.endswith("/") or not target:
        target += "index.html"
    target = posixpath.normpath(target)
    if target.startswith("../") or target == "..":
        raise ValueError(f"{page}: path escapes public site: {ref}")
    return target, parts.fragment or None


def check_links(destination: Path, published: set[str]) -> None:
    errors: list[str] = []
    anchors: dict[str, set[str]] = {}
    references: dict[str, list[str]] = {}
    for path in sorted(published):
        if not path.endswith(".html"):
            continue
        html = (destination / path).read_text(encoding="utf-8")
        if "<html" not in html.lower() or "<main" not in html.lower():
            errors.append(f"{path}: missing HTML document/main landmark")
        parser = LocalReferences()
        parser.feed(html)
        anchors[path] = parser.ids
        references[path] = parser.refs

    for page, refs in references.items():
        for ref in refs:
            try:
                target, fragment = _resolve_reference(page, ref)
                if target is None:
                    continue
                if target not in published:
                    errors.append(f"{page}: reference to unpublished/missing file {ref} -> {target}")
                # Only validate target anchors for HTML. Some dynamic JavaScript
                # areas are intentionally populated after page load.
                if target in anchors and fragment and fragment not in anchors[target]:
                    errors.append(f"{page}: missing anchor #{fragment} in {target}")
            except ValueError as exc:
                errors.append(str(exc))

    if errors:
        raise ValueError("Public-site link validation failed:\n" + "\n".join(errors))


def main() -> int:
    story_files = _read_story_files()
    files = list(PUBLIC) + story_files
    if len(files) != len(set(files)):
        raise ValueError("Duplicate public asset paths")
    if DEST.is_symlink():
        raise ValueError("Refusing symlink as deployment destination")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    published: set[str] = set()
    for asset in files:
        origin = _safe_path(asset)
        target = DEST / asset
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin, target)
        published.add(asset)
    check_links(DEST, published)
    disallowed = (".github/", "docs/", "scripts/", "patients/", "clinical-records/")
    if any(p.startswith(disallowed) for p in published):
        raise ValueError("Sensitive or internal directory entered the Pages manifest")
    count = sum((DEST / p).stat().st_size for p in published)
    print(f"READY: {len(published)} allowlisted public files, {count:,} bytes")
    print("Excluded private-capable infrastructure: GitHub metadata, docs, scripts, issues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
