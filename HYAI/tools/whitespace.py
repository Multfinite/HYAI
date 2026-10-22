#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка пробелов и концовки файла. Настройки — `meta/lint/whitespace.json`.

В `.md` разрешены ровно два пробела в конце строки: это CommonMark hard break.
Любые другие хвостовые пробелы и табы — ошибка; пустая строка в конце файла — тоже.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh


def check_text(rel: str, text: str, break_exts: set[str], forbid_eof_blank: bool) -> list[str]:
    problems: list[str] = []
    suffix = Path(rel).suffix.lower()
    if forbid_eof_blank and text.endswith("\n\n"):
        problems.append(f"{rel}: пустая строка в конце файла")
    for number, line in enumerate(text.split("\n"), 1):
        stripped = line.rstrip(" \t")
        if stripped == line:
            continue
        tail = line[len(stripped):]
        if suffix in break_exts and tail == "  ":
            continue
        problems.append(f"{rel}:{number}: хвостовой пробел или таб")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка пробелов")
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--stdin-paths", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    rel_cfg = (man.get("validation", {}).get("data") or {}).get("whitespace") or "meta/lint/whitespace.json"
    config = sh.load_json(root / str(rel_cfg)) or {}
    extensions = config.get("extensions") or [".md", ".py", ".json", ".yaml", ".yml"]
    break_exts = set(config.get("allow_two_space_break_in") or [])
    forbid_eof_blank = bool(config.get("forbid_blank_line_at_eof", True))

    if args.stdin_paths:
        raw = sys.stdin.buffer.read().split(b"\0")
        files = [Path(item.decode()) for item in raw if item]
    elif args.files:
        files = [f if f.is_absolute() else (root / f) for f in args.files]
    else:
        files = sh.iter_files(root, extensions, skip_parts=(".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"))

    problems: list[str] = []
    for path in files:
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        rel = sh.rel_posix(root, path)
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"{rel}: не UTF-8")
            continue
        problems.extend(check_text(rel, text, break_exts, forbid_eof_blank))

    for problem in problems:
        print(f"  {problem}")
    print(f"\nпробелы: проблем: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
