#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Согласованность названий lint-правил: документы ↔ `meta/lint/terms/*.json`.

Политика может обещать машинную проверку формулировкой «правило `X`».
Проверка: каждое такое имя существует в правилах домена (иначе обещание
невыполнимо — дефект P0). Названием считается и прямое упоминание id в обратных
кавычках (таблицы «Машинные проверки»). Обратное — правило определено, но ни разу не
названо в документах — предупреждение: такая норма невидима для агента.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

# Имя lint-правила: домен-префикс (2+ буквы) + точка + имя с дефисами.
# Без подчёркиваний — не ловит пути вида `lint_terms.py`; первый сегмент от двух
# букв — не ловит «e.g»/«i.e».
NAMED_PHRASE = re.compile(r"правил[ао]? `([a-z][\w.-]*)`")
ROOT_FILES = ("AGENTS.md", "CLAUDE.md", "README.md", "CHANGELOG.md")


TOOL_RULE_ID = re.compile(r"""["']([a-z][a-z0-9]+(?:-[a-z0-9]+)*\.[a-z][a-z0-9-]*(?:-[a-z0-9]+)*)["']""")


def defined_rules(root: Path) -> dict[str, str]:
    rules: dict[str, str] = {}
    core = sh.core_dir(root)
    terms_dir = core / "meta/lint/terms"
    for path in sorted(terms_dir.glob("*.json")) if terms_dir.exists() else []:
        data = sh.load_json(path)
        for rule in data.get("rules") or []:
            rid = str(rule.get("id") or "")
            if rid:
                rules[rid] = path.name
    # Структурные проверки несут те же id в строковых литералах скриптов
    # (например, pic.body-ref-not-deleted в check_picture_refs.py).
    file_ext = {"md", "py", "json", "yaml", "yml", "html", "txt", "js", "css", "webp", "png", "jpg"}
    for path in sorted((core / "tools").glob("*.py")):
        for rid in TOOL_RULE_ID.findall(path.read_text(encoding="utf-8", errors="replace")):
            if rid.split(".", 1)[1] in file_ext:
                continue  # имя файла, а не id правила
            rules.setdefault(rid, f"{core.name}/tools/{path.name}")
    return rules


def main() -> int:
    parser = argparse.ArgumentParser(description="Согласованность названий lint-правил")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    defined = defined_rules(root)

    md_files = [root / name for name in ROOT_FILES if (root / name).exists()]
    md_files.extend(p for p in sorted(root.rglob("*.md")) if ".git" not in p.parts)

    # 1) Названия по формулировке «правило/правила `X» с зарегистрированным
    #    доменным префиксом: ловит обещания проверок, игнорирует `lint_terms.py`
    #    и имена файлов.
    domain_prefixes = {rid.split(".", 1)[0] for rid in defined}
    named: set[str] = set()
    mentioned: set[str] = set()
    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for candidate in NAMED_PHRASE.findall(text):
            prefix = candidate.split(".", 1)[0]
            if "." in candidate and prefix in domain_prefixes:
                named.add(candidate)
        for rid in defined:
            if f"`{rid}`" in text:
                mentioned.add(rid)
    named |= mentioned

    missing = sorted(n for n in named if n not in defined)
    unused = sorted(n for n in defined if n not in named)

    if args.json:
        print(json.dumps({"missing": missing, "unused": unused}, ensure_ascii=False, indent=2))
    else:
        for name in missing:
            print(f"  [ERROR] названо в документах, но не определено в meta/lint/terms/*.json: {name}")
        for name in unused:
            print(f"  [WARN ] определено в {defined[name]}, но не названо ни в одном документе: {name}")
        print(f"названо: {len(named)}; определено: {len(defined)}; несуществующих: {len(missing)}; неназванных: {len(unused)}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
