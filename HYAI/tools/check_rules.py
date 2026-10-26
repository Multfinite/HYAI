#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Проверка идентификаторов правил: формат, владелец, уникальность, ссылки.

Схема — `HYAI/core/kernel/spec/rule-ids.md`, машинные данные — `HYAI/meta/schema/rule-ids.yaml`.
Движок не знает ни одного конкретного ID: всё, что он проверяет, объявлено в реестре.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

# Два вида ID: `<OWNER>-<CLASS>-<NN>` (`HYAI-ART-15`) и `<OWNER>-<CLASS>-<БУКВА><NN>`
# (`HYAI-PERM-N01`): у классов `PERM` буква приклеена к номеру, без дефиса.
TOKEN = r"[A-Z]{2,6}-[A-Z]+(?:-[A-Z]+)?-[A-Z]?\d{2}"
TOKEN_RE = re.compile(rf"\b({TOKEN})(?:\.\.(\d{{2}}))?\b")
TICKED_RE = re.compile(rf"`({TOKEN})`")
DEF_RE = re.compile(rf"^[\s|>*+-]*`({TOKEN})`")
# Номер без класса (`NR-<NN>` из первого выпуска): формат не распознаётся как ID,
# и правило молча выпадает из учёта. `Q-<DOMAIN>-<NN>` — ID вопроса, не legacy-правило.
LEGACY_RE = re.compile(r"(?<!Q-)\b([A-Z]{2,6})-\d{2}\b")


def load_registry(root: Path) -> tuple[dict, list[str]]:
    man = sh.manifest(root)
    rel = ((man.get("validation") or {}).get("data") or {}).get("rule_ids")
    if not rel:
        return {}, ["HYAI/meta/manifest.yaml: не задан validation.data.rule_ids"]
    path = root / str(rel)
    if not path.exists():
        return {}, [f"{rel}: реестр идентификаторов не найден"]
    data = sh.load_yaml(path)
    if not data:
        return {}, [f"{rel}: реестр пуст или не читается"]
    return data, []


def source_files(root: Path, registry: dict) -> list[Path]:
    result: list[Path] = []
    seen: set[Path] = set()
    for pattern in registry.get("sources") or []:
        for path in sorted(root.glob(str(pattern))):
            if path.is_file() and path not in seen:
                seen.add(path)
                result.append(path)
    return result


def reference_files(root: Path, registry: dict, skip: set[Path]) -> list[Path]:
    scope = [str(p) for p in registry.get("reference_scope") or []]
    exts = {".md", ".yaml", ".yml", ".json", ".py"}
    result: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in exts or path in skip:
            continue
        if any(part in {"__pycache__", ".git", "node_modules"} for part in path.parts):
            continue
        rel = sh.rel_posix(root, path)
        if scope and not any(sh.matches(rel, [s]) for s in scope):
            continue
        result.append(path)
    return result


def split_token(token: str) -> tuple[str, str, str]:
    """`HYAI-ART-15` → (HYAI, ART, 15); `HYAI-PERM-N01` → (HYAI, PERM-N, 01).

    Второй вид — класс `PERM-N`, где буква подкласса приклеена к номеру. Различаем по форме:
    (класс, номер) или (класс-буква, цифры). Какой вариант верен, решает реестр классов.
    """
    owner, rest = token.split("-", 1)
    klass, number = rest.rsplit("-", 1)
    return owner, klass, number


def resolve_class(token: str, classes: dict) -> tuple[str, str, str]:
    """Разбор с учётом реестра: пробуем оба чтения и берём то, что объявлено."""
    owner, klass, number = split_token(token)
    if number[:1].isalpha():
        merged = f"{klass}-{number[:1]}"
        if merged in (classes.get(owner) or []):
            return owner, merged, number[1:]
    return owner, klass, number


def collect_definitions(root: Path, files: list[Path]) -> tuple[dict[str, list[str]], list[str]]:
    defs: dict[str, list[str]] = {}
    problems: list[str] = []
    for path in files:
        rel = sh.rel_posix(root, path)
        for line in path.read_text(encoding="utf-8").splitlines():
            match = DEF_RE.match(line)
            if not match:
                continue
            defs.setdefault(match.group(1), []).append(rel)
    return defs, problems


def collect_references(root: Path, files: list[Path], definitions: dict[str, list[str]]) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    for path in files:
        rel = sh.rel_posix(root, path)
        for line in path.read_text(encoding="utf-8").splitlines():
            for match in TOKEN_RE.finditer(line):
                token = match.group(1)
                if DEF_RE.match(line) and line.strip().startswith(f"`{token}`"):
                    continue
                refs.setdefault(token, []).append(f"{rel}:{token}")
    return refs


