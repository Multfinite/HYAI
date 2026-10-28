#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка терминов и паттернов по данным из `meta/lint/terms/*.json`.

Правило обязано иметь `id`, `severity`, `applies_to` и `reason`. Нет `applies_to` —
ошибка конфигурации (код 2): правило без зоны действия обязательно ударит по чужому домену.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

CODE_FENCE = re.compile(r"```.*?```", re.S)


def load_rules(root: Path, man: dict, domain: str | None) -> tuple[list[dict], list[str], list[str]]:
    rel_dir = (man.get("validation", {}).get("data") or {}).get("terms_dir") or "meta/lint/terms/"
    configs = sh.domain_configs(root, man)
    rules: list[dict] = []
    config_problems: list[str] = []
    searched: list[str] = []
    loaded_domains: set[str] = set()

    candidate_paths: list[Path] = []
    local_dir = sh.fw(root, str(rel_dir))
    if local_dir.exists():
        candidate_paths.extend(sorted(local_dir.glob("*.json")))

    for path in candidate_paths:
        config = sh.load_json(path)
        name = str(config.get("domain") or path.stem)
        loaded_domains.add(name)

    for dname, cfg in sorted(configs.items()):
        if dname in loaded_domains:
            continue
        for lint_rel in (cfg.get("data") or {}).get("lint") or []:
            resolved = sh.fw(root, str(lint_rel))
            if resolved.exists() and resolved not in candidate_paths:
                candidate_paths.append(resolved)

    for path in candidate_paths:
        config = sh.load_json(path)
        name = str(config.get("domain") or path.stem)
        if domain and name != domain:
            continue
        searched.append(sh.rel_posix(root, path))
        dom_cfg = configs.get(name) or {}
        template_roots = dom_cfg.get("template_root_paths") or []
        effective_roots = (dom_cfg.get("data") or {}).get("root_paths") or []
        default_scope = sh.rebase_globs(config.get("applies_to") or [], template_roots, effective_roots)
        for rule in config.get("rules") or []:
            missing = [f for f in ("id", "severity", "reason") if not rule.get(f)]
            raw_scope = rule.get("applies_to") or default_scope
            if not raw_scope:
                missing.append("applies_to")
            if missing:
                config_problems.append(f"{path.name}: правило {rule.get('id') or '?'} без полей {', '.join(missing)}")
                continue
            merged = dict(rule)
            merged["applies_to"] = sh.rebase_globs(raw_scope, template_roots, effective_roots)
            merged["domain"] = name
            rules.append(merged)
    return rules, config_problems, searched


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка терминов")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--domain", default=None, help="только правила указанного домена")
    parser.add_argument("--strict", action="store_true", help="предупреждения тоже ошибки")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    rules, config_problems, searched = load_rules(root, man, args.domain)

    if config_problems:
        for problem in config_problems:
            print(f"  {problem}")
        print(f"\nконфигурация правил: ошибок: {len(config_problems)}")
        return 2

    candidates = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {
        ".md", ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".sql", ".txt", ".yaml", ".yml", ".json"
    } and "__pycache__" not in p.parts and ".git" not in p.parts]

    findings: list[dict] = []
    for path in sorted(candidates):
        rel = sh.rel_posix(root, path)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        stripped = CODE_FENCE.sub("", text) if path.suffix.lower() == ".md" else text
        for rule in rules:
            if not sh.matches(rel, rule["applies_to"]):
                continue
            for match in re.finditer(str(rule.get("pattern") or ""), stripped, re.S | re.M):
                line = stripped.count("\n", 0, match.start()) + 1
                findings.append({
                    "rule": rule["id"],
                    "severity": rule.get("severity", "warn"),
                    "path": rel,
                    "line": line,
                    "snippet": strip_snippet(match.group(0)),
                    "suggest": rule.get("suggest"),
                })

    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] != "error"]

    if args.json:
        print(json.dumps({
            "configs": searched, "rules": len(rules),
            "findings": findings, "errors": len(errors), "warnings": len(warnings),
        }, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            mark = "ERR " if f["severity"] == "error" else "WARN"
            extra = f" → {f['suggest']}" if f.get("suggest") else ""
            print(f"  [{mark}] {f['path']}:{f['line']} {f['rule']}: {f['snippet']}{extra}")
        print(f"\nправил: {len(rules)}; ошибок: {len(errors)}; предупреждений: {len(warnings)}")
    return 1 if errors or (args.strict and warnings) else 0


def strip_snippet(text: str, limit: int = 60) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


if __name__ == "__main__":
    raise SystemExit(main())
