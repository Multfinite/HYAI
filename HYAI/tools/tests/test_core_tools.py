# SPDX-License-Identifier: GPL-3.0-only
"""Ядро движков: frontmatter, ссылки, термины, пробелы, навигация."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kit import KitCopy, add_doc  # noqa: E402


class FrontmatterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_kit_frontmatter_is_clean(self) -> None:
        res = self.kit.run("frontmatter.py", "--check")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_foreign_domain_value_is_rejected(self) -> None:
        add_doc(self.kit, "src/module.md", "# Модуль", visibility="spoiler")
        res = self.kit.run("frontmatter.py", "--check")
        self.assertEqual(res.returncode, 1)
        self.assertIn("spoiler", res.stdout)

    def test_apply_uses_domain_defaults(self) -> None:
        self.kit.write("src/raw.md", "# Сырой файл\n\nБез frontmatter.\n")
        res = self.kit.run("frontmatter.py", "--apply")
        self.assertEqual(res.returncode, 0, res.stdout)
        text = self.kit.read("src/raw.md")
        self.assertIn("authority: implementation", text)
        self.assertIn("visibility: internal", text)
        again = self.kit.run("frontmatter.py", "--check")
        self.assertEqual(again.returncode, 0, again.stdout)


class LinksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_link_into_code_with_line_anchor(self) -> None:
        self.kit.write("src/auth/token.py", "def verify():\n    return True\n")
        add_doc(self.kit, "docs/token.md", "# Токен\n\nСм. [`token.py`](../src/auth/token.py#L1).\n")
        ok = self.kit.run("check_links.py")
        self.assertEqual(ok.returncode, 0, ok.stdout)

        self.kit.path("src/auth/token.py").unlink()
        broken = self.kit.run("check_links.py", "--json")
        self.assertEqual(broken.returncode, 1)
        payload = json.loads(broken.stdout)
        self.assertTrue(any("token.py" in item["target"] for item in payload["problems"]))

    def test_placeholders_in_templates_are_ignored(self) -> None:
        add_doc(self.kit, "docs/tpl.md", "# T\n\n[сущность](<путь>/{{entity}}.md)\n")
        res = self.kit.run("check_links.py")
        self.assertEqual(res.returncode, 0, res.stdout)

    def test_ignore_without_reason_is_config_error(self) -> None:
        config = json.loads(self.kit.read("HYAI/meta/lint/links.json"))
        config["ignore"] = [{"path": "docs/x.md", "target": "missing.png"}]
        self.kit.write("HYAI/meta/lint/links.json", json.dumps(config, ensure_ascii=False))
        self.assertEqual(self.kit.run("check_links.py").returncode, 2)


class TermsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_rule_without_required_fields_is_config_error(self) -> None:
        config = json.loads(self.kit.read("HYAI/meta/lint/terms/software.json"))
        config["rules"].append({"id": "sw.bad", "pattern": "x", "reason": "test"})
        self.kit.write("HYAI/meta/lint/terms/software.json", json.dumps(config, ensure_ascii=False))
        self.assertEqual(self.kit.run("lint_terms.py").returncode, 2)

    def test_domain_rule_applies_only_to_its_paths(self) -> None:
        config = json.loads(self.kit.read("HYAI/meta/lint/terms/software.json"))
        config["rules"] = [{
            "id": "sw.forbidden-tenant", "severity": "error", "pattern": "\\bTenantAccount\\b",
            "applies_to": ["src/**"], "reason": "тест",
        }]
        self.kit.write("HYAI/meta/lint/terms/software.json", json.dumps(config, ensure_ascii=False))

        self.kit.write("world/note.md", "# Заметка\n\nTenantAccount упомянут в тексте.\n")
        clean = self.kit.run("lint_terms.py", "--domain", "software")
        self.assertEqual(clean.returncode, 0, clean.stdout)

        self.kit.write("src/model.py", "class TenantAccount:\n    pass\n")
        dirty = self.kit.run("lint_terms.py", "--domain", "software")
        self.assertEqual(dirty.returncode, 1)
        self.assertIn("src/model.py", dirty.stdout)


    def test_flattery_in_report_is_an_error(self) -> None:
        """HELPER: лесть в отчёте ловится правилом ядра, в тексте продукта — нет."""
        self.kit.write("docs/note.md", "# Заметка\n\nОтличный вопрос, разберём.\n")
        clean = self.kit.run("lint_terms.py")
        self.assertEqual(clean.returncode, 0, clean.stdout)

        self.kit.write("HYAI/meta/reports/kit/2026-10-22-flattery.md",
                       "# Отчёт\n\nОтличный вопрос! Вы абсолютно правы.\n")
        dirty = self.kit.run("lint_terms.py")
        self.assertEqual(dirty.returncode, 1)
        self.assertIn("kernel.no-flattery", dirty.stdout)


class WhitespaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_markdown_two_space_break_allowed_python_not(self) -> None:
        self.kit.write("docs/break.md", "---\nid: x\ntitle: \"x\"\ntype: meta\nstatus: approved\nauthority: none\nvisibility: internal\n---\n\nСтрока  \nПродолжение\n")
        self.assertEqual(self.kit.run("whitespace.py", "docs/break.md").returncode, 0)

        self.kit.write("src/bad.py", "def f():\n    return 1  \n")
        self.assertEqual(self.kit.run("whitespace.py", "src/bad.py").returncode, 1)


class NavigationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_governed_directory_needs_readme_and_mentions(self) -> None:
        add_doc(self.kit, "HYAI/core/newdir/one.md", "# Один")
        res = self.kit.run("check_indexes.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("HYAI/core/newdir/", res.stdout)

        self.kit.write("HYAI/core/newdir/README.md", "---\nid: x.readme\ntitle: \"x\"\ntype: meta\nstatus: approved\nauthority: contract\nvisibility: internal\n---\n\n# newdir\n\n- one.md\n")
        ok = self.kit.run("check_indexes.py")
        self.assertEqual(ok.returncode, 0, ok.stdout)

    def test_registry_ids_are_globally_unique(self) -> None:
        config = self.kit.load("HYAI/core/domains/software/registry/documents.yaml")
        config["documents"][0]["id"] = "repo.agents"
        self.kit.dump("HYAI/core/domains/software/registry/documents.yaml", config)
        res = self.kit.run("check_indexes.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("дубль id", res.stdout)


if __name__ == "__main__":
    unittest.main()
