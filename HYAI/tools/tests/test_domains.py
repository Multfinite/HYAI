# SPDX-License-Identifier: GPL-3.0-only
"""Структура доменов и профилей, контракт расширения каркаса."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import _shared as sh  # noqa: E402
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


class PicturePlacementAndSubmoduleSeparationTest(unittest.TestCase):
    """Размещение данных домена picture в HYAI и изоляция подмодуля в проекте-потребителе."""

    def setUp(self) -> None:
        self.kit = KitCopy()
        self._consumer_tmp: tempfile.TemporaryDirectory[str] | None = None

    def tearDown(self) -> None:
        if self._consumer_tmp is not None:
            self._consumer_tmp.cleanup()
        self.kit.close()

    def _build_consumer_with_submodule(self) -> Path:
        self._consumer_tmp = tempfile.TemporaryDirectory(prefix="hyai-consumer-")
        consumer = Path(self._consumer_tmp.name)
        submodule = consumer / "HYAI"
        shutil.copytree(self.kit.root, submodule)

        (consumer / "meta" / "hyai" / "domains" / "picture").mkdir(parents=True, exist_ok=True)
        for sub in ("briefs", "prompts", "stages", "assets"):
            (consumer / "meta" / "hyai" / "domains" / "picture" / "pictures" / sub).mkdir(parents=True, exist_ok=True)
        for folder in (
            consumer / "meta",
            consumer / "meta" / "decisions" / "project",
            consumer / "meta" / "decisions" / "picture",
            consumer / "meta" / "reports" / "picture",
        ):
            folder.mkdir(parents=True, exist_ok=True)

        (consumer / "meta" / "README.md").write_text(
            "---\nid: consumer.meta.readme\ntitle: \"Данные проекта\"\ntype: meta\n"
            "status: draft\nauthority: contract\nvisibility: internal\n---\n\n"
            "# Данные проекта\n\n- `manifest.yaml`\n- `hyai/`\n- `decisions/`\n- `reports/`\n",
            encoding="utf-8",
        )
        (consumer / "meta" / "decisions" / "README.md").write_text(
            "---\nid: consumer.decisions.readme\ntitle: \"Решения\"\ntype: meta\n"
            "status: draft\nauthority: contract\nvisibility: internal\n---\n\n"
            "# Решения\n\n- `project/`\n- `picture/`\n",
            encoding="utf-8",
        )
        (consumer / "meta" / "reports" / "README.md").write_text(
            "---\nid: consumer.reports.readme\ntitle: \"Отчёты\"\ntype: meta\n"
            "status: draft\nauthority: contract\nvisibility: internal\n---\n\n"
            "# Отчёты\n\n- `picture/`\n\n## Индекс\n\n| Отчёт | Домен | Профиль | Вид |\n| --- | --- | --- | --- |\n",
            encoding="utf-8",
        )
        (consumer / "meta" / "hyai" / "domains" / "picture" / "README.md").write_text(
            "---\nid: consumer.domain.picture.readme\ntitle: \"Проектный манифест picture\"\ntype: meta\n"
            "status: draft\nauthority: contract\nvisibility: internal\n---\n\n"
            "# Настройка домена `picture` в проекте\n\n- `manifest.yaml`\n- `pictures/`\n",
            encoding="utf-8",
        )

        domain_overlay = {
            "apiVersion": "hyai/v1",
            "kind": "AgentDomain",
            "metadata": {
                "name": "picture",
                "title": "Генерация изображений проекта",
                "status": "review",
                "updated": "2026-10-28",
                "owner": "maintainer",
            },
            "includes": ["HYAI/core/domains/picture/manifest.yaml"],
            "root_paths": ["meta/hyai/domains/picture/pictures"],
        }
        (consumer / "meta" / "hyai" / "domains" / "picture" / "manifest.yaml").write_text(
            yaml.safe_dump(domain_overlay, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

        template_man = sh.load_yaml(submodule / "HYAI" / "meta" / "manifest.yaml")
        consumer_man = {
            "apiVersion": "hyai/v1",
            "kind": "HyaiManifest",
            "metadata": {
                "name": "eidolon-consumer",
                "version": "1.0.0",
                "status": "draft",
                "updated": "2026-10-28",
                "language": "ru",
                "owner": "maintainer",
            },
            "entrypoint": "AGENTS.md",
            "entrypoints": ["AGENTS.md"],
            "active": [{"domain": "picture", "profile": "instant"}],
            "domains": {
                "picture": "meta/hyai/domains/picture/manifest.yaml",
            },
            "framework": {"root": "HYAI/", "prefix": "HYAI/HYAI/"},
            "paths": {
                "core": "HYAI/core/",
                "kernel": "HYAI/core/kernel/",
                "domains": "HYAI/core/domains/",
                "shared": "HYAI/core/shared/",
                "tools": "HYAI/tools/",
                "hyai_tools": "HYAI/tools/",
                "meta": "meta/",
                "reports": "meta/reports/",
                "decisions": "meta/decisions/",
                "schema": "HYAI/meta/schema/",
                "frontmatter_schema": "HYAI/meta/schema/frontmatter.yaml",
                "frontmatter_overlay": "HYAI/meta/schema/domains/{domain}.yaml",
            },
            "protected_zones": [
                "HYAI/core/kernel/",
                "meta/manifest.yaml",
            ],
            "optional_paths": [],
            "path_map": {
                "*.md": "project",
                "meta/**": "project",
                "meta/hyai/domains/picture/pictures/**": "picture",
            },
            "report": {
                **template_man["report"],
                "dir_pattern": "meta/reports/{scope}/",
                "allowed_scopes": ["project", "picture"],
                "index": "meta/reports/README.md",
            },
            "decisions": {
                "id_format": "{prefix}-NNNN",
                "filename": "{id}-{slug}.md",
                "index": "meta/decisions/README.md",
                "max_lines": 120,
                "scopes": {
                    "project": {"prefix": "P", "dir": "meta/decisions/project", "title": "Проектные решения"},
                    "picture": {"prefix": "PIC", "dir": "meta/decisions/picture", "title": "Решения picture"},
                },
            },
            "permissions": {
                "read": {"scope": "repo", "exclude": [".git/**"]},
                "write": {
                    "scope": "repo",
                    "require_approval_for": ["HYAI/core/kernel/**", "meta/manifest.yaml"],
                },
                "execute": {"allow": ["python3", "git"]},
                "secrets": "deny",
            },
            "validation": {
                "assemble": ["python3 HYAI/HYAI/tools/assemble_agents.py --check"],
                "core": ["python3 HYAI/HYAI/tools/check_domains.py"],
                "data": {
                    "frontmatter_schema": "HYAI/meta/schema/frontmatter.yaml",
                    "links": "HYAI/meta/lint/links.json",
                    "whitespace": "HYAI/meta/lint/whitespace.json",
                    "terms_dir": "HYAI/meta/lint/terms/",
                    "rule_ids": "HYAI/meta/schema/rule-ids.yaml",
                },
                "ci": "HYAI/.github/workflows/hyai-checks.yml",
            },
            "bootstrap": {"require_domain_and_profile": True, "max_questions": 2},
            "artifacts": {"exports_dir": "meta/exports/", "no_binaries_over_mb": 10},
        }
        (consumer / "meta" / "manifest.yaml").write_text(
            yaml.safe_dump(consumer_man, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        return consumer

    def _run_tool_on(self, consumer: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        tool = consumer / "HYAI" / "HYAI" / "tools" / script
        return subprocess.run(
            [sys.executable, str(tool), "--root", str(consumer), *args],
            cwd=consumer,
            text=True,
            capture_output=True,
        )

    def test_hyai_picture_data_lives_inside_domain_and_not_repo_root(self) -> None:
        self.assertFalse((self.kit.root / "pictures").exists())
        pic_root = self.kit.path("HYAI/core/domains/picture/pictures")
        self.assertTrue(pic_root.is_dir())
        for sub in ("briefs", "prompts", "stages", "assets"):
            self.assertTrue((pic_root / sub).is_dir(), sub)

        man = self.kit.load("HYAI/meta/manifest.yaml")
        dom = self.kit.load("HYAI/core/domains/picture/manifest.yaml")
        self.assertIn("picture", man["domains"])
        self.assertNotIn("picture", self.kit.load("HYAI/core/domains/narrative/manifest.yaml").get("profiles", {}))
        self.assertEqual(dom["root_paths"], ["HYAI/core/domains/picture/pictures"])
        self.assertEqual(man["path_map"].get("HYAI/core/domains/picture/pictures/**"), "picture")
        self.assertNotIn("pictures/**", man["path_map"])

        self.assertEqual(
            sh.resolve_scope(self.kit.root, man, "HYAI/core/domains/picture/pictures/prompts/hero-base.md"),
            "picture",
        )
        self.assertEqual(
            sh.resolve_scope(self.kit.root, man, "HYAI/core/domains/picture/policy.md"),
            "kit",
        )

        for folder in ("templates", "workflows"):
            for md_file in sorted(self.kit.path(f"HYAI/core/domains/picture/{folder}").glob("*.md")):
                content = md_file.read_text(encoding="utf-8")
                for sub in ("briefs", "prompts", "stages", "assets"):
                    self.assertNotIn(
                        f"HYAI/core/domains/picture/pictures/{sub}",
                        content,
                        f"{md_file.name} не должен жёстко направлять проектные данные внутрь подмодуля",
                    )

        sample_prompt = pic_root / "prompts" / "hero-base.md"
        sample_prompt.write_text(
            "---\nid: picture.prompt.hero.base\ntitle: \"Промпт героя\"\n"
            "type: prompt-spec\nstatus: review\nauthority: prompt\nvisibility: internal\n---\n\n"
            "# Промпт героя\n\n- safety_nsfw: strict-block [А]\n- negative_prompt: blur, extra fingers\n",
            encoding="utf-8",
        )
        for cmd in (
            ("frontmatter.py", "--check"),
            ("check_indexes.py",),
            ("lint_terms.py", "--domain", "picture", "--strict"),
            ("lint_scopes.py", "--domain", "picture"),
            ("build_export.py", "--domain", "picture", "--preset", "public", "--dry-run"),
        ):
            res = self.kit.run(*cmd)
            self.assertEqual(res.returncode, 0, f"{cmd}: {res.stdout}\n{res.stderr}")

    def test_consumer_project_with_submodule_uses_active_domain_manifest_root(self) -> None:
        consumer = self._build_consumer_with_submodule()
        man = sh.manifest(consumer)
        configs = sh.domain_configs(consumer, man)
        pic_cfg = configs["picture"]
        self.assertEqual(pic_cfg["data"]["root_paths"], ["meta/hyai/domains/picture/pictures"])
        inst = sh.profile_config(consumer, pic_cfg, "instant")
        self.assertEqual(
            inst["scope_primary"],
            [
                "meta/hyai/domains/picture/pictures/prompts/**",
                "meta/hyai/domains/picture/pictures/assets/**",
            ],
        )

        prompt_file = consumer / "meta" / "hyai" / "domains" / "picture" / "pictures" / "prompts" / "scene-base.md"
        prompt_file.write_text(
            "---\nid: picture.prompt.scene.base\ntitle: \"Сцена\"\n"
            "type: prompt-spec\nstatus: review\nauthority: prompt\nvisibility: internal\n---\n\n"
            "# Сцена\n\n- safety_nsfw: strict-block [А]\n- negative_prompt: blur, extra limbs\n",
            encoding="utf-8",
        )

        for script, extra in (
            ("assemble_agents.py", ("--write",)),
            ("assemble_agents.py", ("--check",)),
            ("check_domains.py", ()),
            ("check_manifest.py", ()),
            ("check_indexes.py", ()),
            ("lint_terms.py", ("--domain", "picture", "--strict")),
            ("lint_scopes.py", ("--domain", "picture")),
            ("build_export.py", ("--domain", "picture", "--preset", "public", "--dry-run")),
        ):
            res = self._run_tool_on(consumer, script, *extra)
            self.assertEqual(res.returncode, 0, f"{script} {extra}: {res.stdout}\n{res.stderr}")

        agents_text = (consumer / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("HYAI/HYAI/core/domains/picture/policy.md", agents_text)

        submodule_pic_files = [
            p.relative_to(consumer / "HYAI" / "HYAI" / "core" / "domains" / "picture" / "pictures").as_posix()
            for p in (consumer / "HYAI" / "HYAI" / "core" / "domains" / "picture" / "pictures").rglob("*")
            if p.is_file()
        ]
        self.assertEqual(
            sorted(submodule_pic_files),
            [".gitkeep", "assets/.gitkeep", "briefs/.gitkeep", "prompts/.gitkeep", "stages/.gitkeep"],
        )

        bad_prompt = consumer / "meta" / "hyai" / "domains" / "picture" / "pictures" / "prompts" / "bad.md"
        bad_prompt.write_text("safety_nsfw: TBD\n", encoding="utf-8")
        lint_bad = self._run_tool_on(consumer, "lint_terms.py", "--domain", "picture")
        self.assertEqual(lint_bad.returncode, 1)
        self.assertIn("pic.unset-safety-placeholder", lint_bad.stdout)

    def test_consumer_project_inline_active_root_paths_override_is_supported(self) -> None:
        consumer = self._build_consumer_with_submodule()
        man_path = consumer / "meta" / "manifest.yaml"
        man = sh.load_yaml(man_path)
        man["domains"]["picture"] = "HYAI/core/domains/picture/manifest.yaml"
        man["active"] = [
            {
                "domain": "picture",
                "profile": "instant",
                "root_paths": ["meta/hyai/domains/picture/pictures"],
            }
        ]
        man_path.write_text(yaml.safe_dump(man, allow_unicode=True, sort_keys=False), encoding="utf-8")

        for script in ("check_domains.py", "check_manifest.py", "check_indexes.py"):
            res = self._run_tool_on(consumer, script)
            self.assertEqual(res.returncode, 0, f"{script}: {res.stdout}\n{res.stderr}")

    def test_consumer_project_rejects_active_domain_pointing_into_submodule(self) -> None:
        consumer = self._build_consumer_with_submodule()
        man_path = consumer / "meta" / "manifest.yaml"
        man = sh.load_yaml(man_path)

        # Случай 1: активный домен в проекте-потребителе оставил шаблонный путь внутри подмодуля.
        man["domains"]["picture"] = "HYAI/core/domains/picture/manifest.yaml"
        man_path.write_text(yaml.safe_dump(man, allow_unicode=True, sort_keys=False), encoding="utf-8")

        res_dom = self._run_tool_on(consumer, "check_domains.py")
        self.assertEqual(res_dom.returncode, 1)
        self.assertIn("подмодул", res_dom.stdout)

        res_idx = self._run_tool_on(consumer, "check_indexes.py")
        self.assertEqual(res_idx.returncode, 1)
        self.assertIn("подмодул", res_idx.stdout)

        # Случай 2: root_paths переопределён на проектный, но path_map всё ещё ведёт внутрь подмодуля.
        man["domains"]["picture"] = "meta/hyai/domains/picture/manifest.yaml"
        man["path_map"]["HYAI/core/domains/picture/pictures/**"] = "picture"
        man_path.write_text(yaml.safe_dump(man, allow_unicode=True, sort_keys=False), encoding="utf-8")

        res_man = self._run_tool_on(consumer, "check_manifest.py")
        self.assertEqual(res_man.returncode, 1)
        self.assertIn("подмодул", res_man.stdout)


if __name__ == "__main__":
    unittest.main()
