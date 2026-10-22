# SPDX-License-Identifier: GPL-3.0-only
"""Отчёты (домен, профиль, вид) и решения (область, affects, индекс)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kit import KitCopy  # noqa: E402

REPORT = """---
id: report.{domain}.2026-10-22-sample
title: "Пример"
type: report
report_kind: {kind}
domain: {domain}
profile: {profile}
status: review
authority: none
visibility: internal
date: "2026-10-22"
workflow: {workflow}
decisions: []
---

# Пример

## Задача

Текст.

## Что сделано

Текст.

## Проверка

Текст.

## Открытые вопросы

Нет.
"""

ANALYSIS = """---
id: report.{domain}.2026-10-22-sample
title: "Разбор"
type: report
report_kind: analysis
domain: {domain}
profile: {profile}
status: review
authority: none
visibility: internal
date: "2026-10-22"
workflow: audit
decisions: []
---

# Разбор

## Вопрос

Текст.

## Разбор

Текст.

## Варианты

Текст.

## Рекомендация

Текст.

## Открытые вопросы

Нет.
"""


class ReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def _add(self, rel: str, text: str) -> None:
        self.kit.write(rel, text)
        index = self.kit.read("HYAI/meta/reports/README.md")
        name = Path(rel).name
        entry = Path(rel).relative_to("HYAI/meta/reports").as_posix()
        if name not in index:
            self.kit.write("HYAI/meta/reports/README.md", index.rstrip() + f"\n| [`{entry}`]({entry}) | — | — | — |\n")

    def test_kit_reports_are_valid(self) -> None:
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_report_domain_must_match_directory(self) -> None:
        self._add("HYAI/meta/reports/software/2026-10-22-sample.md", REPORT.format(
            domain="narrative", profile="narrative/lore", kind="task", workflow="narrative/lore-change"))
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("не совпадает с каталогом", res.stdout)

    def test_unknown_workflow_is_reported(self) -> None:
        self._add("HYAI/meta/reports/software/2026-10-22-sample.md", REPORT.format(
            domain="software", profile="software/code", kind="task", workflow="software/teleport"))
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("неизвестный workflow", res.stdout)

    def test_missing_section_is_reported(self) -> None:
        text = REPORT.format(domain="software", profile="software/code", kind="task",
                             workflow="software/feature").replace("## Проверка", "## Итог")
        self._add("HYAI/meta/reports/software/2026-10-22-sample.md", text)
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("Проверка", res.stdout)

    def test_analysis_report_needs_analysis_sections(self) -> None:
        text = ANALYSIS.format(domain="software", profile="software/analysis").replace("## Разбор", "## Итог")
        self._add("HYAI/meta/reports/software/2026-10-22-sample.md", text)
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("Разбор", res.stdout)

    def test_report_missing_from_index_is_reported(self) -> None:
        self.kit.write("HYAI/meta/reports/software/2026-10-22-unlisted.md", REPORT.format(
            domain="software", profile="software/code", kind="task", workflow="software/feature"))
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("отсутствует в", res.stdout)


class DecisionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def _decision(self, scope_dir: str, name: str, scope: str, affects: list[str], extra: str = "") -> None:
        rel = f"HYAI/meta/decisions/{scope_dir}/{name}"
        self.kit.write(rel, f"""---
id: decision.{scope}.{name.split('-')[0]}-{name.split('-')[1]}
title: "Тест"
type: decision
status: review
authority: contract
visibility: internal
scope: {scope}
affects: {affects}
{extra}---

# Тест

## Решение

Текст.
""")
        index = self.kit.read("HYAI/meta/decisions/README.md")
        decision_id = f"{name.split('-')[0]}-{name.split('-')[1]}"
        self.kit.write("HYAI/meta/decisions/README.md", index.rstrip() + f"\n| [`{decision_id}`]({scope_dir}/{name}) | {scope} | Тест | review |\n")

    def test_kit_decisions_are_valid(self) -> None:
        res = self.kit.run("check_decisions.py")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_decision_scope_must_match_directory(self) -> None:
        self._decision("software", "SW-0001-sample.md", "narrative", [])
        res = self.kit.run("check_decisions.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("не совпадает с каталогом", res.stdout)

    def test_decision_affects_must_exist(self) -> None:
        self._decision("software", "SW-0001-sample.md", "software", '["src/ghost.py"]')
        res = self.kit.run("check_decisions.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("src/ghost.py", res.stdout)

    def test_cross_domain_decision_must_live_in_project(self) -> None:
        self._decision("software", "SW-0001-sample.md", "software", '["src/auth/README.md"]',
                       extra="affects_domains: [software, narrative]\n")
        res = self.kit.run("check_decisions.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("project", res.stdout)

    def test_unquoted_decision_number_in_report_is_rejected(self) -> None:
        text = REPORT.format(domain="software", profile="software/code", kind="task",
                             workflow="software/feature").replace("decisions: []", "decisions: [0001]")
        self.kit.write("HYAI/meta/reports/software/2026-10-22-sample.md", text)
        index = self.kit.read("HYAI/meta/reports/README.md")
        self.kit.write("HYAI/meta/reports/README.md", index.rstrip() + "\n| [`software/2026-10-22-sample.md`](software/2026-10-22-sample.md) | — | — | — |\n")
        res = self.kit.run("check_report.py")
        self.assertEqual(res.returncode, 1)
        self.assertIn("кавычк", res.stdout)


if __name__ == "__main__":
    unittest.main()
