---
id: report.kit.2026-11-23-literary-agents-and-claude-skills
title: "Литературные агенты и перевод каталога навыков в .claude"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-11-23"
workflow: task
decisions: ["KIT-0008", "KIT-0009"]
cross_scope:
  - path: "HYAI/meta/manifest.yaml"
    why: "перенос skills.out из .github/skills в .claude/skills; защищённая зона, одобрение владельца"
  - path: "README.md"
    why: "синхронизация ссылок на каталог навыков"
  - path: "CHANGELOG.md"
    why: "фиксация миграции и нового блока агентов"
---

# Литературные агенты и перевод каталога навыков в `.claude`

## Задача

Добавить в `.claude/agents/` литературно-сценарный блок ролей (структура и драматизм, фактура и текст,
логика вселенной, голоса персонажей, финальная вычитка) и завершить перевод генерируемого каталога
навыков из `.github/skills/` в `.claude/skills/`, чтобы агентские оболочки читали один каталог.

## Что сделано

- `.claude/agents/Screenwriter.md` — архитектор сюжета: фабула, поэпизодник, арки, темп.
- `.claude/agents/Worldbuilder.md` — лор-мастер: законы мира, история, география, системы.
- `.claude/agents/Novelist.md` — прозаик: атмосфера, сенсорика, ритм, стиль.
- `.claude/agents/Dialogue Specialist.md` — диалогист: голоса, лексикон, подтекст.
- `.claude/agents/Literary Editor.md` — редактор: стиль, логика, целостность.
- `.claude/agents/README.md` — два блока роли, пайплайн литературной команды, формат агента.
- `HYAI/meta/manifest.yaml` — `skills.out` переведён на `.claude/skills/`.
- `HYAI/meta/schema/frontmatter.yaml` — исключены `.claude/skills` и `.claude/agents`.
- `README.md`, `CHANGELOG.md`, `HYAI/tools/README.md`, `HYAI/core/shared/README.md`,
  `HYAI/tools/build_skills.py`, `HYAI/tools/tests/test_skills.py` — ссылки и тест приведены к новому пути.
- `KIT-0008`, `KIT-0009` — уточнены пути каталога; норма не менялась.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Сборка входа | `python3 HYAI/tools/assemble_agents.py --check` | актуален, 185 строк |
| Сборка навыков | `python3 HYAI/tools/build_skills.py --check` | без ошибок, 47 предупреждений о длине |
| Конвейер | `python3 HYAI/tools/run_checks.py --skip-project` | 30 проверок, 0 падений |
| Самопроверка | `python3 -m unittest HYAI/tools/tests/test_self_check.py -v` | 8 тестов, успешно |

## Открытые вопросы

- `Technical Writer` уже существовал в `.claude/agents/`; новых правок не потребовалось.
- Старый путь `.github/skills/` остаётся только в пояснительной заметке `KIT-0008` как исторический.
