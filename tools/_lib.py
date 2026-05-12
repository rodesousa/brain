"""Helpers partagés par les scripts du vault."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
WIKI = VAULT / "wiki"
RAW = VAULT / "raw"
REPORTS = WIKI / "reports"
INDEX_MD = VAULT / "index.md"
LOG_MD = VAULT / "log.md"
HOT_MD = VAULT / "hot.md"

VALID_ACTIONS = {"init", "ingest", "query", "lint", "crystallize", "update", "note"}
VALID_TYPES = {"entity", "concept", "source-summary", "comparison", "overview", "lint-report"}
VALID_LIFECYCLE = {"draft", "reviewed", "verified"}
TAG_BLACKLIST = {"ai", "llm", "agent", "tech", "notes", "startup", "interesting", "cool"}
MAX_TAGS = 5
MIN_TAGS = 3
DRAFT_WARN_DAYS = 14
HOT_WINDOW_DAYS = 7

REQUIRED_FM_FIELDS = ("type", "summary", "lifecycle", "created", "updated")

WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]")
LOG_ENTRY_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \| (.+)$")


@dataclass
class Page:
    path: Path
    fm: dict
    body: str

    @property
    def slug(self) -> str:
        return self.path.stem

    @property
    def rel(self) -> str:
        return str(self.path.relative_to(VAULT))


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parser YAML minimal pour notre schéma fixe (scalaires + listes simples)."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5:]
    fm: dict = {}
    current_list_key: str | None = None
    for line in raw.split("\n"):
        if not line.strip():
            current_list_key = None
            continue
        if line.lstrip().startswith("- ") and current_list_key:
            val = line.lstrip(" -").strip().strip('"').strip("'")
            fm[current_list_key].append(val)
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                fm[key] = []
                current_list_key = key
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                fm[key] = [s.strip().strip('"').strip("'") for s in inner.split(",")] if inner else []
                current_list_key = None
            else:
                fm[key] = val.strip('"').strip("'")
                current_list_key = None
    return fm, body


def iter_wiki_pages(include_reports: bool = False) -> list[Page]:
    pages: list[Page] = []
    if not WIKI.exists():
        return pages
    for p in sorted(WIKI.rglob("*.md")):
        if not include_reports and "reports" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        pages.append(Page(path=p, fm=fm, body=body))
    return pages


def all_vault_slugs() -> set[str]:
    """Tous les slugs (.md) de raw/ + wiki/, excluant les reports.

    Utilisé par le lint pour résoudre les wikilinks : une page wiki/ peut
    légitimement citer un fichier de raw/ (cluster file, source brute, etc.)
    sans que ce soit un lien cassé.
    """
    slugs: set[str] = set()
    for root in (WIKI, RAW):
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if "reports" in p.parts:
                continue
            slugs.add(p.stem)
    return slugs


def extract_wikilinks(body: str) -> list[str]:
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(body)]


def today_iso() -> str:
    return date.today().isoformat()


def days_since(iso: str) -> int | None:
    try:
        d = date.fromisoformat(iso)
    except (ValueError, TypeError):
        return None
    return (date.today() - d).days


def append_log_line(action: str, details: str) -> None:
    if action not in VALID_ACTIONS:
        raise ValueError(f"action invalide: {action} (valides: {sorted(VALID_ACTIONS)})")
    line = f"## [{today_iso()}] {action} | {details.strip()}"
    LOG_MD.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_MD.exists():
        LOG_MD.write_text("# Log\n\nJournal chronologique du wiki. Append-only.\n\n", encoding="utf-8")
    existing = LOG_MD.read_text(encoding="utf-8").rstrip()
    LOG_MD.write_text(existing + "\n" + line + "\n", encoding="utf-8")


def read_log_entries() -> list[tuple[date, str, str]]:
    if not LOG_MD.exists():
        return []
    out = []
    for line in LOG_MD.read_text(encoding="utf-8").splitlines():
        m = LOG_ENTRY_RE.match(line)
        if m:
            try:
                d = date.fromisoformat(m.group(1))
            except ValueError:
                continue
            out.append((d, m.group(2), m.group(3)))
    return out
