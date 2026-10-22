#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Контракт манифеста: версия формата, заблокированные зоны, отсутствие прав в профилях.

Проверяет правила `MERGE-01..06` и `KIT-POL-01`: то, что можно ослабить только случайно, — а значит, надо проверять машинно.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

REQUIRED_KEYS = ("apiVersion", "kind", "metadata", "entrypoint", "active", "domains", "paths", "path_map", "decisions", "report", "validation", "permissions")
RESERVED_SCOPES = {"kernel", "project"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка контракта манифеста")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    problems: list[str] = []

    if not man:
        print("HYAI/meta/manifest.yaml не найден", file=sys.stderr)
        return 2

    api = str(man.get("apiVersion") or "")
    if api != "hyai/v1":
        problems.append(f"HYAI/meta/manifest.yaml: apiVersion={api!r}, ожидалось hyai/v1")
    for key in REQUIRED_KEYS:
        if key not in man or man.get(key) in (None, "", [], {}):
            problems.append(f"HYAI/meta/manifest.yaml: нет обязательного раздела `{key}`")

    approval = ((man.get("permissions") or {}).get("write") or {}).get("require_approval_for") or []
    zones = [str(z) for z in (man.get("protected_zones") or [])]
    if not zones:
        print("HYAI/meta/manifest.yaml: нет protected_zones — проверять нечего", file=sys.stderr)
        return 2
    for zone in zones:
        covered = any(sh.matches(zone, [str(pat)]) or sh.matches(zone.rstrip("/") + "/x", [str(pat)]) for pat in approval)
        if not covered:
            problems.append(f"HYAI/meta/manifest.yaml: зона {zone!r} не входит в permissions.write.require_approval_for (HYAI-PERM-G05)")

    forbidden_in_domain = ("permissions", "non_overridable", "precedence")
    for name, cfg in sh.domain_configs(root, man).items():
        for key in forbidden_in_domain:
            if key in cfg["data"]:
                problems.append(f"{cfg['rel']}: домен не задаёт `{key}` — это уровень репозитория (MERGE-01)")
        scope = cfg["data"].get("decisions_scope")
        if scope and scope not in ((man.get("decisions") or {}).get("scopes") or {}):
            problems.append(f"{cfg['rel']}: decisions_scope={scope!r} отсутствует в decisions.scopes")

        for profile, rel in (cfg["data"].get("profiles") or {}).items():
            path = root / str(rel)
            if path.exists() and "permissions" in (sh.load_yaml(path) or {}):
                problems.append(f"{rel}: профиль не задаёт права (MERGE-04, KIT-POL-09)")

    scopes = set(((man.get("decisions") or {}).get("scopes") or {}))
    report_scopes = set((man.get("report") or {}).get("allowed_scopes") or [])
    for scope in report_scopes - scopes - {"project"}:
        problems.append(f"HYAI/meta/manifest.yaml: report.allowed_scopes содержит {scope!r} без области решений")

    declared = set(man.get("domains") or {})
    for pattern, domain in (man.get("path_map") or {}).items():
        if domain not in declared | RESERVED_SCOPES:
            problems.append(f"HYAI/meta/manifest.yaml: path_map[{pattern!r}] указывает на незаявленный домен {domain!r}")

    active = sh.active_pairs(man)
    if len({d for d, _ in active}) != len(active) and man.get("bootstrap", {}).get("require_domain_and_profile"):
        duplicates = [d for d in {d for d, _ in active} if sum(1 for x, _ in active if x == d) > 1]
        if duplicates:
            problems.append(f"HYAI/meta/manifest.yaml: несколько профилей одного домена в active: {', '.join(duplicates)}")

    return sh.emit(problems, "контракт манифеста", args.json)


if __name__ == "__main__":
    raise SystemExit(main())
