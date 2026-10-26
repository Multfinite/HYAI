#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка и простановка frontmatter по схемам, а не по зашитым спискам.

Источник данных:
- `HYAI/meta/manifest.yaml` — пути, `path_map`, `strict_map`;
- `meta/schema/frontmatter.yaml` — базовая схема;
- `meta/schema/domains/<domain>.yaml` — оверлей домена;
- `HYAI/core/domains/<domain>/schema/authority.yaml` и `.../access.yaml` — словари уровней и контуров.

Ни одно имя каталога, поля или значения не зашито в код.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

SLUG_RE = re.compile(r"[^a-z0-9]+")


def deep_merge(base: dict, overlay: dict) -> dict:
    """Слияние схем по правилам `merge` базовой схемы (MERGE-01..06)."""
    result = {k: (v.copy() if isinstance(v, (dict, list)) else v) for k, v in base.items()}
    for key, value in overlay.items():
        if key in ("merge", "extends"):
            continue
        if key in ("required", "optional", "skip_parts", "skip_prefixes"):
            existing = list(result.get(key) or [])
            for item in value or []:
                if item not in existing:
                    existing.append(item)
            result[key] = existing
        elif key == "enums":
            enums = dict(result.get("enums") or {})
            enums.update(value or {})
            result["enums"] = enums
        elif key == "defaults_by_dir":
            rows = dict(result.get("defaults_by_dir") or {})
            rows.update(value or {})
            result["defaults_by_dir"] = rows
        elif key == "field_aliases":
            aliases = {k: list(v) for k, v in (result.get("field_aliases") or {}).items()}
            for field, names in (value or {}).items():
                aliases[field] = sorted(set(aliases.get(field, []) + list(names)))
            result["field_aliases"] = aliases
        elif key == "forbidden_values":
            result["forbidden_values"] = value or {}
        else:
            result[key] = value
    return result


def schema_for_scope(root: Path, man: dict, scope: str | None) -> tuple[dict, list[str]]:
    """Возвращает (схема, предупреждения)."""
    warns: list[str] = []
    base_rel = (man.get("validation", {}).get("data") or {}).get("frontmatter_schema") or "meta/schema/frontmatter.yaml"
    base = sh.load_yaml(sh.fw(root, str(base_rel)))
    if not base:
        warns.append(f"схема не найдена: {base_rel}")
    if not scope or scope in ("project", "kernel"):
        return base, warns
    overlay_rel = str((man.get("paths") or {}).get("frontmatter_overlay") or "").format(domain=scope)
    overlay = sh.load_yaml(sh.fw(root, overlay_rel)) if overlay_rel else {}
    if not overlay:
        warns.append(f"нет оверлея схемы для области {scope!r}: {overlay_rel}")
        return base, warns
    merged = deep_merge(base, overlay)

    dom = (sh.domain_configs(root, man).get(scope) or {}).get("data") or {}
    auth_schema_rel = (dom.get("authority") or {}).get("schema")
    access_schema_rel = (dom.get("access") or {}).get("schema")
    auth = sh.load_yaml(sh.fw(root, str(auth_schema_rel))) if auth_schema_rel else {}
    access = sh.load_yaml(sh.fw(root, str(access_schema_rel))) if access_schema_rel else {}

    if auth.get("authority", {}).get("values"):
        merged.setdefault("enums", {})["authority"] = list(auth["authority"]["values"])
    if auth.get("status", {}).get("values"):
        merged.setdefault("enums", {})["status"] = list(auth["status"]["values"])
    if access.get("visibility", {}).get("values"):
        merged.setdefault("enums", {})["visibility"] = list(access["visibility"]["values"])
    if access.get("knowledge", {}).get("values"):
        merged.setdefault("enums", {})["knowledge"] = list(access["knowledge"]["values"])
    merged["_defaults_from_domain"] = {
        "authority": (auth.get("authority") or {}).get("default"),
        "status": (auth.get("status") or {}).get("default"),
        "visibility": (access.get("visibility") or {}).get("default"),
        "knowledge": (access.get("knowledge") or {}).get("default"),
    }
    return merged, warns


def defaults_for(rel: str, schema: dict) -> dict:
    rows = schema.get("defaults_by_dir") or {}
    best_key, best_len = None, -1
    for key in rows:
        if (rel == key or rel.startswith(str(key).rstrip("/") + "/")) and len(str(key)) > best_len:
            best_key, best_len = key, len(str(key))
    values = dict(schema.get("root_default") or {})
    if best_key:
        values.update(rows[best_key] or {})
    values.update({k: v for k, v in (schema.get("_defaults_from_domain") or {}).items() if v})
    return values