def validate_registry(registry: dict) -> list[str]:
    problems: list[str] = []
    owners = registry.get("owners") or {}
    classes = registry.get("classes") or {}
    if not owners:
        problems.append("реестр: не объявлено ни одного владельца")
    for owner, known in classes.items():
        if owner not in owners:
            problems.append(f"реестр: классы для незарегистрированного владельца {owner!r}")
        if not known:
            problems.append(f"реестр: у владельца {owner!r} нет классов")
    retired = registry.get("retired") or []
    seen: set[str] = set()
    for item in retired:
        ident = str((item or {}).get("id") or "")
        if not ident:
            problems.append("реестр: запись retired без поля id")
            continue
        if ident in seen:
            problems.append(f"реестр: {ident} дважды в retired")
        seen.add(ident)
        for field in ("was", "why", "replaced_by"):
            if not (item or {}).get(field):
                problems.append(f"реестр: retired {ident} без поля {field}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка идентификаторов правил")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    registry, problems = load_registry(root)
    if problems:
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 2
    problems.extend(validate_registry(registry))

    owners = registry.get("owners") or {}
    classes = registry.get("classes") or {}
    ignore = {str(item) for item in registry.get("ignore_references") or []}

    sources = source_files(root, registry)
    if not sources:
        print("реестр: ни один файл-источник правил не найден", file=sys.stderr)
        return 2

    definitions, _ = collect_definitions(root, sources)
    retired = {str((item or {}).get("id")): item or {} for item in registry.get("retired") or []}

    for ident, files in sorted(definitions.items()):
        owner, klass, _number = resolve_class(ident, classes)
        if owner not in owners:
            problems.append(f"{files[0]}: {ident}: владелец {owner!r} не зарегистрирован в rule-ids.yaml")
        elif klass not in (classes.get(owner) or []):
            problems.append(f"{files[0]}: {ident}: класс {klass!r} не зарегистрирован у владельца {owner!r}")
        if len(files) > 1:
            problems.append(f"{ident}: определён дважды — {', '.join(files)} (номер не переиспользуется)")
        if ident in retired:
            problems.append(f"{files[0]}: {ident}: номер выведен из обращения ({retired[ident].get('why')}); нужно новое правило")

    # Ссылки проверяются и в файлах-источниках: там их больше всего.
    # Номера без класса: владелец известен, формат — из первого выпуска.
    # Сам реестр не проверяется: в его `retired` старые номера лежат по определению.
    registry_path = root / str(((sh.manifest(root).get("validation") or {}).get("data") or {}).get("rule_ids") or "")
    for path in reference_files(root, registry, {registry_path}):
        rel = sh.rel_posix(root, path)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in LEGACY_RE.finditer(line):
                moved = re.search(rf"`?{match.group(1)}-[A-Z]+-{match.group(0)[-2:]}`?", line)
                if match.group(1) in owners and not moved:
                    problems.append(f"{rel}:{lineno}: {match.group(0)}: номер без класса — "
                                    f"формат `{match.group(1)}-<CLASS>-NN` или запись в retired")

    # Номера из retired: ищем буквально — их форма могла не разбираться как ID вовсе
    # (вид `PERM-<NN>` из первого выпуска). Строка миграции с `replaced_by` разрешена.
    retired_re = {ident: re.compile(rf"(?<![A-Z-]){re.escape(ident)}(?![A-Z0-9-])")
                  for ident in retired}
    for path in reference_files(root, registry, {registry_path}):
        rel = sh.rel_posix(root, path)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for ident, pattern in retired_re.items():
                if not pattern.search(line):
                    continue
                replacement = str(retired[ident].get("replaced_by") or "")
                if replacement and replacement in line:
                    continue
                problems.append(f"{rel}:{lineno}: {ident}: номер выведен из обращения "
                                f"({retired[ident].get('why')}); замена — {replacement}")

    references = collect_references(root, reference_files(root, registry, set()), definitions)
    for token, places in sorted(references.items()):
        if token in ignore or token in definitions:
            continue
        if token in retired:
            problems.append(f"{places[0]}: ссылка на выведенный номер {token}")
            continue
        problems.append(f"{places[0]}: ссылка на неопределённое правило {token}")

    if args.json:
        print(json.dumps({"definitions": len(definitions), "references": len(references),
                          "problems": problems}, ensure_ascii=False, indent=2))
        return 1 if problems else 0
    for problem in problems:
        print(f"  {problem}")
    print(f"\nправил: {len(definitions)}; ссылок: {len(references)}; проблем: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
