# SPDX-License-Identifier: GPL-3.0-only
"""Идентификаторы правил: формат, владелец, уникальность, ссылки, выведенные номера."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kit import KitCopy  # noqa: E402


class RuleIdsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_registry_is_clean(self) -> None:
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_two_part_class_is_counted(self) -> None:
        """`HYAI-PERM-N01`: класс `PERM-N` с буквой, приклеенной к номеру. Такой ID обязан считаться."""
        res = self.kit.run("check_rules.py", "--json")
        import json
        data = json.loads(res.stdout)
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertGreater(data["definitions"], 240)

    def test_dangling_gate_reference_is_rejected(self) -> None:
        self.kit.append("HYAI/core/domains/docs/README.md", "\nСм. `HYAI-PERM-G99`.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("HYAI-PERM-G99", res.stdout)

    def test_two_part_class_must_be_registered(self) -> None:
        """Класс `PERM-Z` не объявлен — правило с ним не должно пройти."""
        self.kit.append("HYAI/core/kernel/policies/permissions.md",
                        "\n`HYAI-PERM-Z01`. Несуществующий подкласс.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("PERM-Z", res.stdout)

    def test_unknown_owner_is_rejected(self) -> None:
        self.kit.append("HYAI/core/domains/narrative/policy.md",
                        "\n`ZZZ-POL-01`. Правило неизвестного владельца.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("владелец", res.stdout)

    def test_duplicate_id_is_rejected(self) -> None:
        self.kit.write("HYAI/core/domains/narrative/text.md",
                       self.kit.read("HYAI/core/domains/narrative/text.md")
                       + "\n`NR-TXT-01`. Второе определение того же номера.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("дважды", res.stdout)

    def test_sources_are_scanned_for_references(self) -> None:
        """Файл-источник тоже ссылается: строки-определения пропускаются, остальные проверяются."""
        self.kit.append("HYAI/core/domains/docs/policy.md", "\nСм. также `HYAI-INT-99`.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("HYAI-INT-99", res.stdout)

    def test_dangling_reference_is_rejected(self) -> None:
        self.kit.append("HYAI/core/domains/docs/README.md", "\nСм. также `HYAI-INT-99`.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("неопределённое правило", res.stdout)

    def test_number_without_class_is_rejected(self) -> None:
        """`NR-09` — формат первого выпуска: правило выпало бы из учёта молча."""
        self.kit.append("HYAI/core/domains/narrative/policy.md", "\n`NR-09`. Черновик не цитируется.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("номер без класса", res.stdout)

    def test_question_id_is_not_a_legacy_rule_reference(self) -> None:
        """Идентификатор вопроса `Q-KIT-01` не является правилом `KIT-01`."""
        self.kit.append("HYAI/meta/questions/kit.md", "\nСм. `Q-KIT-01`.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_migration_note_is_allowed(self) -> None:
        """Строка «старый → новый» законна: это карта переименования, а не действующее правило."""
        self.kit.append("CHANGELOG.md", "\n`NR-09` → `NR-POL-09`.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 0, res.stdout)

    def test_retired_number_is_caught_in_old_form(self) -> None:
        """`PERM-G02` из первого выпуска не разбирается как ID — искать надо буквально."""
        self.kit.append("HYAI/core/domains/narrative/policy.md", "\n`PERM-G02`. Удаление файла.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("выведен из обращения", res.stdout)

    def test_retired_number_cannot_be_reused(self) -> None:
        registry = self.kit.read("HYAI/meta/schema/rule-ids.yaml")
        registry = registry.replace("retired:\n", "retired:\n"
                                    "  - id: \"NR-POL-09\"\n"
                                    "    was: \"старое правило о копиях\"\n"
                                    "    why: \"история живёт в git\"\n"
                                    "    replaced_by: \"HYAI-ART-15\"\n")
        self.kit.write("HYAI/meta/schema/rule-ids.yaml", registry)
        self.kit.write("HYAI/core/domains/narrative/policy.md",
                       self.kit.read("HYAI/core/domains/narrative/policy.md")
                       + "\n`NR-POL-09`. Копия файлов для истории.\n")
        res = self.kit.run("check_rules.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("выведен из обращения", res.stdout)


class ExportGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_draft_is_not_exported(self) -> None:
        """NR-EXP-02: draft не выгружается никому, даже при visibility: public."""
        self.kit.write("world/draft-note.md",
                       "---\nid: nr.draft\ntitle: \"Черновик\"\ntype: entity\nstatus: draft\n"
                       "authority: contract\nvisibility: public\nknowledge: common\n---\n\n# Черновик\n\nТекст.\n")
        res = self.kit.run("build_export.py", "--domain", "narrative", "--preset", "public", "--dry-run")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("по статусу 1", res.stdout)

    def test_approved_public_is_exported(self) -> None:
        self.kit.write("world/public-note.md",
                       "---\nid: nr.pub\ntitle: \"Заметка\"\ntype: entity\nstatus: approved\n"
                       "authority: contract\nvisibility: public\nknowledge: common\n---\n\n# Заметка\n\nТекст.\n")
        res = self.kit.run("build_export.py", "--domain", "narrative", "--preset", "public", "--dry-run")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("world/public-note.md", res.stdout)

    def test_unknown_preset_is_refused(self) -> None:
        res = self.kit.run("build_export.py", "--domain", "narrative", "--preset", "ghost", "--dry-run")
        self.assertEqual(res.returncode, 2)


if __name__ == "__main__":
    unittest.main()
