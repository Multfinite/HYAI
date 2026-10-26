---
id: report.kit.2026-10-26-bootstrap-pointer-consolidation
title: "Сокращение входа и интеграция v1.0.1"
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
  - path: "HYAI/core/domains/kit/agents.md"
    why: "Сохранены новые требования v1.0.1 в компактной сводке по одобренному владельцем разрешению конфликта"
    profile: "project/maintainer"
  - path: "HYAI/core/domains/software/agents.md"
    why: "Компактная сводка объединена с новыми требованиями v1.0.1"
    profile: "software/code"
  - path: "HYAI/core/domains/narrative/agents.md"
    why: "Компактная сводка объединена с новыми требованиями v1.0.1"
    profile: "narrative/prose"
  - path: "AGENTS.md"
    why: "Пересобран генерируемый общий entrypoint из обновлённых источников"
    profile: "project/maintainer"
---

# Сокращение входа и интеграция v1.0.1

## Задача

Сократить повторение правил выбора пары и оформления результата в общем входе, а затем разрешить конфликты PR с `master` v1.0.1, сохранив его новые требования и переносимые пути. Защищённые изменения показаны владельцу и одобрены до применения.

## Что сделано

- `HYAI/core/kernel/agents.md`, §1 и §7 — краткие указатели на канонические routing- и task-источники; сохранены выбор пользователя, объявление пары, отчёт, решение при изменении нормы и полный конвейер.
- `HYAI/core/kernel/agents.md` взят на основе v1.0.1, включая `{{HYAI}}` для переносимых путей; остальные разделы v1.0.1 сохранены.
- `HYAI/core/domains/kit/agents.md` — компактная сводка объединяет согласованный draft с новыми требованиями v1.0.1 о шаблонах, доступе, профилях и решении формата.
- `HYAI/core/domains/software/agents.md` и `HYAI/core/domains/narrative/agents.md` — сохранены короткие сводки, дополненные существенными правилами v1.0.1.
- `AGENTS.md` — пересобран генератором; вручную не редактировался.

Нормативные политики, safety-сводка и workflow не менялись. Размеры не сравнивались с несопоставимой версией v1.0.1; число токенов и поведение host/runtime не измерялись.

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
