#!/usr/bin/env python3
"""Snapshot un repo GitHub dans raw/repos/<owner>-<repo>.md.

Récupère le README via l'API GitHub et l'écrit avec un frontmatter minimal.

Usage:
    python3 tools/snapshot_repo.py <github-url>
    python3 tools/snapshot_repo.py <github-url> --force   # écrase si le fichier existe
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import RAW, today_iso

URL_RE = re.compile(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")


def parse_url(url: str) -> tuple[str, str]:
    m = URL_RE.search(url.strip())
    if not m:
        raise ValueError(f"URL GitHub non reconnue : {url}")
    return m.group(1), m.group(2)


def fetch_readme(owner: str, repo: str) -> str:
    api = f"https://api.github.com/repos/{owner}/{repo}/readme"
    req = urllib.request.Request(api, headers={"Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("encoding") != "base64":
        raise RuntimeError(f"encoding inattendu : {data.get('encoding')}")
    return base64.b64decode(data["content"]).decode("utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url", help="URL du repo GitHub (https://github.com/owner/repo)")
    p.add_argument("--force", action="store_true", help="Écrase si le fichier existe déjà")
    args = p.parse_args()

    owner, repo = parse_url(args.url)
    out = RAW / "repos" / f"{owner}-{repo}.md"

    if out.exists() and not args.force:
        print(f"  ✗ {out.relative_to(RAW.parent)} existe déjà (utilise --force pour écraser)")
        return 1

    print(f"  fetching README de {owner}/{repo}...")
    readme = fetch_readme(owner, repo)

    body = (
        "---\n"
        f"repo: {owner}/{repo}\n"
        f"url: https://github.com/{owner}/{repo}\n"
        f"fetched_at: {today_iso()}\n"
        "---\n\n"
        + readme.rstrip() + "\n"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"  + {out.relative_to(RAW.parent)} ({len(readme)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
