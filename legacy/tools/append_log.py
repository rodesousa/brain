#!/usr/bin/env python3
"""Append une entrée au log.md avec la date du jour et un format strict.

Usage:
    python tools/append_log.py <action> "<details>"

Actions valides : init | ingest | query | lint | crystallize | update | note
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import VALID_ACTIONS, append_log_line, today_iso


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("action", choices=sorted(VALID_ACTIONS))
    p.add_argument("details", help="Description courte de l'opération")
    args = p.parse_args()

    append_log_line(args.action, args.details)
    print(f"  + ## [{today_iso()}] {args.action} | {args.details.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
