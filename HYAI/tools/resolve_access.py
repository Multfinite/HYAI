#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Вердикт доступа «роль × призма» и карта понимания.

Движок универсален: модель читается из `access.schema` домена. Домен объявляет роли,
призмы, контуры и шкалу компетенций; здесь нет ни одного имени роли или призмы.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh


def load_model(root: Path, domain: str, man: dict | None = None) -> dict:
    man = man or sh.manifest(root)
    cfg = sh.domain_configs(root, man).get(domain) or {}
    rel = ((cfg.get("data") or {}).get("access") or {}).get("schema")
    if not rel:
        return {}
    return sh.load_yaml(sh.fw(root, str(rel)))


def competence_catalog(root: Path, model: dict) -> dict:
    """Каталог доменов компетенции: файл объявлен в `competence.catalog` схемы домена.

    Нет файла — пустой каталог: движок пишет нейтральную формулировку и не выдумывает лор.
    """
    rel = ((model.get("competence") or {}).get("catalog")) or ""
    if not rel:
        return {}
    data = sh.load_yaml(root / str(rel))
    return {str(item.get("id")): item for item in (data.get("domains") or []) if isinstance(item, dict)}


def _competence_label(model: dict, level) -> str:
    scale = ((model.get("competence") or {}).get("scale") or {})
    prefix = str(scale.get("prefix") or "")
    if level is None:
        return str(scale.get("unknown") or "?")
    try:
        return f"{prefix}{int(level)}"
    except (TypeError, ValueError):
        return str(level)


def _requirements(doc: dict) -> list[dict]:
    return [r for r in (doc.get("requires") or []) if isinstance(r, dict)]


def resolve(model: dict, profile: dict, doc: dict) -> dict:
    """Возвращает {'allowed': bool, 'reasons': [...]}."""
    reasons: list[str] = []
    rules = model.get("rules") or {}
    roles = model.get("roles") or {}
    prisms = model.get("prisms") or {}

    role_name = str(profile.get("role") or "")
    prism_name = str(profile.get("prism") or "")
    role = roles.get(role_name)
    if not role:
        return {"allowed": False, "reasons": [f"неизвестная роль {role_name!r}: доступ закрыт по умолчанию"]}
    if prism_name not in (role.get("prisms") or []):
        return {"allowed": False, "reasons": [f"призма {prism_name!r} недоступна роли {role_name!r}"]}
    prism = prisms.get(prism_name) or {}

    visibility = str(doc.get("visibility") or ((model.get("visibility") or {}).get("default") or ""))
    if visibility in (prism.get("deny_visibility") or []):
        return {"allowed": False, "reasons": [f"контур {visibility!r} закрыт для призмы {prism_name!r}"]}

    characters = [c for c in (profile.get("characters") or []) if isinstance(c, dict)]
    if prism.get("require_owner") or (role or {}).get("require_owner_match"):
        owner = profile.get("owner")
        foreign = [c.get("id") for c in characters if owner and c.get("owner") != owner]
        if foreign:
            return {"allowed": False, "reasons": [f"чужие персонажи: {', '.join(map(str, foreign))}"]}
        if not characters:
            return {"allowed": False, "reasons": ["призма требует персональной привязки, но персонажи не указаны"]}

    knowledge = str(doc.get("knowledge") or ((model.get("knowledge") or {}).get("default") or ""))
    secret_kinds = rules.get("secret_requires_known_by") or []
    if knowledge in secret_kinds:
        known_by = [str(x) for x in (doc.get("known_by") or [])]
        if not known_by:
            return {"allowed": False, "reasons": [f"секрет без носителя: knowledge={knowledge!r}, known_by пуст"]}
        if prism.get("competence_gate"):
            mine = [c for c in characters if str(c.get("id")) in known_by]
            if not mine:
                return {"allowed": False, "reasons": ["никто из персонажей не знает сведений"]}
            reasons.append(f"носители: {', '.join(c.get('title') or str(c.get('id')) for c in mine)}")

    if prism.get("competence_gate") and _requirements(doc):
        passing = []
        for character in characters:
            levels = character.get("domains") or {}
            ok = all(
                levels.get(str(req.get("domain"))) is not None
                and levels.get(str(req.get("domain"))) >= int(req.get("min") or 0)
                for req in _requirements(doc)
            )
            if ok:
                passing.append(character)
        if not passing:
            return {"allowed": False, "reasons": ["компетенция всех субъектов ниже требуемого порога"]}
        reasons.append(f"понимают: {', '.join(c.get('title') or str(c.get('id')) for c in passing)}")

    if not reasons:
        reasons.append(f"роль {role_name!r} × призма {prism_name!r}: доступ разрешён")
    return {"allowed": True, "reasons": reasons}


