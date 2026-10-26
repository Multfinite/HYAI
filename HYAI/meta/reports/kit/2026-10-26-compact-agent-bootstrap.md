---
id: report.kit.2026-10-26-compact-agent-bootstrap
title: "Перегруппировка общего входа агента"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-10-26"
workflow: task
decisions: ["KIT-0001", "P-0001"]
cross_scope:
  - path: "HYAI/core/kernel/agents.md"
    why: "Перегруппировка общего входа по одобренному владельцем draft"
    profile: "project/maintainer"
  - path: "HYAI/meta/decisions/project/P-0001-shared-agent-bootstrap.md"
    why: "Фиксация требований общего входа для всех активных доменов"
    profile: "project/maintainer"
---

# Перегруппировка общего входа агента

## Задача

Сделать общий вход агента короче и яснее за счёт группировки по этапам работы и сокращения повторов. Численная цель по токенам не ставилась; обязательные правила и их смысл должны сохраниться.

## Что сделано

- `HYAI/core/kernel/agents.md` — сгруппированы домен/профиль, источники, ограничения, общение, провенанс, ворота и результат; уточнены сокращённые формулировки, чтобы сохранить обязательные детали.
- `AGENTS.md` — пересобран из обновлённого источника и прежней активной конфигурации/доменных фрагментов.
- `HYAI/meta/decisions/kit/KIT-0001-agent-entrypoint-structure.md` — зафиксировано решение о структуре общего входа (`status: review`).
- `HYAI/meta/decisions/project/P-0001-shared-agent-bootstrap.md` — зафиксированы общие требования для активных доменов (`status: review`).
- Обновлены индексы решений и отчётов.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Формат патча | `git diff --check` | Успешно (`rc=0`) |
| Сборка entrypoint | Ручная сверка источника и генерации | Префикс `AGENTS.md` совпадает с `kernel/agents.md`; хвост активной конфигурации и доменов сохранён. Автопроверка недоступна: отсутствует `PyYAML`. |
| Полный конвейер | `python3 HYAI/tools/run_checks.py` | Не запущен: `ModuleNotFoundError: No module named 'yaml'` при импорте `PyYAML`. Аналогично заблокированы `assemble_agents.py --check`, `check_decisions.py` и `check_report.py`. |

## Открытые вопросы

- `Q-KIT-01` — поведение host/runtime при загрузке `AGENTS.md` не установлено; поэтому эффект на фактические токены не измерялся.
- Решения оставлены в `review`; `approved` ставит владелец.
