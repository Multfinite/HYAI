# SPDX-License-Identifier: GPL-3.0-only
"""Общие функции движков. Никаких доменных имён: всё читается из HYAI/meta/manifest.yaml.

Модуль намеренно маленький: он не «фреймворк», а набор из пяти функций, которые
иначе пришлось бы копировать в каждый скрипт.
"""

from __future__ import annotations

import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[2]


# ---------- чтение конфигурации ----------

def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


HYAI_DIR = "HYAI"
MANIFEST_REL = "HYAI/meta/manifest.yaml"


def manifest(root: Path) -> dict:
    return load_yaml(root / MANIFEST_REL)


def active_pairs(man: dict) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in man.get("active") or []:
        if isinstance(item, dict) and item.get("domain") and item.get("profile"):
            pairs.append((str(item["domain"]), str(item["profile"])))
    return pairs


def domain_configs(root: Path, man: dict) -> dict[str, dict]:
    """Все домены из манифеста: имя -> {path, data}."""
    result: dict[str, dict] = {}
    for name, rel in (man.get("domains") or {}).items():
        path = root / str(rel)
        result[str(name)] = {"path": path, "rel": str(rel), "data": load_yaml(path)}
    return result


def active_domains(root: Path, man: dict) -> dict[str, dict]:
    configs = domain_configs(root, man)
    names = {d for d, _ in active_pairs(man)}
    return {n: c for n, c in configs.items() if n in names}


def merge_dicts(base: dict, overlay: dict) -> dict:
    """Слияние участков профиля: списки объединяются, словари дополняются, скаляры профиля побеждают."""
    out = dict(base)
    for key, value in overlay.items():
        if key in ("apiVersion", "kind", "includes"):
            continue
        if isinstance(value, list) and isinstance(out.get(key), list):
            merged = list(out[key])
            merged.extend(item for item in value if item not in merged)
            out[key] = merged
        elif isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = {**out[key], **value}
        else:
            out[key] = value
    return out


def load_profile(root: Path, rel: str, depth: int = 0) -> dict:
    """Профиль вместе с общими участками из `includes` (HYAI/core/shared/...)."""
    if depth > 5:
        return {}
    data = load_yaml(root / rel)
    if not data:
        return {}
    merged: dict = {}
    for include in data.get("includes") or []:
        target = root / str(include)
        include_rel = str(target / "profile.yaml") if target.is_dir() else str(include)
        merged = merge_dicts(merged, load_profile(root, include_rel, depth + 1))
    return merge_dicts(merged, data)


def profile_config(root: Path, dom: dict, profile: str) -> dict:
    rel = (dom.get("data", {}).get("profiles") or {}).get(profile)
    if not rel:
        return {}
    return load_profile(root, str(rel))


def profile_paths_by_name(root: Path, man: dict) -> dict[str, list[str]]:
    """Имя профиля -> список его каталогов. Используется для fallback-поиска."""
    out: dict[str, list[str]] = {}
    for name, cfg in domain_configs(root, man).items():
        for profile, rel in (cfg["data"].get("profiles") or {}).items():
            out.setdefault(str(profile), []).append(str(Path(str(rel)).parent))
    return out


# ---------- пути ----------

def glob_to_regex(pattern: str) -> re.Pattern:
    """Переводит глоб в регулярное выражение, понимая `**` как «любая глубина»."""
    p = pattern.replace("\\", "/")
    i, out = 0, []
    while i < len(p):
        if p.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif p.startswith("**", i):
            out.append(".*")
            i += 2
        elif p[i] == "*":
            out.append("[^/]*")
            i += 1
        elif p[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(p[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def matches(rel: str, patterns: Iterable[str]) -> bool:
    rel = rel.replace("\\", "/").lstrip("./")
    return any(glob_to_regex(str(pat)).match(rel) for pat in patterns or [])


def rel_posix(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_scope(root: Path, man: dict, rel: str) -> str | None:
    """Путь -> область (`project`, имя домена или `kernel`).

    Порядок: отчёты и решения (scope из пути) -> path_map (самое длинное совпадение)
    -> root_paths доменов -> None (ошибка при strict_map).
    """
    rel = rel.replace("\\", "/").lstrip("./")

    rep = man.get("report") or {}
    pattern = str(rep.get("dir_pattern") or "")
    if pattern:
        prefix_re = glob_to_regex(pattern.replace("{scope}", "*"))
        if prefix_re.match(rel) or rel.startswith(pattern.split("{scope}")[0]):
            rest = rel[len(pattern.split("{scope}")[0]):]
            scope = rest.split("/")[0]
            if scope in (rep.get("allowed_scopes") or []):
                return scope

    dec = man.get("decisions") or {}
    for scope, cfg in (dec.get("scopes") or {}).items():
        directory = str((cfg or {}).get("dir") or "").rstrip("/")
        if directory and rel == f"{directory}/README.md":
            return "project"          # индекс области — документ проекта, а не домена
        if directory and rel.startswith(directory + "/"):
            return str(scope)

    best: tuple[int, str] | None = None
    for pattern, domain in (man.get("path_map") or {}).items():
        if matches(rel, [str(pattern)]):
            depth = len(str(pattern))
            if best is None or depth > best[0]:
                best = (depth, str(domain))
    if best:
        return best[1]

    for name, cfg in domain_configs(root, man).items():
        for root_path in cfg["data"].get("root_paths") or []:
            base = str(root_path).rstrip("/")
            if rel == base or rel.startswith(base + "/"):
                return name
    return None


def domains_for_scope(root: Path, man: dict, scope: str | None) -> dict:
    if not scope:
        return {}
    cfg = domain_configs(root, man).get(scope)
    return cfg["data"] if cfg else {}


# ---------- файлы ----------

def iter_files(root: Path, exts: Iterable[str], skip_parts: Iterable[str] = (), skip_prefixes: Iterable[str] = (), skip_names: Iterable[str] = ()) -> list[Path]:
    exts = {e.lower() for e in exts}
    skip_parts = set(skip_parts)
    skip_names = {n.lower() for n in skip_names}
    result: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in exts:
            continue
        if path.name.lower() in skip_names:
            continue
        rel = rel_posix(root, path)
        if any(part in skip_parts for part in Path(rel).parts):
            continue
        if any(rel == p.rstrip("/") or rel.startswith(p.rstrip("/") + "/") for p in skip_prefixes):
            continue
        result.append(path)
    return result


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    try:
        block = yaml.safe_load(text[3:end])
    except yaml.YAMLError:
        return {}, text
    return (block if isinstance(block, dict) else {}), text[end + 4:]


def emit(problems: list[str], header: str, as_json: bool = False, extra: dict | None = None) -> int:
    payload = {"problems": problems, "count": len(problems), **(extra or {})}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for problem in problems:
            print(f"  {problem}")
        print(f"\n{header}: проблем: {len(problems)}")
    return 1 if problems else 0


def run_md_tool(main_fn) -> None:
    try:
        raise SystemExit(main_fn())
    except BrokenPipeError:
        sys.exit(1)
