#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Навигация и реестры: README в каталогах, индексы, уникальность id, пути манифеста.

Проверяются управляемые слои: инструкции каркаса (`paths.core`), данные проекта (`paths.meta`)
и встроенные движки (`paths.hyai_tools`) — там навигация — часть контракта, HYAI-ART-09..11.
Каталоги продукта (`src/`, `world/`, …) не обязаны иметь README в каждом подкаталоге.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

SKIP_PARTS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", "Exports", "_backups"}
SKIP_PREFIXES = {"HYAI/core/intermediate", "HYAI/HYAI/core/intermediate"}


def governed_bases(man: dict) -> list[str]:
    """Управляемые корни берутся из манифеста, а не из кода (`3D`)."""
    paths = man.get("paths") or {}
    bases: list[str] = []
    for key in ("core", "meta", "hyai_tools"):
        value = str(paths.get(key) or "").rstrip("/")
        if value and value not in bases:
            bases.append(value)
    return bases or ["HYAI/core", "HYAI/meta", "HYAI/tools"]


def working_data_roots(root: Path, man: dict) -> set[str]:
    """Рабочие каталоги доменов (`root_paths`), не содержащие манифестов доменов и схем."""
    configs = sh.domain_configs(root, man)
    governance_targets: list[str] = []
    for cfg in configs.values():
        if cfg.get("rel"):
            governance_targets.append(str(cfg["rel"]).replace("\\", "/").strip("/"))
        overlay = (cfg.get("data") or {}).get("schema")
        if overlay:
            governance_targets.append(str(overlay).replace("\\", "/").strip("/"))
    schema_dir = ((man.get("paths") or {}).get("schema")) or ""
    if schema_dir:
        governance_targets.append(str(schema_dir).replace("\\", "/").strip("/"))
    fm_schema = (((man.get("validation") or {}).get("data") or {}).get("frontmatter_schema")) or ""
    if fm_schema:
        governance_targets.append(str(fm_schema).replace("\\", "/").strip("/"))

    data_roots: set[str] = set()
    for cfg in configs.values():
        for raw in (cfg.get("data") or {}).get("root_paths") or []:
            clean = str(raw).replace("\\", "/").strip("/")
            if not clean:
                continue
            if any(t == clean or t.startswith(clean + "/") for t in governance_targets if t):
                continue
            data_roots.add(clean)
    return data_roots


def governed_dirs(root: Path, man: dict) -> list[Path]:
    result: list[Path] = []
    skip_data = working_data_roots(root, man)
    for base in governed_bases(man):
        for path in sorted(sh.fw(root, base).rglob("*")):
            if not path.is_dir():
                continue
            if path.name.startswith((".", "__")):
                continue
            rel = sh.rel_posix(root, path)
            if any(part in SKIP_PARTS for part in Path(rel).parts):
                continue
            if any(rel == p or rel.startswith(p + "/") for p in SKIP_PREFIXES | skip_data):
                continue
            if any(child.suffix.lower() in (".md", ".yaml", ".yml", ".json", ".py") for child in path.iterdir() if child.is_file()):
                result.append(path)
    return result


def check_readmes(root: Path, man: dict) -> list[str]:
    problems: list[str] = []
    for directory in governed_dirs(root, man):
        rel = sh.rel_posix(root, directory)
        readme = directory / "README.md"
        if not readme.exists():
            problems.append(f"{rel}/: нет README.md (HYAI-ART-09)")
            continue
        text = urllib.parse.unquote(readme.read_text(encoding="utf-8"))
        for child in sorted(directory.iterdir()):
            if child.name == "README.md":
                continue
            if child.is_dir() and child.name.startswith((".", "__")):
                continue
            if child.name == "__pycache__":
                continue
            if child.name.lower() in ("agents.md",) and child.suffix.lower() == ".md":
                pass
            if child.name not in text:
                problems.append(f"{rel}/README.md: не упомянут {child.name} (HYAI-ART-09)")
    return problems


def check_index_files(root: Path) -> list[str]:
    problems: list[str] = []
    for index_path in sorted(root.rglob("*.index.md")):
        rel = sh.rel_posix(root, index_path)
        if any(part in SKIP_PARTS for part in Path(rel).parts):
            continue
        readme = index_path.parent / "README.md"
        if not readme.exists() or index_path.name not in readme.read_text(encoding="utf-8"):
            problems.append(f"{rel}: не упомянут в README своего каталога (HYAI-ART-10)")
    return problems


