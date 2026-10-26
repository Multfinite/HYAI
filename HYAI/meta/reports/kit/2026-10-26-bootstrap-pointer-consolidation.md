---
id: report.kit.2026-10-26-bootstrap-pointer-consolidation
title: "Сокращение повторов в общем входе агента"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-10-26"
workflow: task
decisions: ["KIT-0001"]
cross_scope:
  - path: "HYAI/core/kernel/agents.md"
    why: "Сокращены повторные инструкции защищённого общего входа по одобренному владельцем изменению"
    profile: "project/maintainer"
  - path: "AGENTS.md"
    why: "Пересобран генерируемый общий entrypoint из источников"
    profile: "project/maintainer"
---

# Сокращение повторов в общем входе агента

## Задача

Сократить повторение правил выбора пары и оформления результата в общем входе, оставив подробности в канонических источниках. Защищённый draft показан владельцу и одобрен до изменения.

## Что сделано

- `HYAI/core/kernel/agents.md`, §1 — краткий маршрут выбора домена/профиля с указателями на `routing.md` и `interaction.md`; сохранены приоритет явного выбора, фиксация пары и требование объявить её до начала работы.
- `HYAI/core/kernel/agents.md`, §7 — краткая отсылка к WF-05 для отчёта, индекса и решения; отдельно оставлена обязательная команда полного конвейера и правило исправлять, а не отключать упавшие проверки.
- `AGENTS.md` — пересобран генератором; вручную не редактировался. Размер источника и entrypoint уменьшился на 564 байта и 10 строк; это не измерение токенов.

Нормы, safety-сводка, правила общения и доменные фрагменты не менялись. Число токенов и поведение host/runtime не измерялись.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Дрейф генерации | `/tmp/hyai-token-check-venv/bin/python HYAI/tools/assemble_agents.py --check` | Успешно; `AGENTS.md` актуален. |
| Конвейер | `/tmp/hyai-token-check-venv/bin/python HYAI/tools/run_checks.py --skip-project` | 19 проверок, упало 0. |
| Набор тестов | `/tmp/hyai-token-check-venv/bin/python -m unittest discover -s HYAI/tools/tests` | 68 тестов, успешно. |
| Патч | `git diff --check` | Успешно. |

PyYAML используется только во временном окружении `/tmp/hyai-token-check-venv`; зависимости проекта не менялись.

## Открытые вопросы

- `Q-KIT-01` остаётся открытым: фактическое влияние на контекст зависит от host/runtime и способа загрузки `AGENTS.md`.
- Решение `KIT-0001` остаётся в `review`; статус `approved` ставит владелец.
