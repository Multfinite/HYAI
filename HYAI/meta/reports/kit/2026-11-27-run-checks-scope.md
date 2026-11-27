---
id: report.kit.2026-11-27-run-checks-scope
title: "Соразмерность проверок: полный run_checks только по необходимости"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: approved
authority: none
visibility: internal
date: "2026-11-27"
workflow: task
decisions: [KIT-0010]
---

# Соразмерность проверок

## Задача

Обновить правило HYAI про `run_checks.py`: полный конвейер — только по необходимости, а по
умолчанию проверять только изменённые файлы и затронутую зону. Норма объявлена владельцем [А],
домен `kit`, профиль `kit/domain-builder`.

## Что сделано

- `HYAI/core/kernel/policies/interaction.md` — добавлено `HYAI-INT-31` с формулировкой объёма проверок.
- `HYAI/core/kernel/agents.md` и сгенерированный `AGENTS.md` — вместо безусловного полного прогона ссылка на `HYAI-INT-31`.
- `HYAI/core/kernel/workflows/task.md` (WF-04), `HYAI/core/kernel/policies/artifacts.md` (`HYAI-ART-21`), `HYAI/core/kernel/templates/report.md`, `HYAI/core/shared/templates/skill-domain.md` — проверка стала соразмерной правке.
- `HYAI/core/domains/software/workflows/feature.md`, `software/profiles/code/profile.yaml`, `software/profiles/code/README.md`, `narrative/workflows/lore-change.md`, `narrative/workflows/entity-card.md` — уточнены формулировки про зону проверок.
- `HYAI/meta/decisions/kit/KIT-0010-run-checks-scope.md` — норма зафиксирована; индексы решений обновлены.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| полный конвейер | `python3 HYAI/tools/run_checks.py` | 0 падений |
| сборка входа и навыков | `assemble_agents.py --check`, `build_skills.py --check` | дрейфа нет |

Полный конвейер запущен намеренно: затронуто ядро и шаблоны, то есть случай «по необходимости» из `HYAI-INT-31`.

## Открытые вопросы

—
