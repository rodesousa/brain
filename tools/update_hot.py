#!/usr/bin/env python3
"""Régénère hot.md — snapshot d'activité récente (7 derniers jours)."""
from __future__ import annotations

import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import (
    DRAFT_WARN_DAYS,
    HOT_MD,
    HOT_WINDOW_DAYS,
    days_since,
    iter_wiki_pages,
    read_log_entries,
    today_iso,
)


def main() -> int:
    cutoff = date.today() - timedelta(days=HOT_WINDOW_DAYS)
    pages = iter_wiki_pages(include_reports=False)
    log = [(d, a, det) for (d, a, det) in read_log_entries() if d >= cutoff]

    recent_sources = []
    page_touches: Counter[str] = Counter()
    for d, a, det in log:
        if a == "ingest":
            recent_sources.append(det)
        if a in ("ingest", "update", "crystallize"):
            page_touches[det[:80]] += 1

    drafts_old = []
    for p in pages:
        if p.fm.get("lifecycle") == "draft":
            d = days_since(p.fm.get("updated", ""))
            if d is not None and d >= HOT_WINDOW_DAYS:
                drafts_old.append((d, p))

    pages_recent = []
    for p in pages:
        d = days_since(p.fm.get("updated", ""))
        if d is not None and d <= HOT_WINDOW_DAYS:
            pages_recent.append((d, p))

    lines = [
        "# Hot — état actuel",
        "",
        f"_Snapshot du {today_iso()}, fenêtre {HOT_WINDOW_DAYS} jours._",
        "",
        f"## Sources récemment ajoutées ({len(recent_sources)})",
        "",
    ]
    if recent_sources:
        for s in recent_sources[-10:]:
            lines.append(f"- {s}")
    else:
        lines.append("_(aucune)_")
    lines.append("")

    lines.append(f"## Pages mises à jour récemment ({len(pages_recent)})")
    lines.append("")
    if pages_recent:
        for d, p in sorted(pages_recent, key=lambda x: x[0]):
            lc = p.fm.get("lifecycle", "")
            badge = f" `{lc}`" if lc else ""
            lines.append(f"- [[{p.slug}]]{badge} — il y a {d} j")
    else:
        lines.append("_(aucune)_")
    lines.append("")

    lines.append(f"## Drafts à relire (> {HOT_WINDOW_DAYS} j)")
    lines.append("")
    if drafts_old:
        for d, p in sorted(drafts_old, key=lambda x: -x[0]):
            lines.append(f"- [[{p.slug}]] — {d} j")
    else:
        lines.append("_(aucun)_")
    lines.append("")

    queries_recent = [det for d, a, det in log if a == "query"][-5:]
    if queries_recent:
        lines.append("## Queries récentes")
        lines.append("")
        for q in queries_recent:
            lines.append(f"- {q}")
        lines.append("")

    HOT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"  + hot.md régénéré ({len(pages_recent)} pages récentes, {len(drafts_old)} drafts vieillis)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
