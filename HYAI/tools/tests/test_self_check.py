# SPDX-License-Identifier: GPL-3.0-only
"""Самопроверка каркаса: сборка AGENTS.md, полный конвейер, матрица доменов и профилей."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kit import ROOT, KitCopy  # noqa: E402


class AssembleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_agents_file_matches_assembly(self) -> None:
        res = self.kit.run("assemble_agents.py", "--check")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_manual_edit_is_reported_as_drift(self) -> None:
        self.kit.append("AGENTS.md", "\nПравка руками.\n")
        res = self.kit.run("assemble_agents.py", "--check")
        self.assertEqual(res.returncode, 1)
        self.assertIn("дрейф", res.stdout)

    def test_assembly_follows_active_configuration(self) -> None:
        manifest = self.kit.load("HYAI/meta/manifest.yaml")
        manifest["active"] = [item for item in manifest["active"] if item["domain"] != "narrative"]
        self.kit.dump("HYAI/meta/manifest.yaml", manifest)
        self.assertEqual(self.kit.run("assemble_agents.py", "--write").returncode, 0)
        text = self.kit.read("AGENTS.md")
        self.assertNotIn("## Домен `narrative`", text)
        self.assertIn("## Домен `software`", text)


class PipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_full_pipeline_is_green(self) -> None:
        res = self.kit.run("run_checks.py", "--skip-project")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_project_layer_is_planned_by_flag(self) -> None:
        # Слой проекта планируется по манифесту, но запускать его из теста нельзя:
        # он вызовет unittest, который вызовет этот же тест. Проверяем план, а не запуск.
        sys.path.insert(0, str(ROOT / "HYAI" / "tools"))
        import run_checks  # noqa: E402

        saved = os.environ.pop("AI_CHECKS_RUNNING_PROJECT", None)
        try:
            manifest = run_checks.sh.manifest(self.kit.root)
            with_project = run_checks.build_plan(self.kit.root, manifest, include_project=True)
            without_project = run_checks.build_plan(self.kit.root, manifest, include_project=False)
        finally:
            if saved is not None:
                os.environ["AI_CHECKS_RUNNING_PROJECT"] = saved

        self.assertTrue(any(step["layer"] == "project" for step in with_project))
        self.assertFalse(any(step["layer"] == "project" for step in without_project))


class MatrixTest(unittest.TestCase):
    """Каждая объявленная пара «домен + профиль» должна проходить структурные проверки."""

    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_every_declared_profile_passes_structure_checks(self) -> None:
        manifest = self.kit.load("HYAI/meta/manifest.yaml")
        base_active = manifest["active"]
        pairs = []
        for domain, rel in manifest["domains"].items():
            cfg = self.kit.load(rel)
            pairs.extend((domain, profile) for profile in (cfg.get("profiles") or {}))

        self.assertTrue(pairs, "в каркасе не объявлено ни одного профиля")
        for domain, profile in pairs:
            manifest["active"] = [item for item in base_active if item["domain"] not in (domain, "kit")]
            manifest["active"].append({"domain": domain, "profile": profile})
            self.kit.dump("HYAI/meta/manifest.yaml", manifest)
            for tool in ("check_domains.py", "check_manifest.py"):
                res = self.kit.run(tool)
                self.assertEqual(res.returncode, 0, f"{domain}/{profile}, {tool}:\n{res.stdout}")
        manifest["active"] = base_active
        self.kit.dump("HYAI/meta/manifest.yaml", manifest)


if __name__ == "__main__":
    unittest.main()
