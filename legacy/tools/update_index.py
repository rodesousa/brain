#!/usr/bin/env python3
"""Régénère index.md à partir des frontmatters des pages du wiki.

L'index est une vue dérivée — la source de vérité reste les pages elles-mêmes.
Lancer après chaque ingest ou crystallize.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import INDEX_MD, VAULT, WIKI, append_log_line, iter_wiki_pages, today_iso

TYPE_ORDER = ["overview", "entity", "concept", "comparison", "source-summary"]
TYPE_LABELS = {
    "overview": "Vues d'ensemble",
    "entity": "Entités",
    "concept": "Concepts",
    "comparison": "Comparaisons",
    "source-summary": "Sources",
}


def main() -> int:
    pages = iter_wiki_pages(include_reports=False)
    by_type: dict[str, list] = defaultdict(list)
    untyped = []
    for page in pages:
        t = page.fm.get("type", "").strip()
        if t in TYPE_LABELS:
            by_type[t].append(page)
        else:
            untyped.append(page)

    out: list[str] = ["# Index", "", f"_Régénéré le {today_iso()} — {len(pages)} pages._", ""]

    for t in TYPE_ORDER:
        out.append(f"## {TYPE_LABELS[t]}")
        out.append("")
        if not by_type[t]:
            out.append("_(aucune)_")
        else:
            for page in sorted(by_type[t], key=lambda p: p.slug):
                summary = page.fm.get("summary", "").strip()
                lifecycle = page.fm.get("lifecycle", "").strip()
                badge = f" `{lifecycle}`" if lifecycle and lifecycle != "verified" else ""
                line = f"- [[{page.slug}]]{badge}"
                if summary:
                    line += f" — {summary}"
                out.append(line)
        out.append("")

    if untyped:
        out.append("## Sans type")
        out.append("")
        for page in sorted(untyped, key=lambda p: p.slug):
            out.append(f"- [[{page.slug}]] — _frontmatter `type:` manquant ou invalide_")
        out.append("")

    INDEX_MD.write_text("\n".join(out), encoding="utf-8")
    print(f"  + index.md régénéré ({len(pages)} pages)")
    append_log_line("update", f"index.md régénéré ({len(pages)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
