#!/usr/bin/env python3
"""Bootstrappe la structure du vault. Idempotent — n'écrase rien."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import VAULT, WIKI, RAW, INDEX_MD, LOG_MD, HOT_MD, append_log_line


INDEX_TEMPLATE = """# Index

Catalogue du wiki. Régénéré par `tools/update_index.py`.

_(vide pour l'instant — lance `python tools/update_index.py` après ton premier ingest)_
"""

LOG_TEMPLATE = """# Log

Journal chronologique du wiki. Append-only. Format : `## [YYYY-MM-DD] action | details`.

"""

HOT_TEMPLATE = """# Hot — état actuel

_(régénéré par `tools/update_hot.py`)_
"""


def ensure_dir(p: Path) -> bool:
    if p.exists():
        return False
    p.mkdir(parents=True, exist_ok=True)
    return True


def ensure_file(p: Path, content: str) -> bool:
    if p.exists():
        return False
    p.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    created: list[str] = []
    for d in (RAW, WIKI):
        if ensure_dir(d):
            created.append(f"dir  {d.relative_to(VAULT)}/")
    for f, tpl in ((INDEX_MD, INDEX_TEMPLATE), (LOG_MD, LOG_TEMPLATE), (HOT_MD, HOT_TEMPLATE)):
        if ensure_file(f, tpl):
            created.append(f"file {f.relative_to(VAULT)}")

    if created:
        for c in created:
            print(f"  + {c}")
        append_log_line("init", f"Bootstrap : {len(created)} éléments créés")
    else:
        print("Vault déjà initialisé — rien à faire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