def derive_title(text: str, stem: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return stem.replace("-", " ").strip().capitalize()


def derive_id(scope: str, rel: str, type_value: str) -> str:
    parts = list(Path(rel).with_suffix("").parts)
    slug = SLUG_RE.sub("-", "-".join(parts).lower()).strip("-")
    prefix = "kernel" if scope in (None, "project") else scope
    return f"{prefix}.{type_value}.{slug}"


def check_file(rel: str, text: str, schema: dict, alias_map: dict) -> list[str]:
    meta, _ = sh.split_frontmatter(text)
    problems: list[str] = []
    if not meta:
        return [f"{rel}: нет frontmatter"]
    for field in schema.get("required") or []:
        if not meta.get(field):
            problems.append(f"{rel}: нет обязательного поля `{field}`")
    for field, names in alias_map.items():
        if not meta.get(field) and any(meta.get(name) for name in names):
            source = next(name for name in names if meta.get(name))
            problems.append(f"{rel}: поле `{source}` допустимо как алиас `{field}`, но лучше `{field}`")
    enums = schema.get("enums") or {}
    for field, allowed in enums.items():
        if field not in meta or meta.get(field) in (None, ""):
            continue
        value = meta[field]
        values = meta[field] if isinstance(value, list) else [value]
        for item in values:
            if item not in allowed:
                problems.append(f"{rel}: {field}={item!r} недопустимо (допустимо: {', '.join(map(str, allowed))})")
    for field in schema.get("forbidden_fields") or []:
        if field in meta:
            problems.append(f"{rel}: поле `{field}` запрещено — флаг не заменяет решение (KIT-0001)")
    for field, forbidden in (schema.get("forbidden_values") or {}).items():
        if meta.get(field) in (forbidden or []):
            problems.append(f"{rel}: {field}={meta[field]!r} принадлежит другому домену и здесь запрещено")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка и простановка frontmatter")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--apply", action="store_true", help="дописать отсутствующие поля")
    parser.add_argument("--check", action="store_true", help="только проверить (по умолчанию)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    if not man:
        print("HYAI/meta/manifest.yaml не найден", file=sys.stderr)
        return 2

    base_schema = sh.load_yaml(sh.fw(root, str((man.get("validation", {}).get("data") or {}).get("frontmatter_schema") or "")))
    extensions = [".md"]
    files = sh.iter_files(
        root, extensions,
        skip_parts=base_schema.get("skip_parts") or [],
        skip_prefixes=base_schema.get("skip_prefixes") or [],
        skip_names=base_schema.get("skip_names") or [],
    )

    problems: list[str] = []
    added = 0
    strict = bool(man.get("strict_map"))
    schemas: dict[str | None, tuple[dict, list[str]]] = {}

    for path in files:
        rel = sh.rel_posix(root, path)
        scope = sh.resolve_scope(root, man, rel)
        if scope is None and strict:
            problems.append(f"{rel}: путь не отображён ни на один домен (path_map / root_paths)")
            continue
        if scope not in schemas:
            schemas[scope] = schema_for_scope(root, man, scope)
        schema, _warns = schemas[scope]
        text = path.read_text(encoding="utf-8")

        if args.apply and not sh.split_frontmatter(text)[0]:
            values = defaults_for(rel, schema)
            title = derive_title(text, path.stem)
            values.setdefault("title", f'"{title}"')
            values.setdefault("type", "working")
            values["id"] = f"{scope or 'kernel'}.{(values.get('type') or 'working')}.{SLUG_RE.sub('-', rel.lower()).strip('-')}"
            block = "\n".join(f"{k}: {v}" for k, v in values.items())
            path.write_text(f"---\n{block}\n---\n\n{text.lstrip()}", encoding="utf-8")
            added += 1
            text = path.read_text(encoding="utf-8")

        problems.extend(check_file(rel, text, schema, schema.get("field_aliases") or {}))

    if args.apply:
        for scope, (_schema, warns) in schemas.items():
            problems.extend(w for w in warns)

    if args.json:
        sh.emit(problems, "frontmatter", True, {"files": len(files), "added": added})
    else:
        for p in problems:
            print(f"  {p}")
        print(f"\nфайлов: {len(files)}; проблемных: {len(problems)}; добавлено полей: {added}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
