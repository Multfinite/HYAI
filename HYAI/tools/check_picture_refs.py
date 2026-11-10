#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Структурная проверка каталогов эталонов частей тела (`<picture_root>/refs/`).

Правило `pic.body-ref-not-deleted` (PIC-POL-12): эталоны не удаляются при чистке,
в каждом `refs/<part>/` обязан быть `README.md` («файл — что это — Drive id») и
только `webp`-файлы эталонов. Это проверка состояния каталога, а не текста,
поэтому она не входит в текстовые паттерны `lint_terms.py`: id правила
сохранён, выполняется здесь.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

RULE_ID = "pic.body-ref-not-deleted"


def run_checks(root: Path, domain: str) -> tuple[list[dict], int]:
    findings: list[dict] = []
    catalogs = 0
    cfg = sh.domain_configs(root, sh.manifest(root)).get(domain) or {}
    for base in (cfg.get("data") or {}).get("root_paths") or []:
        refs = root / str(base) / "refs"
        if not refs.is_dir():
            continue
        for part in sorted(p for p in refs.iterdir() if p.is_dir()):
            catalogs += 1
            if not (part / "README.md").is_file():
                findings.append({
                    "rule": RULE_ID, "severity": "error",
                    "path": sh.rel_posix(root, part),
                    "message": "нет README.md в каталоге эталонов (PIC-POL-12)",
                })
            for f in sorted(part.iterdir()):
                if f.is_file() and f.suffix.lower() not in (".webp", ".md"):
                    findings.append({
                        "rule": RULE_ID, "severity": "error",
                        "path": sh.rel_posix(root, f),
                        "message": "не-webp файл в каталоге эталонов; эталон — webp q95 (PIC-POL-12)",
                    })
    return findings, catalogs


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка каталогов эталонов частей тела")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--domain", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings, catalogs = run_checks(root, args.domain)

    if args.json:
        print(json.dumps({"findings": findings, "errors": len(findings)}, ensure_ascii=False, indent=2))
        return 1 if findings else 0
    if catalogs:
        print(f"каталоги эталонов {args.domain}: {catalogs}, проблем: {len(findings)}")
    else:
        print(f"каталоги эталонов {args.domain}: отсутствуют (проверка не требуется)")
    for finding in findings:
        print(f"  [{finding['severity'].upper()}] {finding['path']} {finding['rule']}: {finding['message']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
