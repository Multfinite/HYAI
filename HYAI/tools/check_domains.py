#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Метавалидатор структуры доменов и профилей.

Проверяет то, что нельзя проверить «по смыслу»: полноту файлов, зоны, право расширять
другие домены, отсутствие прав в профилях и чистоту движков от доменных имён.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

REQUIRED_DOMAIN_FIELDS = ("metadata", "root_paths", "authority", "access", "policy", "agents", "registry", "profiles")
REQUIRED_PROFILE_FIELDS = ("topic", "scope_primary", "workflow", "produced_artifacts")


def check_domain(root: Path, name: str, cfg: dict) -> list[str]:
    problems: list[str] = []
    data = cfg["data"]
    base = cfg["rel"]
    if not data:
        return [f"{base}: не читается"]
    for field in REQUIRED_DOMAIN_FIELDS:
        if not data.get(field):
            problems.append(f"{base}: нет обязательного поля `{field}` (KIT-POL-04)")

    if str((data.get("metadata") or {}).get("name")) != name:
        problems.append(f"{base}: metadata.name не совпадает с именем домена {name!r}")
    if name not in data.get("root_paths", []) and not data.get("root_paths"):
        problems.append(f"{base}: пустой root_paths (KIT-POL-06)")

    for key in ("policy", "agents"):
        rel = data.get(key)
        if rel and not sh.fw(root, str(rel)).exists():
            problems.append(f"{base}: {key} указывает на несуществующий файл: {rel}")
    for group in ("authority", "access"):
        rel = (data.get(group) or {}).get("doc")
        schema = (data.get(group) or {}).get("schema")
        if rel and not sh.fw(root, str(rel)).exists():
            problems.append(f"{base}: {group}.doc не найден: {rel}")
        if schema and not sh.fw(root, str(schema)).exists():
            problems.append(f"{base}: {group}.schema не найден: {schema}")
    overlay = data.get("schema")
    if overlay and not sh.fw(root, str(overlay)).exists():
        problems.append(f"{base}: schema-оверлей не найден: {overlay}")
    for rel in data.get("lint") or []:
        if not sh.fw(root, str(rel)).exists():
            problems.append(f"{base}: правило терминов не найдено: {rel}")

    profiles = data.get("profiles") or {}
    if not profiles:
        problems.append(f"{base}: домен без профилей (KIT-POL-08)")

    zones: dict[tuple[str, ...], str] = {}
    for profile, rel in profiles.items():
        p_cfg_path = sh.fw(root, str(rel))
        if not p_cfg_path.exists():
            problems.append(f"{base}: профиль {profile!r} — файл не найден: {rel}")
            continue
        p = sh.profile_config(root, cfg, profile)
        problems.extend(check_profile(root, name, profile, p, p_cfg_path))
        key = tuple(sorted(p.get("scope_primary") or []))
        if key and key in zones:
            problems.append(f"{rel}: зона профиля {profile!r} совпадает с {zones[key]!r} — профили дублируются (KIT-POL-08)")
        elif key:
            zones[key] = profile
    return problems


def check_profile(root: Path, domain: str, profile: str, p: dict, path: Path) -> list[str]:
    problems: list[str] = []
    rel = sh.rel_posix(root, path)
    for field in REQUIRED_PROFILE_FIELDS:
        if not p.get(field):
            problems.append(f"{rel}: нет поля `{field}` (KIT-POL-08)")
    if "permissions" in p:
        problems.append(f"{rel}: профиль не задаёт права — поле `permissions` запрещено (KIT-POL-09)")
    if str((p.get("metadata") or {}).get("domain")) != domain:
        problems.append(f"{rel}: metadata.domain не совпадает с доменом {domain!r}")

    checklist = p.get("checklist") or []
    if len(checklist) < 3:
        problems.append(f"{rel}: чек-лист короче трёх вопросов — профиль не самодостаточен")
    if not (p.get("definition_of_done") or []):
        problems.append(f"{rel}: пустой definition_of_done — профиль превратится в пожелание")

    workflow = str(p.get("workflow") or "")
    man = sh.manifest(root)
    if workflow and "/" in workflow:
        wf_domain, wf_name = workflow.split("/", 1)
        dom = sh.domain_configs(root, man).get(wf_domain) or {}
        wf_dir = sh.fw(root, str((dom.get("data") or {}).get("workflows_dir") or ""))
        if not (wf_dir / f"{wf_name}.md").exists():
            problems.append(f"{rel}: процесс {workflow!r} не найден")
    elif workflow:
        kernel_dir = sh.fw(root, str((man.get("paths") or {}).get("kernel") or "HYAI/core/kernel/"))
        if not (kernel_dir / "workflows" / f"{workflow}.md").exists():
            problems.append(f"{rel}: ядерный процесс {workflow!r} не найден")

    readme = path.parent / "README.md"
    if not readme.exists():
        problems.append(f"{rel}: нет README.md рядом с профилем (HYAI-ART-09)")
    elif "не делает" not in readme.read_text(encoding="utf-8").lower():
        problems.append(f"{rel}: в README нет раздела «чего не делает» — профиль не определён (KIT-POL-08)")
    return problems


