# SPDX-License-Identifier: GPL-3.0-only
"""Структура доменов и профилей, контракт расширения каркаса."""

from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kit import KitCopy  # noqa: E402


class DomainStructureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_kit_is_structurally_valid(self) -> None:
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_profile_without_checklist_is_rejected(self) -> None:
        rel = "HYAI/core/domains/software/profiles/code/profile.yaml"
        data = self.kit.load(rel)
        data["checklist"] = ["один вопрос"]
        self.kit.dump(rel, data)
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("чек-лист", res.stdout)

    def test_profile_may_not_declare_permissions(self) -> None:
        rel = "HYAI/core/domains/software/profiles/architect/profile.yaml"
        data = self.kit.load(rel)
        data["permissions"] = {"write": {"scope": "repo"}}
        self.kit.dump(rel, data)
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("permissions", res.stdout)

    def test_domain_roots_must_not_overlap(self) -> None:
        rel = "HYAI/core/domains/narrative/manifest.yaml"
        data = self.kit.load(rel)
        data["root_paths"] = list(data.get("root_paths") or []) + ["src"]
        self.kit.dump(rel, data)
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("уже принадлежит", res.stdout)

    def test_domain_without_authority_is_rejected(self) -> None:
        rel = "HYAI/core/domains/kit/manifest.yaml"
        data = self.kit.load(rel)
        data.pop("authority", None)
        self.kit.dump(rel, data)
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("authority", res.stdout)

    def test_flag_field_is_rejected(self) -> None:
        rel = "HYAI/core/domains/software/profiles/code/profile.yaml"
        data = self.kit.load(rel)
        data["self_editable"] = True
        self.kit.dump(rel, data)
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("KIT-0001", res.stdout)

    def test_engines_must_not_know_domain_names(self) -> None:
        tool = self.kit.path("HYAI/tools/whitespace.py")
        tool.write_text(tool.read_text(encoding="utf-8") + "\n# narrative\n", encoding="utf-8")
        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("KIT-INV-01", res.stdout)


class ManifestContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_manifest_contract_is_clean(self) -> None:
        res = self.kit.run("check_manifest.py")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_locked_path_must_be_covered_by_approval(self) -> None:
        rel = "HYAI/meta/manifest.yaml"
        data = self.kit.load(rel)
        approval = data["permissions"]["write"]["require_approval_for"]
        data["permissions"]["write"]["require_approval_for"] = [p for p in approval if "HYAI/core/kernel/**" not in p]
        self.kit.dump(rel, data)
        res = self.kit.run("check_manifest.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("HYAI-PERM-G05", res.stdout)

    def test_domain_may_not_redefine_permissions(self) -> None:
        rel = "HYAI/core/domains/software/manifest.yaml"
        data = self.kit.load(rel)
        data["permissions"] = {"write": {"scope": "repo"}}
        self.kit.dump(rel, data)
        res = self.kit.run("check_manifest.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("permissions", res.stdout)

    def test_old_api_version_is_rejected(self) -> None:
        rel = "HYAI/meta/manifest.yaml"
        data = self.kit.load(rel)
        data["apiVersion"] = "agent.governance/v1"
        self.kit.dump(rel, data)
        res = self.kit.run("check_manifest.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("apiVersion", res.stdout)


class ExtensionTest(unittest.TestCase):
    """Новый профиль добавляется данными: правки HYAI/tools/*.py не требуются (KIT-POL-07)."""

    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_new_profile_from_existing_one_passes_checks(self) -> None:
        src = self.kit.path("HYAI/core/domains/software/profiles/code")
        dst = self.kit.path("HYAI/core/domains/software/profiles/reviewer")
        shutil.copytree(src, dst)
        readme = dst / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8").replace("software/code", "software/reviewer")
            + "\n## Чего не делает\n\n- Не меняет контракты.\n",
            encoding="utf-8",
        )
        profile = self.kit.load("HYAI/core/domains/software/profiles/reviewer/profile.yaml")
        profile["metadata"]["name"] = "reviewer"
        profile["topic"] = "Ревью изменений"
        profile["scope_primary"] = ["docs/**", "HYAI/meta/reports/**"]
        self.kit.dump("HYAI/core/domains/software/profiles/reviewer/profile.yaml", profile)

        manifest_rel = "HYAI/core/domains/software/manifest.yaml"
        manifest = self.kit.load(manifest_rel)
        manifest["profiles"]["reviewer"] = "HYAI/core/domains/software/profiles/reviewer/profile.yaml"
        self.kit.dump(manifest_rel, manifest)

        res = self.kit.run("check_domains.py")
        self.assertEqual(res.returncode, 0, res.stdout)


if __name__ == "__main__":
    unittest.main()
