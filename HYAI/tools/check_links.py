#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка ссылок в Markdown: `.md -> .md` и `.md -> код` (с якорем строки).

Все настройки — в `meta/lint/links.json`: расширения, исключения, шаблоны плейсхолдеров.
Исключение без `reason` — ошибка конфигурации (код возврата 2), а не тихий пропуск.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://", "data:", "#")


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text


def load_config(root: Path, man: dict) -> dict:
    rel = (man.get("validation", {}).get("data") or {}).get("links") or "meta/lint/links.json"
    config = sh.load_json(root / str(rel))
    return config or {"extensions": [".md"], "exclude": [], "ignore": []}


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка ссылок")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="считать предупреждения ошибками")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    config = load_config(root, man)

    ignore = config.get("ignore") or []
    without_reason = [entry for entry in ignore if not entry.get("reason")]
    if without_reason:
        print(json.dumps({"error": "ignore без reason", "entries": without_reason}, ensure_ascii=False, indent=2))
        return 2

    placeholders = [re.compile(p) for p in config.get("placeholder_patterns") or []]
    ignore_keys = {(entry.get("path"), entry.get("target")) for entry in ignore}
    exclude = list(config.get("exclude") or [])
    check_code = bool(config.get("check_code_targets", True))

    problems: list[dict] = []
    checked = 0
    for path in sh.iter_files(root, config.get("extensions") or [".md"]):
        rel = sh.rel_posix(root, path)
        if sh.matches(rel, exclude):
            continue
        text = strip_code(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(SKIP_SCHEMES):
                continue
            if any(p.search(target) for p in placeholders):
                continue
            if (rel, target) in ignore_keys:
                continue
            checked += 1
            base_target = urllib.parse.unquote(target.split("#", 1)[0])
            if not base_target:
                continue
            resolved = (root / base_target.lstrip("/")) if base_target.startswith("/") else (path.parent / base_target)
            if not resolved.exists():
                problems.append({"path": rel, "target": target, "reason": "файл не найден"})
                continue
            if resolved.suffix.lower() not in (config.get("extensions") or []) and not check_code:
                continue

    if args.json:
        print(json.dumps({"checked": checked, "problems": problems, "count": len(problems)}, ensure_ascii=False, indent=2))
        return 1 if problems else 0

    for problem in problems:
        print(f"  {problem['path']}: {problem['target']} — {problem['reason']}")
    print(f"\nСсылки: {len(problems)} битых (проверено {checked})")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