def check_purity(root: Path, man: dict) -> list[str]:
    """Движки не должны знать имён доменов (KIT-INV-01)."""
    problems: list[str] = []
    names = [n for n in (man.get("domains") or {}) if len(n) > 2]
    paths = man.get("paths") or {}
    tools_rel = paths.get("hyai_tools") or paths.get("tools") or "HYAI/tools/"
    tools_dir = sh.fw(root, str(tools_rel))
    for path in sorted(tools_dir.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for name in names:
            if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text):
                problems.append(f"{sh.rel_posix(root, path)}: доменное имя {name!r} в движке (KIT-INV-01)")
    return problems


def collect_keys(data, found: set[str]) -> set[str]:
    if isinstance(data, dict):
        for key, value in data.items():
            found.add(str(key))
            collect_keys(value, found)
    elif isinstance(data, list):
        for item in data:
            collect_keys(item, found)
    return found


def check_flags(root: Path, man: dict) -> list[str]:
    """Поля-флаги запрещены (KIT-0001); список читается из схемы frontmatter."""
    schema_rel = str(((man.get("validation") or {}).get("data") or {}).get("frontmatter_schema") or "")
    schema = sh.load_yaml(sh.fw(root, schema_rel)) if schema_rel else {}
    forbidden = {str(item) for item in (schema.get("forbidden_fields") or [])}
    if not forbidden:
        return []
    problems: list[str] = []
    for path in sh.iter_files(root, [".yaml", ".yml"], skip_parts=set(schema.get("skip_parts") or []),
                              skip_prefixes=set(schema.get("skip_prefixes") or [])):
        data = sh.load_yaml(path)
        hits = collect_keys(data, set()) & forbidden
        for key in sorted(hits):
            problems.append(f"{sh.rel_posix(root, path)}: поле `{key}` запрещено — флаг не заменяет решение (KIT-0001)")
    return problems


def check_consumer_separation(root: Path, man: dict, configs: dict[str, dict]) -> list[str]:
    """В проекте-потребителе активные домены не направляют данные внутрь подмодуля каркаса."""
    if not sh.is_consumer_project(root):
        return []
    problems: list[str] = []
    seen: set[str] = set()
    for domain, _profile in sh.active_pairs(man):
        if domain in seen:
            continue
        seen.add(domain)
        cfg = configs.get(domain)
        if not cfg:
            continue
        for root_path in cfg["data"].get("root_paths") or []:
            if sh.in_submodule(root, man, str(root_path)):
                problems.append(
                    f"{cfg['rel']}: активный домен {domain!r} в проекте-потребителе указывает root_paths внутрь "
                    f"подмодуля ({root_path!r}); задайте собственный корень данных проекта в манифесте активного домена"
                )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка структуры доменов")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    man_rel = sh.rel_posix(root, sh.manifest_path(root))
    configs = sh.domain_configs(root, man)
    problems: list[str] = []

    if not configs:
        problems.append(f"{man_rel}: не объявлено ни одного домена")

    roots_seen: dict[str, str] = {}
    for name, cfg in configs.items():
        problems.extend(check_domain(root, name, cfg))
        for root_path in cfg["data"].get("root_paths") or []:
            base = str(root_path).rstrip("/")
            if base in roots_seen and roots_seen[base] != name:
                problems.append(f"{cfg['rel']}: каталог {base!r} уже принадлежит домену {roots_seen[base]!r} (KIT-POL-06)")
            roots_seen[base] = name

    # Границы расширения заданы политикой домена-редактора и permissions манифеста,
    # а не флагами: флаг — это решение, которое агент должен принимать, а не читать.

    active = sh.active_pairs(man)
    if man.get("bootstrap", {}).get("require_domain_and_profile") and not active:
        problems.append(f"{man_rel}: active пуст, но bootstrap требует домен и профиль")
    for domain, profile in active:
        cfg = configs.get(domain)
        if not cfg:
            problems.append(f"{man_rel}: active ссылается на незаявленный домен {domain!r}")
            continue
        if profile not in (cfg["data"].get("profiles") or {}):
            problems.append(f"{man_rel}: у домена {domain!r} нет профиля {profile!r}")

    problems.extend(check_consumer_separation(root, man, configs))
    problems.extend(check_purity(root, man))
    problems.extend(check_flags(root, man))
    return sh.emit(problems, "домены и профили", args.json)


if __name__ == "__main__":
    raise SystemExit(main())