def _knows_until(model: dict, catalog: dict, domain: str, level) -> tuple[str, str]:
    """Граница «знает до …»: (метка уровня, что именно знает).

    Формулировку даёт каталог домена; без каталога — нейтральная, с той же меткой.
    """
    label = _competence_label(model, level)
    if level is None:
        return label, "некомпетентен"
    entry = catalog.get(domain) or {}
    levels = entry.get("levels") or {}
    text = levels.get(int(level)) or levels.get(str(int(level)))
    if text:
        return label, f"знает до {text}"
    return label, f"знает до {label} включительно"


def competence_map(model: dict, profile: dict, doc: dict, catalog: dict | None = None) -> list[str]:
    """Блок «Карта понимания»: по каждому субъекту — уровень и статус знания."""
    scale_unknown = ((model.get("competence") or {}).get("scale") or {}).get("unknown") or "?"
    requirements = _requirements(doc)
    known_by = [str(x) for x in (doc.get("known_by") or [])]
    lines: list[str] = []
    for character in [c for c in (profile.get("characters") or []) if isinstance(c, dict)]:
        title = str(character.get("title") or character.get("id"))
        levels = character.get("domains") or {}
        if not requirements:
            lines.append(f"{title} — все сведения доступны: требований к пониманию нет")
            continue
        parts: list[str] = []
        competent = True
        for req in requirements:
            domain, minimum = str(req.get("domain")), int(req.get("min") or 0)
            level = levels.get(domain)
            if level is None:
                competent = False
                parts.append(f"{scale_unknown}: некомпетентен в «{domain}»")
                continue
            label, knows_until = _knows_until(model, catalog or {}, domain, level)
            if level < minimum:
                competent = False
                parts.append(f"{label} (ниже порога {_competence_label(model, minimum)}): {knows_until}")
            else:
                parts.append(f"{label}: {knows_until}")
        knows = (not known_by) or str(character.get("id")) in known_by
        if not knows and known_by:
            parts.append("не знает сведений")
        elif competent:
            parts.append("понимает")
        lines.append(f"{title} — {'; '.join(parts)}")
    return lines


def matrix(model: dict) -> str:
    roles = list((model.get("roles") or {}).keys())
    prisms = list((model.get("prisms") or {}).keys())
    rows = ["| Роль \\ Призма | " + " | ".join(f"`{p}`" for p in prisms) + " |", "| --- | " + " | ".join("---" for _ in prisms) + " |"]
    for role in roles:
        cells = ["да" if p in (model["roles"][role].get("prisms") or []) else "нет" for p in prisms]
        rows.append(f"| `{role}` | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Роль × призма")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--domain", required=True)
    parser.add_argument("--role")
    parser.add_argument("--prism")
    parser.add_argument("--owner")
    parser.add_argument("--character", action="append", default=[], help="id персонажа")
    parser.add_argument("--doc")
    parser.add_argument("--matrix", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    model = load_model(root, args.domain)
    catalog = competence_catalog(root, model)
    if not model:
        print(f"нет модели доступа для домена {args.domain!r}", file=sys.stderr)
        return 2

    if args.matrix:
        print(matrix(model))
        return 0

    doc: dict = {}
    if args.doc:
        meta, _ = sh.split_frontmatter((root / args.doc).read_text(encoding="utf-8"))
        doc = meta
    profile = {
        "role": args.role,
        "prism": args.prism,
        "owner": args.owner,
        "characters": [{"id": c, "owner": args.owner, "domains": {}} for c in args.character],
    }
    verdict = resolve(model, profile, doc)
    if args.json:
        print(json.dumps({**verdict, "map": competence_map(model, profile, doc, catalog)}, ensure_ascii=False, indent=2))
    else:
        print("доступ: " + ("да" if verdict["allowed"] else "нет"))
        for reason in verdict["reasons"]:
            print(f"  — {reason}")
        for line in competence_map(model, profile, doc, catalog):
            print(f"  {line}")
    return 0 if verdict["allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
