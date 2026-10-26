#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Сборка `AGENTS.md` из ядра и активных доменов.

`AGENTS.md` — генерируемый артефакт, а не место для правок: одна точка входа при любом
числе доменов. `--check` сравнивает файл в репозитории с результатом сборки и возвращает
`rc=1` при расхождении («дрейф сборки»).
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

HEADER = """<!-- generated: true -->
<!-- source: {{HYAI}}core/kernel/agents.md + {{HYAI}}core/domains/<domain>/agents.md -->
<!-- правки вносятся в источники; проверка: assemble_agents.py --check -->
"""


def framework_prefix(man: dict) -> str:
    """Префикс каталогов каркаса для инструкций агенту: `framework.prefix` (иначе `framework.root`)."""
    cfg = man.get("framework") or {}
    return str(cfg.get("prefix") or cfg.get("root") or "")


def render(root: Path, man: dict) -> tuple[str, list[str]]:
    problems: list[str] = []
    prefix = framework_prefix(man)
    kernel_rel = (man.get("paths") or {}).get("kernel") or "HYAI/core/kernel/"
    kernel_fragment = root / str(kernel_rel) / "agents.md"
    if not kernel_fragment.exists():
        problems.append(f"нет фрагмента ядра: {sh.rel_posix(root, kernel_fragment)}")
        kernel_text = ""
    else:
        kernel_text = kernel_fragment.read_text(encoding="utf-8").strip().replace("{{HYAI}}", prefix)

    configs = sh.domain_configs(root, man)
    parts = [HEADER.replace("{{HYAI}}", prefix), kernel_text, ""]
    active = sh.active_pairs(man)
    listing = ", ".join(f"`{d}/{p}`" for d, p in active) or "—"
    parts.append("## Активная конфигурация\n")
    parts.append(f"Домены и профили этого репозитория: {listing}.\n")
    parts.append("| Домен | Профили | Когда выбирать |")
    parts.append("| --- | --- | --- |")
    for domain, _profile in active:
        cfg = (configs.get(domain) or {}).get("data") or {}
        profiles = ", ".join(f"`{domain}/{p}`" for p in (cfg.get("profiles") or {})) or "—"
        parts.append(f"| `{domain}` | {profiles} | {cfg.get('metadata', {}).get('title', '')} |")
    parts.append("")

    seen: set[str] = set()
    for domain, _profile in active:
        if domain in seen:
            continue
        seen.add(domain)
        cfg = (configs.get(domain) or {}).get("data") or {}
        rel = cfg.get("agents")
        if not rel:
            problems.append(f"домен {domain!r}: не указан agents в манифесте домена")
            continue
        path = sh.fw(root, str(rel))
        if not path.exists():
            problems.append(f"домен {domain!r}: фрагмент не найден: {rel}")
            continue
        parts.append(path.read_text(encoding="utf-8").strip().replace("{{HYAI}}", prefix))
        parts.append("")

    text = "\n".join(parts).rstrip() + "\n"
    return text, problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Сборка AGENTS.md")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--check", action="store_true", help="только проверить дрейф")
    parser.add_argument("--write", action="store_true", help="записать результат")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    entry = str(man.get("entrypoint") or "AGENTS.md")
    target = root / entry

    text, problems = render(root, man)
    if problems:
        for problem in problems:
            print(f"  {problem}")
        print(f"\nсборка AGENTS.md: проблем: {len(problems)}")
        return 1

    current = target.read_text(encoding="utf-8") if target.exists() else ""

    if args.write or (not args.check and not current):
        target.write_text(text, encoding="utf-8")
        print(f"{entry}: записан ({len(text.splitlines())} строк)")
        return 0

    if current != text:
        diff = list(difflib.unified_diff(current.splitlines(), text.splitlines(), "репозиторий", "сборка", lineterm="", n=1))
        for line in diff[:40]:
            print(line)
        print(f"\n{entry}: дрейф сборки — запустите `assemble_agents.py --write`")
        return 1

    print(f"{entry}: актуален ({len(text.splitlines())} строк)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
