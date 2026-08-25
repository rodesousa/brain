#!/usr/bin/env python3
"""
scrape_profile — récupère les tweets d'un profil Nitter à partir de son URL

Deps:
    pip install curl_cffi beautifulsoup4

Note: nitter.net filtre les clients sans empreinte TLS de browser.
On utilise curl_cffi (impersonation Firefox) pour passer ce filtre.

Usage:
    python scrape_profile.py https://nitter.net/PhedEU
    python scrape_profile.py https://nitter.net/PhedEU --pages 10
    python scrape_profile.py https://nitter.net/PhedEU > tmp/phed.json
"""

import argparse
import json
import sys
import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests

IMPERSONATE = "firefox135"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape un profil Nitter")
    parser.add_argument("url", help="URL du profil Nitter (ex: https://nitter.net/foo)")
    parser.add_argument("--pages", type=int, default=5, help="Nombre max de pages (défaut: 5)")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if not parsed.scheme.startswith("http"):
        sys.stderr.write("❌ URL invalide\n")
        return 1
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        sys.stderr.write("❌ Impossible d'extraire le username depuis l'URL\n")
        return 1
    username = parts[0]
    origin = f"{parsed.scheme}://{parsed.netloc}"

    session = requests.Session(impersonate=IMPERSONATE)

    all_tweets: list[dict[str, str]] = []
    url = f"{origin}/{username}"

    for i in range(args.pages):
        sys.stderr.write(f"📄 Page {i + 1}: {url}\n")
        r = session.get(url, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        page_tweets = []
        for el in soup.select(".timeline-item"):
            content_el = el.select_one(".tweet-content")
            link_el = el.select_one(".tweet-link")
            content = content_el.get_text(strip=True) if content_el else None
            link = link_el.get("href") if link_el else None
            if content and link:
                page_tweets.append({"content": content, "link": link})

        sys.stderr.write(f"  → {len(page_tweets)} tweets\n")
        all_tweets.extend(page_tweets)

        next_href = None
        for a in soup.select(".show-more a"):
            href = a.get("href") or ""
            if "cursor" in href:
                next_href = href
                break
        if not next_href:
            break

        url = f"{origin}/{username}{next_href}" if next_href.startswith("?") else f"{origin}{next_href}"
        time.sleep(0.8)

    seen: dict[str, dict[str, str]] = {}
    for t in all_tweets:
        seen[t["link"]] = t

    output = [
        {
            "content": t["content"],
            "link": f"{origin}{t['link']}" if t["link"].startswith("/") else t["link"],
            "source_username": username,
        }
        for t in seen.values()
    ]

    sys.stderr.write(f"\n✅ {len(output)} tweets uniques\n")
    sys.stdout.write(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
