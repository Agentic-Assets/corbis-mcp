#!/usr/bin/env python3
"""Observe a public skills.sh collection; not a content or search-index check."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

SOURCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_BYTES = 2_000_000
ATTEMPTS = 4
RETRY_SECONDS = 15


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class CollectionParser(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source.lower()
        self.in_heading = False
        self.heading = []
        self.headings = []
        self.slugs = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.in_heading = True
            self.heading = []
        if tag == "a":
            href = attrs.get("href", "")
            prefix = f"/{self.source}/"
            if href.lower().startswith(prefix):
                slug = href[len(prefix):]
                if SLUG.fullmatch(slug):
                    self.slugs.add(slug)

    def handle_endtag(self, tag):
        if tag == "h1" and self.in_heading:
            self.headings.append("".join(self.heading).strip().lower())
            self.in_heading = False

    def handle_data(self, data):
        if self.in_heading:
            self.heading.append(data)


def inventory(root):
    skills = root / "skills"
    if skills.is_symlink() or not skills.is_dir():
        raise ValueError("skills directory is missing or symlinked")
    names = set()
    for entry in skills.iterdir():
        if entry.is_symlink():
            raise ValueError("symlinked skill entry")
        if not entry.is_dir():
            continue
        skill = entry / "SKILL.md"
        if skill.is_symlink():
            raise ValueError("symlinked skill file")
        if skill.is_file():
            if not SLUG.fullmatch(entry.name):
                raise ValueError("invalid skill name")
            names.add(entry.name)
    if not names:
        raise ValueError("empty skill inventory")
    return names


def classify(html, source, expected):
    parser = CollectionParser(source)
    parser.feed(html)
    parser.close()
    # A source heading plus at least one skill link signals a recognized page;
    # an empty or changed layout is unknown, not evidence all skills are absent.
    if source.lower() not in parser.headings or not parser.slugs:
        return "unknown", set(), set(expected)
    visible = expected & parser.slugs
    pending = expected - visible
    return ("pending" if pending else "visible"), visible, pending


def observe(source, expected, opener=None):
    if not SOURCE.fullmatch(source):
        raise ValueError("source must be a GitHub owner/repository")
    opener = opener or build_opener(NoRedirect())
    req = Request(f"https://www.skills.sh/{source.lower()}", headers={"Accept": "text/html", "User-Agent": "skills-collection-observer/1.0"})
    try:
        with opener.open(req, timeout=20) as response:
            if response.status != 200 or response.headers.get_content_type() != "text/html":
                return "unknown", set(), set(expected)
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                return "unknown", set(), set(expected)
            html = body.decode("utf-8", errors="strict")
        return classify(html, source, expected)
    except HTTPError as exc:
        exc.close()
        return "unknown", set(), set(expected)
    except (URLError, OSError, TimeoutError, UnicodeError, ValueError):
        return "unknown", set(), set(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        expected = inventory(args.root)
        if not SOURCE.fullmatch(args.source):
            raise ValueError("source must be a GitHub owner/repository")
    except ValueError as exc:
        print(f"unknown: {exc}", file=sys.stderr)
        return 2
    for attempt in range(ATTEMPTS):
        state, visible, remainder = observe(args.source, expected)
        print(f"attempt {attempt + 1}/{ATTEMPTS}: {state}", flush=True)
        if state == "visible":
            break
        if attempt + 1 < ATTEMPTS:
            time.sleep(RETRY_SECONDS)
    print("observed:", ", ".join(sorted(visible)) or "none")
    if remainder:
        print(("pending" if state == "pending" else "unknown") + ":", ", ".join(sorted(remainder)))
    print("Observation of public collection links only; content revision and search are not verified.")
    return {"visible": 0, "pending": 1, "unknown": 2}[state]


if __name__ == "__main__":
    sys.exit(main())
