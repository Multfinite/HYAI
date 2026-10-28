# SPDX-License-Identifier: GPL-3.0-only
"""Общие функции движков. Никаких доменных имён: всё читается из манифеста проекта (meta/manifest.yaml).

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

DEFAULT_ROOT = Path.cwd().resolve()


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
# Данные проекта живут в ./meta проекта, а не в каталоге каркаса:
# HYAI/meta — шаблон, HYAI/tools — встроенные движки самого HYAI.
# Для каркаса, установленного «сам в себя» (его собственный репозиторий),
# манифест остаётся в HYAI/meta/ — это второй кандидат.
MANIFEST_RELS = ("meta/manifest.yaml", "HYAI/meta/manifest.yaml")


def manifest_path(root: Path) -> Path:
    for rel in MANIFEST_RELS:
        candidate = root / rel
        if candidate.exists():
            return candidate
    return root / MANIFEST_RELS[-1]


def manifest(root: Path) -> dict:
    for rel in MANIFEST_RELS:
        man = load_yaml(root / rel)
        if man:
            return man
    return {}


def is_consumer_project(root: Path) -> bool:
    """True, когда каркас подключён к внешнему проекту (манифест лежит в ./meta/manifest.yaml)."""
    return (root / MANIFEST_RELS[0]).exists()


def fw_root(root: Path) -> Path:
    """Корень каркаса: каталог, внутри которого лежит `HYAI/` с `core/`, `meta/` (шаблон), `tools/`.

    Это не корень проекта: данные проекта (`meta/`, `tools/`) живут от корня проекта,
    а пути самого каркаса (`HYAI/core/...`, `HYAI/tools/...`) — от корня каркаса.
    `framework.root` в манифесте задаёт, где каркас установлен (`""` — каркас сам себе проект).
    """
    rel = str(((manifest(root).get("framework") or {}).get("root")) or "").strip("/")
    return (root / rel) if rel and rel != "." else root


def submodule_prefixes(root: Path, man: dict) -> list[str]:
    """Префиксы каталога каркаса/подмодуля во внешнем проекте-потребителе."""
    if not is_consumer_project(root):
        return []
    out: list[str] = [HYAI_DIR]
    cfg = man.get("framework") or {}
    for key in ("root", "prefix"):
        val = str(cfg.get(key) or "").replace("\\", "/").strip("/")
        if val and val != ".":
            if val not in out:
                out.append(val)
    return out


def in_submodule(root: Path, man: dict, rel: str) -> bool:
    """Проверяет, ведёт ли путь или глоб во внутреннее дерево подмодуля каркаса."""
    clean = str(rel or "").replace("\\", "/").lstrip("./").rstrip("/")
    for prefix in submodule_prefixes(root, man):
        if clean == prefix or clean.startswith(prefix + "/"):
            return True
    return False


def fw(root: Path, rel: str) -> Path:
    """Резолв пути: сначала от корня проекта, затем от корня каркаса.

    Пути проекта (`meta/...`, `src/...`) находятся сразу; пути каркаса (`HYAI/core/...`)
    в установленном виде находятся от корня каркаса. Так один и тот же код работает и в
    репозитории каркаса, и в проекте, куда каркас поставлен каталогом `HYAI/`.
    """
    rel = str(rel or "")
    direct = root / rel
    if direct.exists():
        return direct
    return fw_root(root) / rel


def active_pairs(man: dict) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in man.get("active") or []:
        if isinstance(item, dict) and item.get("domain") and item.get("profile"):
            pairs.append((str(item["domain"]), str(item["profile"])))
    return pairs


def rebase_globs(patterns: Iterable[str], template_roots: Iterable[str], effective_roots: Iterable[str]) -> list[str]:
    """Переносит глобы и пути с шаблонного корня домена каркаса на фактический root_paths домена."""
    src_list = [str(r).replace("\\", "/").strip("/") for r in (template_roots or []) if str(r).strip("/")]
    dst_list = [str(r).replace("\\", "/").strip("/") for r in (effective_roots or []) if str(r).strip("/")]
    raw = [str(p) for p in (patterns or [])]
    if not src_list or not dst_list or src_list == dst_list:
        return raw
    out: list[str] = []
    for pat in raw:
        norm = pat.replace("\\", "/").lstrip("./")
        replaced = False
        for idx, src in enumerate(src_list):
            targets = [dst_list[idx]] if idx < len(dst_list) else dst_list
            if norm == src or norm.startswith(src + "/"):
                suffix = norm[len(src):]
                for dst in targets:
                    candidate = dst + suffix
                    if candidate not in out:
                        out.append(candidate)
                replaced = True
                break
        if not replaced and pat not in out:
            out.append(pat)
    return out


def merge_domain_dicts(base: dict, overlay: dict) -> dict:
    """Слияние манифеста домена (`includes`): `root_paths` оверлея заменяет шаблонный путь подмодуля."""
    out = merge_dicts(base, overlay)
    if "root_paths" in overlay and overlay.get("root_paths") is not None:
        out["root_paths"] = [str(item) for item in (overlay.get("root_paths") or [])]
    return out


def load_domain(root: Path, rel: str, depth: int = 0) -> tuple[dict, list[str]]:
    """Загружает манифест домена с поддержкой `includes`; возвращает `(data, template_root_paths)`."""
    if depth > 5:
        return {}, []
    data = load_yaml(fw(root, rel))
    if not data:
        return {}, []
    merged: dict = {}
    template_roots: list[str] = []
    for include in data.get("includes") or []:
        target = fw(root, str(include))
        include_rel = str(target / "manifest.yaml") if target.is_dir() else str(include)
        inc_data, inc_roots = load_domain(root, include_rel, depth + 1)
        for item in inc_roots or inc_data.get("root_paths") or []:
            if str(item) not in template_roots:
                template_roots.append(str(item))
        merged = merge_domain_dicts(merged, inc_data)
    merged = merge_domain_dicts(merged, data)
    return merged, template_roots


def domain_configs(root: Path, man: dict) -> dict[str, dict]:
    """Все домены из манифеста: имя -> {path, rel, data, template_root_paths}."""
    active_roots: dict[str, list[str]] = {}
    for item in man.get("active") or []:
        if isinstance(item, dict) and item.get("domain") and item.get("root_paths"):
            active_roots[str(item["domain"])] = [str(p) for p in (item.get("root_paths") or [])]

    result: dict[str, dict] = {}
    for name, rel in (man.get("domains") or {}).items():
        dname = str(name)
        path = fw(root, str(rel))
        data, template_roots = load_domain(root, str(rel))
        if not template_roots:
            fw_manifest = fw_root(root) / HYAI_DIR / "core" / "domains" / dname / "manifest.yaml"
            if fw_manifest.exists() and (not path.exists() or fw_manifest.resolve() != path.resolve()):
                fw_data = load_yaml(fw_manifest)
                template_roots = [str(r) for r in (fw_data.get("root_paths") or [])]
        if dname in active_roots:
            if not template_roots:
                template_roots = [str(r) for r in (data.get("root_paths") or [])]
            data = {**data, "root_paths": list(active_roots[dname])}
        if not template_roots:
            template_roots = [str(r) for r in (data.get("root_paths") or [])]
        result[dname] = {
            "path": path,
            "rel": str(rel),
            "data": data,
            "template_root_paths": template_roots,
        }
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
    data = load_yaml(fw(root, rel))
    if not data:
        return {}
    merged: dict = {}
    for include in data.get("includes") or []:
        target = fw(root, str(include))
        include_rel = str(target / "profile.yaml") if target.is_dir() else str(include)
        merged = merge_dicts(merged, load_profile(root, include_rel, depth + 1))
    return merge_dicts(merged, data)


def profile_config(root: Path, dom: dict, profile: str) -> dict:
    rel = (dom.get("data", {}).get("profiles") or {}).get(profile)
    if not rel:
        return {}
    loaded = load_profile(root, str(rel))
    if not loaded:
        return {}
    template_roots = dom.get("template_root_paths") or []
    effective_roots = (dom.get("data") or {}).get("root_paths") or []
    for scope_key in ("scope_primary", "scope_secondary"):
        if loaded.get(scope_key):
            loaded[scope_key] = rebase_globs(loaded[scope_key], template_roots, effective_roots)
    return loaded


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
