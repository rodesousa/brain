#!/usr/bin/env python3
"""Vérifie les 7 règles de lint du schéma. Écrit un rapport daté.

Exit code : 1 si ≥1 erreur (block), 0 sinon (warnings ok).
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import (
    DRAFT_WARN_DAYS,
    MAX_TAGS,
    MIN_TAGS,
    REPORTS,
    REQUIRED_FM_FIELDS,
    TAG_BLACKLIST,
    VALID_LIFECYCLE,
    VALID_TYPES,
    VAULT,
    Page,
    all_vault_slugs,
    append_log_line,
    days_since,
    extract_wikilinks,
    iter_wiki_pages,
    today_iso,
)


def lint(pages: list[Page]) -> tuple[list[str], list[str]]:
    """Retourne (errors, warnings) sous forme de bullets markdown."""
    errors: list[str] = []
    warnings: list[str] = []

    by_slug: dict[str, Page] = {p.slug: p for p in pages}
    valid_targets = all_vault_slugs()  # raw/ + wiki/ — pour résolution des liens
    inbound: dict[str, set[str]] = defaultdict(set)

    for page in pages:
        for target in extract_wikilinks(page.body):
            if target in by_slug and target != page.slug:
                inbound[target].add(page.slug)

    for page in pages:
        rel = page.rel

        # 1. Frontmatter requis
        missing = [f for f in REQUIRED_FM_FIELDS if not page.fm.get(f)]
        if missing:
            errors.append(f"`{rel}` : frontmatter manquant — {', '.join(missing)}")

        t = page.fm.get("type", "").strip()
        if t and t not in VALID_TYPES:
            errors.append(f"`{rel}` : `type: {t}` invalide (valides : {sorted(VALID_TYPES)})")
        lc = page.fm.get("lifecycle", "").strip()
        if lc and lc not in VALID_LIFECYCLE:
            errors.append(f"`{rel}` : `lifecycle: {lc}` invalide (valides : {sorted(VALID_LIFECYCLE)})")

        # 2. Tags : count + blacklist
        tags = page.fm.get("tags", []) or []
        if isinstance(tags, list):
            if len(tags) > MAX_TAGS:
                errors.append(f"`{rel}` : {len(tags)} tags (max {MAX_TAGS})")
            elif 0 < len(tags) < MIN_TAGS:
                warnings.append(f"`{rel}` : {len(tags)} tags (min recommandé {MIN_TAGS})")
            forbidden = [t for t in tags if t.lower() in TAG_BLACKLIST]
            if forbidden:
                warnings.append(f"`{rel}` : tags interdits — {', '.join(forbidden)}")

        # 3. Liens cassés (résolus contre raw/ + wiki/)
        broken = [link for link in extract_wikilinks(page.body) if link not in valid_targets]
        for b in broken:
            errors.append(f"`{rel}` : lien cassé `[[{b}]]`")

        # 4. Forward sans reverse (uniquement entre pages wiki/, raw/ n'a pas vocation à back-référencer)
        forward_targets = {l for l in extract_wikilinks(page.body) if l in by_slug and l != page.slug}
        for target in forward_targets:
            target_page = by_slug[target]
            if page.slug not in extract_wikilinks(target_page.body):
                warnings.append(f"`{rel}` → `[[{target}]]` mais pas de retour `[[{page.slug}]]` dans `{target_page.rel}`")

        # 5. Drafts vieillis
        if lc == "draft":
            d = days_since(page.fm.get("updated", ""))
            if d is not None and d > DRAFT_WARN_DAYS:
                warnings.append(f"`{rel}` : draft depuis {d} jours (seuil {DRAFT_WARN_DAYS})")

    # 6. Orphelins (pages sans aucun lien entrant)
    for page in pages:
        if page.slug not in inbound:
            t = page.fm.get("type", "")
            # les "overview" et "source-summary" peuvent légitimement être orphelins racines
            if t not in ("overview", "source-summary"):
                warnings.append(f"`{page.rel}` : orphelin (aucun lien entrant)")

    # 7. Index drift — vérifié indirectement : on signale si index.md mentionne une page absente
    index_path = VAULT / "index.md"
    if index_path.exists():
        idx_text = index_path.read_text(encoding="utf-8")
        for link in extract_wikilinks(idx_text):
            if link not in valid_targets and not link.startswith("lint-"):
                warnings.append(f"`index.md` : référence `[[{link}]]` qui n'existe plus (lance `update_index.py`)")

    return errors, warnings


def render_report(pages: list[Page], errors: list[str], warnings: list[str]) -> str:
    lines = [
        "---",
        "type: lint-report",
        f"summary: Rapport de lint du {today_iso()} — {len(errors)} erreurs, {len(warnings)} warnings sur {len(pages)} pages.",
        f"created: {today_iso()}",
        f"updated: {today_iso()}",
        "lifecycle: verified",
        "tags: [lint, report]",
        "---",
        "",
        f"# Lint — {today_iso()}",
        "",
        "## Sommaire",
        "",
        f"- {len(pages)} pages dans `wiki/`",
        f"- **{len(errors)} erreurs** (block)",
        f"- {len(warnings)} warnings",
        "",
    ]
    if errors:
        lines.append("## Erreurs")
        lines.append("")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")
    if warnings:
        lines.append("## Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")
    if not errors and not warnings:
        lines.append("✓ Tout est propre.")
        lines.append("")
    lines.extend([
        "---",
        "",
        "_Lint mécanique — l'humain reste responsable du lint sémantique (contradictions entre pages, claims stales, synthèse à raffiner)._",
    ])
    return "\n".join(lines)


def main() -> int:
    pages = iter_wiki_pages(include_reports=False)
    errors, warnings = lint(pages)

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / f"lint-{today_iso()}.md"
    report_path.write_text(render_report(pages, errors, warnings), encoding="utf-8")

    print(f"  Pages : {len(pages)}")
    print(f"  Erreurs : {len(errors)}")
    print(f"  Warnings : {len(warnings)}")
    print(f"  Rapport : {report_path.relative_to(VAULT)}")
    if errors:
        print()
        print("ERREURS :")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print()
        print("WARNINGS :")
        for w in warnings[:10]:
            print(f"  ! {w}")
        if len(warnings) > 10:
            print(f"  … {len(warnings) - 10} autres dans le rapport")

    append_log_line("lint", f"{len(errors)} erreurs, {len(warnings)} warnings sur {len(pages)} pages")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
