#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка отчётов: домен, профиль, вид, разделы, ссылки на решения, индекс.

Всё берётся из `HYAI/meta/manifest.yaml` и доменных манифестов: списка процессов нет в коде,
поэтому новый процесс не может «не пройти проверку только потому, что о нём забыли».
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def known_workflows(root: Path, man: dict) -> set[str]:
    names: set[str] = set()
    kernel_dir = root / str((man.get("paths") or {}).get("kernel") or "HYAI/core/kernel/") / "workflows"
    if kernel_dir.exists():
        names.update(p.stem for p in kernel_dir.glob("*.md") if p.stem.lower() != "readme")
    for domain, cfg in sh.domain_configs(root, man).items():
        wf_rel = cfg["data"].get("workflows_dir")
        if not wf_rel:
            continue
        wf_dir = root / str(wf_rel)
        if wf_dir.exists():
            for path in wf_dir.glob("*.md"):
                if path.stem.lower() != "readme":
                    names.add(f"{domain}/{path.stem}")
    return names


def decision_ids(root: Path, man: dict) -> set[str]:
    ids: set[str] = set()
    for scope, settings in ((man.get("decisions") or {}).get("scopes") or {}).items():
        directory = root / str((settings or {}).get("dir") or "")
        prefix = str((settings or {}).get("prefix") or "")
        if not directory.exists():
            continue
        for path in directory.glob("*.md"):
            match = re.match(rf"^({re.escape(prefix)}-\d{{4}})-", path.name)
            if match:
                ids.add(match.group(1))
    return ids


def section_body(body: str, title: str) -> str | None:
    matches = list(HEADING_RE.finditer(body))
    for index, match in enumerate(matches):
        if match.group(1).strip() != title:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        return body[match.end():end].strip()
    return None


def check_one(root: Path, man: dict, path: Path, ctx: dict) -> list[str]:
    rel = sh.rel_posix(root, path)
    problems: list[str] = []
    scope = sh.resolve_scope(root, man, rel)
    if not path.name.lower() == "readme.md" and not NAME_RE.match(path.name):
        problems.append(f"{rel}: имя должно быть YYYY-MM-DD-slug.md")
    text = path.read_text(encoding="utf-8")
    meta, body = sh.split_frontmatter(text)
    if not meta:
        return problems + [f"{rel}: нет frontmatter"]

    report_cfg = man.get("report") or {}
    for field in report_cfg.get("required_fields") or []:
        if not meta.get(field):
            problems.append(f"{rel}: нет обязательного поля `{field}` (HYAI-ART-02)")

    if meta.get("type") != "report":
        problems.append(f"{rel}: type={meta.get('type')!r}, ожидалось report")
    if meta.get("date") and not DATE_RE.match(str(meta["date"])):
        problems.append(f"{rel}: date должен быть YYYY-MM-DD")

    if meta.get("domain") and scope and str(meta["domain"]) != str(scope):
        problems.append(f"{rel}: domain={meta['domain']!r} не совпадает с каталогом области {scope!r} (HYAI-ART-01)")
    if scope and scope not in (report_cfg.get("allowed_scopes") or []):
        problems.append(f"{rel}: область {scope!r} не разрешена для отчётов")
    active = {d for d, _ in sh.active_pairs(man)}
    if scope in (man.get("domains") or {}) and scope not in active:
        problems.append(f"{rel}: домен {scope!r} не активен в манифесте")

    kind = str(meta.get("report_kind") or "")
    kinds = report_cfg.get("kinds") or {}
    if kind not in kinds:
        problems.append(f"{rel}: report_kind={kind!r} недопустим (допустимо: {', '.join(kinds)})")
    else:
        for title in (kinds[kind] or {}).get("required_sections") or []:
            content = section_body(body, title)
            if content is None:
                problems.append(f"{rel}: нет раздела «## {title}» (HYAI-ART-04)")
            elif not content:
                problems.append(f"{rel}: раздел «## {title}» пуст")

    workflow = str(meta.get("workflow") or "")
    if workflow and workflow not in ctx["workflows"]:
        problems.append(f"{rel}: неизвестный workflow {workflow!r} (нет такого процесса в ядре или активных доменах)")

    profile = str(meta.get("profile") or "")
    if profile and scope:
        expected_prefix = f"{scope}/"
        if not profile.startswith(expected_prefix):
            problems.append(f"{rel}: profile={profile!r} должен принадлежать домену {scope!r} ({expected_prefix}…)")
        else:
            cfg = sh.profile_config(root, sh.domain_configs(root, man).get(scope, {}), profile[len(expected_prefix):])
            if not cfg:
                problems.append(f"{rel}: профиль {profile!r} не объявлен в домене {scope!r}")

    cross = meta.get("cross_scope")
    if cross is not None:
        if not isinstance(cross, list) or not cross:
            problems.append(f"{rel}: cross_scope должен быть непустым списком (HYAI-ART-14)")
        else:
            for entry in cross:
                if not isinstance(entry, dict) or not entry.get("path") or not entry.get("why"):
                    problems.append(f"{rel}: в cross_scope нужны path и why (HYAI-ART-14)")
                    break

    for ref in meta.get("decisions") or []:
        if not isinstance(ref, str):
            problems.append(f"{rel}: decisions содержит не строку ({ref!r}); номер в кавычках (HYAI-DEC-05)")
            continue
        if ref not in ctx["decisions"]:
            problems.append(f"{rel}: решение {ref} не найдено в meta/decisions")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка отчётов")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    report_cfg = man.get("report") or {}
    index_rel = str(report_cfg.get("index") or "HYAI/meta/reports/README.md")
    index_text = (root / index_rel).read_text(encoding="utf-8") if (root / index_rel).exists() else ""

    skip_dirs = {(man.get("paths") or {}).get("plans"), (man.get("paths") or {}).get("archive")}
    if args.paths:
        paths = [Path(p) for p in args.paths]
    else:
        reports_root = root / str((man.get("paths") or {}).get("reports") or "HYAI/meta/reports/")
        paths = []
        for scope in report_cfg.get("allowed_scopes") or []:
            directory = reports_root / str(scope)
            if not directory.exists():
                continue
            paths.extend(sorted(p for p in directory.glob("*.md") if p.name.lower() != "readme.md"))

    ctx = {"workflows": known_workflows(root, man), "decisions": decision_ids(root, man)}
    problems: list[str] = []
    for path in paths:
        rel = sh.rel_posix(root, path)
        if any(str(part) and f"/{part}/" in f"/{rel}" for part in skip_dirs):
            continue
        problems.extend(check_one(root, man, path, ctx))
        entry = f"({path.name})"
        if index_text and path.name not in index_text:
            problems.append(f"{rel}: отчёт отсутствует в {index_rel} (HYAI-ART-13)")

    if args.json:
        print(__import__("json").dumps({"checked": len(paths), "problems": problems}, ensure_ascii=False, indent=2))
        return 1 if problems else 0
    for problem in problems:
        print(f"  {problem}")
    print(f"\nотчётов: {len(paths)}; проблем: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
