# SPDX-License-Identifier: GPL-3.0-only
"""Сборщик страницы переноса picture/handoff-page: автономность и отказ на битых входах."""

from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parents[2]
GENERATOR = FRAMEWORK / "core/domains/picture/templates/build_handoff_page.py"
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg=="
)


def manifest(frames: list[dict]) -> dict:
    return {
        "slug": "demo",
        "title": "Демо: промпт + картинка",
        "caption": "тестовый манифест",
        "note": "<b>Инструкция.</b> Приложите картинку и вставьте промпт.",
        "frames": frames,
    }


class HandoffPageTest(unittest.TestCase):
    def render(self, data: dict):
        tmp = tempfile.TemporaryDirectory()
        base = Path(tmp.name)
        (base / "images").mkdir()
        (base / "images" / "a.png").write_bytes(PNG)
        (base / "images" / "b.png").write_bytes(PNG)
        path = base / "manifest.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        out = base / "out"
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--manifest", str(path), "--out-dir", str(out)],
            capture_output=True, text=True,
        )
        return tmp, out, result

    def test_render_is_self_contained(self):
        frames = [
            {"id": "01", "caption": "A", "image": "images/a.png", "prompt_a": "Prompt A", "prompt_b": "Single A"},
            {"id": "02", "caption": "B", "image": "images/b.png", "prompt_a": "Prompt B"},
        ]
        tmp, out, result = self.render(manifest(frames))
        try:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            page = (out / "demo-handoff.html").read_text(encoding="utf-8")
            self.assertEqual(page.count('<section class="card"'), 2)
            self.assertEqual(page.count("data:image/"), 2)
            self.assertNotIn("__HANDOFF_", page)
            self.assertNotIn("sandbox:", page)
            self.assertNotRegex(page, r'(?:src|href)="https?://')
            self.assertIn("HAS_B = true", page)
            self.assertIn("Prompt A", page)
            self.assertIn("Prompt B", page)
            self.assertTrue((out / "demo-handoff.txt").is_file())
            with zipfile.ZipFile(out / "demo-handoff.zip") as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(len(z.namelist()), 8)
        finally:
            tmp.cleanup()

    def test_missing_prompt_is_rejected(self):
        frames = [{"id": "01", "caption": "A", "image": "images/a.png"}]
        tmp, _out, result = self.render(manifest(frames))
        try:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("prompt_a", result.stderr)
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
