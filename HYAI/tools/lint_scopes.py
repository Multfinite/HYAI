#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка контуров домена: секреты без носителя, закрытое в открытой выгрузке.

Набор проверок объявлен в `access.schema` домена (`checks[].kind`). Движок реализует
виды правил, домен выбирает, какие из них действуют.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh


def docs_of_domain(root: Path, man: dict, domain: str) -> list[tuple[str, dict]]:
    cfg = sh.domain_configs(root, man).get(domain) or {}
    data = cfg.get("data") or {}
    result: list[tuple[str, dict]] = []
    for base in data.get("root_paths") or []:
        directory = root / str(base)
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            rel = sh.rel_posix(root, path)
            meta, _ = sh.split_frontmatter(path.read_text(encoding="utf-8"))
            result.append((rel, meta))
    return result


def run_checks(root: Path, domain: str, model: dict) -> list[dict]:
    findings: list[dict] = []
    rules = model.get("rules") or {}
    secret_kinds = rules.get("secret_requires_known_by") or []
    presets = (model.get("export") or {}).get("presets") or {}

    for spec in model.get("checks") or []:
        kind = str(spec.get("kind") or "")
        severity = str(spec.get("severity") or "error")
        rule_id = str(spec.get("id") or kind)

        for rel, meta in docs_of_domain(root, sh.manifest(root), domain):
            if kind == "secret_without_known_by":
                knowledge = str(meta.get("knowledge") or "")
                if knowledge in secret_kinds and not meta.get("known_by"):
                    findings.append({"rule": rule_id, "severity": severity, "path": rel,
                                     "message": f"knowledge={knowledge!r} без known_by (NR-POL-11)"})
            elif kind == "open_visibility_with_secret":
                preset = str((spec.get("params") or {}).get("preset") or "")
                allowed = ((presets.get(preset) or {}).get("allow_visibility")) or []
                knowledge = str(meta.get("knowledge") or "")
                if meta.get("visibility") in allowed and knowledge in secret_kinds:
                    findings.append({"rule": rule_id, "severity": severity, "path": rel,
                                     "message": f"документ попадает в открытый пресет {preset!r}, но несёт {knowledge!r} (NR-POL-10)"})
            elif kind == "unknown_visibility":
                values = (model.get("visibility") or {}).get("values") or []
                if meta.get("visibility") and meta["visibility"] not in values:
                    findings.append({"rule": rule_id, "severity": severity, "path": rel,
                                     "message": f"контур {meta.get('visibility')!r} не объявлен в домене"})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка контуров домена")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--domain", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    cfg = sh.domain_configs(root, man).get(args.domain) or {}
    rel = ((cfg.get("data") or {}).get("access") or {}).get("schema")
    model = sh.load_yaml(root / str(rel)) if rel else {}
    if not model:
        print(f"нет модели доступа для домена {args.domain!r}", file=sys.stderr)
        return 2

    findings = run_checks(root, args.domain, model)
    errors = [f for f in findings if f["severity"] == "error"]

    if args.json:
        print(__import__("json").dumps({"findings": findings, "errors": len(errors)}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    for finding in findings:
        print(f"  [{finding['severity'].upper()}] {finding['path']} {finding['rule']}: {finding['message']}")
    print(f"\nконтуры домена {args.domain}: находок: {len(findings)}; ошибок: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
