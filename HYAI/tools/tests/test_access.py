# SPDX-License-Identifier: GPL-3.0-only
"""Система доступа домена: роль × призма, компетенции, контуры, выгрузки."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kit import ROOT, TOOLS, KitCopy, add_doc  # noqa: E402

sys.path.insert(0, str(TOOLS))
import resolve_access as ra  # noqa: E402


def chars(**owners: list) -> dict:
    return {
        "role": "player",
        "prism": "characters",
        "owner": "player.one",
        "characters": [
            {"id": cid, "title": cid.split(".")[-1].title(), "owner": owner, "domains": domains}
            for cid, (owner, domains) in owners.items()
        ],
    }


class ResolveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ra.load_model(ROOT, "narrative")

    def test_model_is_read_from_domain_config(self) -> None:
        self.assertIn("creator", self.model.get("roles") or {})
        self.assertEqual((self.model.get("visibility") or {}).get("values")[0], "public")

    def test_reader_sees_audience_only(self) -> None:
        doc = {"visibility": "internal", "knowledge": "common"}
        self.assertTrue(ra.resolve(self.model, {"role": "reader", "prism": "audience"}, doc)["allowed"])
        denied = ra.resolve(self.model, {"role": "reader", "prism": "scenario"}, doc)
        self.assertFalse(denied["allowed"])
        self.assertIn("недоступна", denied["reasons"][0])

    def test_unknown_role_denied_by_default(self) -> None:
        self.assertFalse(ra.resolve(self.model, {"role": "intruder", "prism": "audience"}, {})["allowed"])

    def test_secret_requires_known_by(self) -> None:
        doc = {"visibility": "internal", "knowledge": "secret"}
        self.assertFalse(ra.resolve(self.model, {"role": "player", "prism": "audience"}, doc)["allowed"])

    def test_characters_prism_respects_competence(self) -> None:
        profile = chars(
            **{
                "character.alpha": ("player.one", {"security": 4}),
                "character.beta": ("player.one", {"security": 7}),
            }
        )
        doc = {"visibility": "internal", "knowledge": "common", "requires": [{"domain": "security", "min": 6}]}
        self.assertTrue(ra.resolve(self.model, profile, doc)["allowed"])

        weak = chars(**{"character.alpha": ("player.one", {"security": 4})})
        self.assertFalse(ra.resolve(self.model, weak, doc)["allowed"])

    def test_foreign_character_is_denied(self) -> None:
        profile = chars(**{"character.other": ("player.two", {})})
        self.assertFalse(ra.resolve(self.model, profile, {"visibility": "internal"})["allowed"])

    def test_competence_map_lines(self) -> None:
        profile = chars(
            **{
                "character.alpha": ("player.one", {"security": 4}),
                "character.beta": ("player.one", {"security": 7}),
                "character.gamma": ("player.one", {}),
            }
        )
        doc = {"visibility": "internal", "knowledge": "secret", "known_by": ["character.alpha", "character.beta"],
               "requires": [{"domain": "security", "min": 6}]}
        lines = ra.competence_map(self.model, profile, doc)
        text = "\n".join(lines)
        self.assertIn("У4 (ниже порога У6)", text)
        self.assertIn("У7", text)
        self.assertIn("УН", text)


class ScopesAndExportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.kit = KitCopy()

    def tearDown(self) -> None:
        self.kit.close()

    def test_public_document_with_secret_is_flagged(self) -> None:
        add_doc(self.kit, "world/leak.md", "# Утечка", visibility="public", knowledge="secret", known_by="[a]")
        res = self.kit.run("lint_scopes.py", "--domain", "narrative")
        self.assertEqual(res.returncode, 1)
        self.assertIn("acc.open_visibility_with_secret", res.stdout)

    def test_secret_without_known_by_is_flagged(self) -> None:
        add_doc(self.kit, "world/secret.md", "# Секрет", visibility="internal", knowledge="secret")
        res = self.kit.run("lint_scopes.py", "--domain", "narrative")
        self.assertEqual(res.returncode, 1)
        self.assertIn("acc.secret_without_known_by", res.stdout)

    def test_export_keeps_only_allowed_visibility(self) -> None:
        add_doc(self.kit, "world/public.md", "# Открытое", visibility="public", knowledge="common")
        add_doc(self.kit, "world/hidden.md", "# Закрытое", visibility="spoiler", knowledge="common")
        out = self.kit.path("Exports/check")
        res = self.kit.run("build_export.py", "--domain", "narrative", "--preset", "public", "--out", str(out))
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        exported = [p.name for p in out.rglob("*.md")]
        self.assertIn("public.md", exported)
        self.assertNotIn("hidden.md", exported)
        text = (out / "world/public.md").read_text(encoding="utf-8")
        self.assertNotIn("---", text.split("\n")[0], "frontmatter должен быть снят")

    def test_unknown_preset_is_config_error(self) -> None:
        res = self.kit.run("build_export.py", "--domain", "narrative", "--preset", "ghost", "--dry-run")
        self.assertEqual(res.returncode, 2)


if __name__ == "__main__":
    unittest.main()
