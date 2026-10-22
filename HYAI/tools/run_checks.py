#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Конвейер проверок, собранный из манифеста.

Порядок: сборка `AGENTS.md` → `validation.core` → `checks` активных доменов →
`validation.project`. Список проверок не дублируется в CI: он живёт в `HYAI/meta/manifest.yaml`.

Защита от рекурсии: дочерние процессы получают `AI_CHECKS_RUNNING_PROJECT=1`, и
проектные проверки (которые могут сами вызвать `run_checks.py`) не запускаются повторно.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

ENV_GUARD = "AI_CHECKS_RUNNING_PROJECT"


def build_plan(root: Path, man: dict, include_project: bool) -> list[dict]:
    plan: list[dict] = []
    validation = man.get("validation") or {}
    for command in validation.get("assemble") or []:
        plan.append({"layer": "assemble", "command": command})
    for command in validation.get("core") or []:
        plan.append({"layer": "core", "command": command})
    for domain, _profile in sh.active_pairs(man):
        cfg = sh.domain_configs(root, man).get(domain) or {}
        for command in (cfg.get("data") or {}).get("checks") or []:
            plan.append({"layer": f"domain:{domain}", "command": command})
    if include_project and not os.environ.get(ENV_GUARD):
        for command in validation.get("project") or []:
            plan.append({"layer": "project", "command": command})
    return plan


def argv_of(command: str) -> list[str]:
    parts = shlex.split(command)
    if parts and parts[0] in ("python", "python3"):
        parts[0] = sys.executable
    return parts


def main() -> int:
    parser = argparse.ArgumentParser(description="Конвейер проверок")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--skip-project", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    if not man:
        print("HYAI/meta/manifest.yaml не найден", file=sys.stderr)
        return 2

    plan = build_plan(root, man, include_project=not args.skip_project)
    env = os.environ.copy()
    env[ENV_GUARD] = "1"

    results: list[dict] = []
    failed = 0
    for step in plan:
        proc = subprocess.run(argv_of(step["command"]), cwd=str(root), env=env, capture_output=True, text=True, encoding="utf-8")
        ok = proc.returncode == 0
        failed += 0 if ok else 1
        results.append({"layer": step["layer"], "command": step["command"], "returncode": proc.returncode,
                        "ok": ok, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()})
        if not args.json:
            print(f"[{'OK  ' if ok else 'FAIL'}] ({step['layer']}) {step['command']}")
            if not ok:
                for stream in (proc.stdout.strip(), proc.stderr.strip()):
                    if stream:
                        print(stream)

    if args.json:
        print(json.dumps({"total": len(results), "failed": failed, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(f"\nпроверок: {len(results)}; упало: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
