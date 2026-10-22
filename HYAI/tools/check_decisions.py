#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка решений по областям (`decisions.scopes` в манифесте).

Проверяется: формат имени, дубли идентификаторов, обязательные поля, совпадение `scope`
с каталогом, существование путей из `affects`, целостность `supersedes`/`superseded_by`/
`merged_into`, бюджет строк, полнота индекса и принадлежность `affects` объявленным доменам.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка решений")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    cfg = man.get("decisions") or {}
    scopes = cfg.get("scopes") or {}
    if not scopes:
        print("в манифесте нет decisions.scopes", file=sys.stderr)
        return 2

    max_lines = int(cfg.get("max_lines") or 120)
    index_rel = str(cfg.get("index") or "meta/decisions/README.md")
    index_path = root / index_rel
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    errors: list[str] = []
    warnings: list[str] = []
    if not index_path.exists():
        errors.append(f"{index_rel}: индекс решений отсутствует (HYAI-DEC-13)")

    known: dict[str, dict] = {}
    per_scope_files: dict[str, list[Path]] = {s: [] for s in scopes}

    for scope, settings in scopes.items():
        settings = settings or {}
        prefix = str(settings.get("prefix") or "")
        directory = root / str(settings.get("dir") or "")
        if not prefix or not directory.exists():
            errors.append(f"решения: область {scope!r} без префикса или каталога")
            continue
        pattern = re.compile(rf"^{re.escape(prefix)}-(\d{{4}})-[a-z0-9][a-z0-9-]*\.md$")
        for path in sorted(directory.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            rel = sh.rel_posix(root, path)
            if not pattern.match(path.name):
                errors.append(f"{rel}: имя должно быть {prefix}-NNNN-slug.md")
                continue
            per_scope_files[scope].append(path)
            meta, body = sh.split_frontmatter(path.read_text(encoding="utf-8"))
            decision_id = path.name.split("-")[0] + "-" + path.name.split("-")[1]
            if decision_id in known:
                errors.append(f"{rel}: дубль идентификатора {decision_id} (HYAI-DEC-07)")
            known[decision_id] = {"meta": meta, "path": path, "scope": scope}

            if meta.get("id") and str(meta.get("id")).split(".")[-1] != decision_id:
                errors.append(f"{rel}: id={meta.get('id')!r} не совпадает с именем {decision_id}")
            if str(meta.get("scope") or "") != scope:
                errors.append(f"{rel}: scope={meta.get('scope')!r} не совпадает с каталогом области {scope!r} (HYAI-DEC-01)")

            targets = meta.get("affects") or []
            for target in targets:
                if not (root / str(target)).exists():
                    errors.append(f"{rel}: путь из affects не найден: {target} (HYAI-DEC-04)")

            affects_domains = meta.get("affects_domains") or []
            if len(affects_domains) > 1 and scope != "project":
                errors.append(f"{rel}: решение затрагивает несколько доменов — оно должно лежать в project (HYAI-DEC-02)")

            if meta.get("status") == "superseded" and not meta.get("superseded_by"):
                errors.append(f"{rel}: status=superseded требует superseded_by (HYAI-DEC-10)")
            if meta.get("status") == "merged" and not meta.get("merged_into"):
                errors.append(f"{rel}: status=merged требует merged_into (HYAI-DEC-10)")

            lines = len(body.strip().splitlines())
            if lines > max_lines:
                errors.append(f"{rel}: {lines} строк > бюджета {max_lines} (HYAI-DEC-11)")

            if index_text and decision_id not in index_text:
                errors.append(f"{rel}: не перечислен в {index_rel} (HYAI-DEC-13)")

    for decision_id, entry in known.items():
        for field in ("supersedes", "superseded_by", "merged_into"):
            target = entry["meta"].get(field)
            if target in (None, "", "null"):
                continue
            if field == "supersedes":
                refs = target if isinstance(target, list) else [target]
            else:
                refs = [target]
            for ref in refs:
                if str(ref) not in known:
                    errors.append(f"{entry['path'].name}: {field}={ref} указывает на несуществующее решение")

    if index_path.exists():
        for match in re.finditer(r"\[`?([A-Z]+-\d{4})`?\]\(([^)]+)\)", index_text):
            decision_id, link = match.group(1), match.group(2)
            target = (index_path.parent / link).resolve()
            if not target.exists():
                errors.append(f"{index_rel}: ссылка на несуществующий файл {link}")
            elif decision_id not in known:
                warnings.append(f"{index_rel}: строка {decision_id} без файла")

    if args.json:
        print(json.dumps({"decisions": len(known), "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 1 if errors or (args.strict and warnings) else 0

    for problem in errors:
        print(f"  {problem}")
    for problem in warnings:
        print(f"  WARN {problem}")
    print(f"\nрешения: ошибок: {len(errors)}; предупреждений: {len(warnings)}")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
