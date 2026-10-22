# SPDX-License-Identifier: GPL-3.0-only
"""Тестовый помощник: одноразовая копия каркаса и мутации в ней.

Тесты не зависят от состояния рабочего дерева: каждый получает свою копию и может
ломать её как угодно, не влияя на соседние тесты и на сам репозиторий.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "HYAI" / "tools"


class KitCopy:
    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "kit"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", "Exports"))

    # --- пути и чтение ---
    def path(self, rel: str) -> Path:
        return self.root / rel

    def read(self, rel: str) -> str:
        return self.path(rel).read_text(encoding="utf-8")

    def write(self, rel: str, text: str) -> Path:
        path = self.path(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def append(self, rel: str, text: str) -> None:
        self.write(rel, self.read(rel) + text)

    # --- YAML ---
    def load(self, rel: str) -> dict:
        return yaml.safe_load(self.read(rel)) or {}

    def dump(self, rel: str, data: dict) -> None:
        self.write(rel, yaml.safe_dump(data, allow_unicode=True, sort_keys=False))

    # --- запуск ---
    def run(self, tool: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOLS / tool), "--root", str(self.root), *args],
            capture_output=True, text=True, encoding="utf-8",
        )

    def unittest(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(self.root / "AI" / "tests")],
            capture_output=True, text=True, encoding="utf-8", cwd=str(self.root),
        )

    def close(self) -> None:
        self._tmp.cleanup()


def add_doc(kit: KitCopy, rel: str, body: str, visibility: str = "internal", **extra) -> None:
    fields = {
        "id": "test." + rel.replace("/", ".").replace(".md", ""),
        "title": f'"{rel}"',
        "type": "reference",
        "status": "approved",
        "authority": "implementation",
        "visibility": visibility,
        **extra,
    }
    block = "\n".join(f"{k}: {v}" for k, v in fields.items())
    kit.write(rel, f"---\n{block}\n---\n\n{body}\n")