def registry_files(root: Path, man: dict) -> list[Path]:
    files: list[Path] = []
    repo_registry = (man.get("paths") or {}).get("registry")
    if repo_registry and sh.fw(root, str(repo_registry)).exists():
        files.append(sh.fw(root, str(repo_registry)))
    for cfg in sh.domain_configs(root, man).values():
        rel = cfg["data"].get("registry")
        if rel and sh.fw(root, str(rel)).exists():
            files.append(sh.fw(root, str(rel)))
    return files


def check_registries(root: Path, man: dict) -> list[str]:
    problems: list[str] = []
    seen: dict[str, str] = {}
    for path in registry_files(root, man):
        data = sh.load_yaml(path)
        rel = sh.rel_posix(root, path)
        for doc_rel in data.get("read_first") or []:
            if not sh.fw(root, str(doc_rel)).exists():
                problems.append(f"{rel}: read_first указывает на несуществующий файл: {doc_rel}")
        for entry in data.get("documents") or []:
            doc_id = str(entry.get("id") or "")
            doc_path = str(entry.get("path") or "")
            if not doc_id:
                problems.append(f"{rel}: запись без id")
                continue
            if doc_id in seen:
                problems.append(f"{rel}: дубль id={doc_id!r} (уже в {seen[doc_id]}) (HYAI-ART-12)")
            seen[doc_id] = rel
            if doc_path and not sh.fw(root, doc_path).exists():
                problems.append(f"{rel}: путь для {doc_id} не найден: {doc_path}")
    return problems


def check_manifest_paths(root: Path, man: dict) -> list[str]:
    problems: list[str] = []
    candidates: list[str] = []
    for key in ("entrypoint", "entrypoints"):
        value = man.get(key)
        candidates.extend(value if isinstance(value, list) else ([value] if value else []))
    for value in (man.get("paths") or {}).values():
        candidates.append(value)
    for value in (man.get("domains") or {}).values():
        candidates.append(value)
    validation = man.get("validation") or {}
    for key in ("data",):
        candidates.extend((validation.get(key) or {}).values())
    candidates.append(validation.get("ci"))
    for scope in ((man.get("decisions") or {}).get("scopes") or {}).values():
        candidates.append((scope or {}).get("dir"))
    candidates.append((man.get("report") or {}).get("index"))

    optional = [str(p).rstrip("/") for p in man.get("optional_paths") or []]
    domains = list(sh.domain_configs(root, man)) or ["domain"]
    man_rel = sh.rel_posix(root, sh.manifest_path(root))
    seen: set[str] = set()
    for rel in candidates:
        if not rel:
            continue
        raw = str(rel)
        if raw.rstrip("/") in optional:
            continue
        targets = [raw.replace("{domain}", d) for d in domains] if "{domain}" in raw else [raw]
        for target in targets:
            if target in seen:
                continue
            seen.add(target)
            if not sh.fw(root, target).exists():
                problems.append(f"{man_rel}: путь не найден: {target}")
    return problems


def check_domain_roots(root: Path, man: dict) -> list[str]:
    problems: list[str] = []
    optional = [str(p).rstrip("/") for p in man.get("optional_paths") or []]
    active_names = {d for d, _ in sh.active_pairs(man)}
    consumer = sh.is_consumer_project(root)
    for name, cfg in sh.domain_configs(root, man).items():
        for rel in cfg["data"].get("root_paths") or []:
            base = str(rel).rstrip("/")
            if base in optional:
                continue
            if name in active_names:
                if consumer and sh.in_submodule(root, man, str(rel)):
                    problems.append(
                        f"{cfg['rel']}: каталог активного домена указывает внутрь подмодуля: {rel}"
                    )
                    continue
                exists = (root / str(rel)).exists()
            else:
                exists = sh.fw(root, str(rel)).exists()
            if not exists:
                problems.append(f"{cfg['rel']}: каталог домена не найден: {rel}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка навигации и реестров")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    problems = (
        check_readmes(root, man)
        + check_index_files(root)
        + check_registries(root, man)
        + check_manifest_paths(root, man)
        + check_domain_roots(root, man)
    )
    return sh.emit(problems, "навигация и реестры", args.json)


if __name__ == "__main__":
    raise SystemExit(main())
