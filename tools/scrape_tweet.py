#!/usr/bin/env python3
"""
scrape_tweet — récupère un tweet Nitter unique

Deps:
    pip install curl_cffi beautifulsoup4

Note: nitter.net filtre les clients sans empreinte TLS de browser.
On utilise curl_cffi (impersonation Firefox) pour passer ce filtre.

Usage:
    python scrape_tweet.py https://nitter.net/user/status/123456
    python scrape_tweet.py https://nitter.net/user/status/123 > tmp/tweet.json
"""

import json
import sys

from bs4 import BeautifulSoup
from curl_cffi import requests

IMPERSONATE = "firefox135"


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].startswith(("http://", "https://")):
        sys.stderr.write("Usage: python scrape_tweet.py <nitter-tweet-url>\n")
        return 1

    url = sys.argv[1]
    sys.stderr.write(f"📄 {url}\n")

    r = requests.get(url, impersonate=IMPERSONATE, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    main = soup.select_one(".main-tweet")
    if main is None:
        sys.stderr.write("❌ .main-tweet introuvable\n")
        return 1

    content_el = main.select_one(".tweet-content")
    username_el = main.select_one(".username")
    content = content_el.get_text(strip=True) if content_el else None
    username = username_el.get_text(strip=True).lstrip("@") if username_el else None

    if not content:
        sys.stderr.write("❌ Tweet vide\n")
        return 1

    output = {"content": content, "link": url, "source_username": username}
    sys.stderr.write(f"✅ tweet récupéré ({len(content)} chars)\n")
    sys.stdout.write(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
