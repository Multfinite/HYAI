---
id: report.kit.2026-10-28-process-step-narration
title: "Общее озвучивание этапов работы"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-10-28"
workflow: task
decisions: ["KIT-0002", "P-0002"]
cross_scope:
  - path: "HYAI/core/kernel/policies/interaction.md"
    why: "Добавлено общее правило озвучивания шагов по одобренному владельцем draft"
    profile: "project/maintainer"
  - path: "HYAI/core/kernel/agents.md"
    why: "Добавлен единый bootstrap-указатель на правило ядра"
    profile: "project/maintainer"
  - path: "HYAI/meta/decisions/project/P-0002-process-step-narration.md"
    why: "Фиксация поведения, одинакового для всех активных доменов"
    profile: "project/maintainer"
  - path: "AGENTS.md"
    why: "Пересобранный entrypoint содержит ссылку на глобальное правило"
    profile: "project/maintainer"
---

# Общее озвучивание этапов работы

## Задача

Сделать ход работы более словесным: до начала каждого применимого шага из политики, workflow или шаблона агент объясняет источник, действие и ожидаемый результат; смену домена или профиля объявляет заранее. Правило должно жить в ядре и действовать одинаково для всех доменов и профилей.

## Что сделано

- `HYAI/core/kernel/policies/interaction.md` — добавлено `HYAI-INT-29`: озвучивать источник и действие до каждого применимого шага, сообщать результат и переход, объявлять смену домена/профиля с причиной и областью. Уточнено, что это не заменяет ворота одобрения и не требует комментария на каждый вызов инструмента.
- `HYAI/core/kernel/agents.md` — добавлен краткий указатель на правило ядра.
- `HYAI/meta/decisions/kit/KIT-0002-core-process-narration.md` и `HYAI/meta/decisions/project/P-0002-process-step-narration.md` — зафиксированы размещение правила в ядре и его междоменная применимость; статусы `review`.
- `AGENTS.md` — пересобран из исходников.
- Доменные и профильные файлы не изменялись.

Изменение показано владельцу и одобрено до правки. Число токенов и фактическое поведение host/runtime не измерялись.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Сборка инструкций | `/tmp/hyai-token-check-venv/bin/python HYAI/tools/assemble_agents.py --check` | Успешно; `AGENTS.md` актуален (132 строки). |
| Конвейер | `/tmp/hyai-token-check-venv/bin/python HYAI/tools/run_checks.py --skip-project` | Успешно: 19 проверок, упало 0. |
| Тесты | `/tmp/hyai-token-check-venv/bin/python -m unittest discover -s HYAI/tools/tests` | Успешно: 68 тестов. |
| Отчёты и ссылки | `check_report.py`, `check_links.py` | 5 отчётов без проблем; 0 битых ссылок из 368 проверенных. |
| Патч | `git diff --check` | Успешно. |

PyYAML используется только во временном окружении `/tmp/hyai-token-check-venv`; зависимости проекта не менялись.

## Открытые вопросы

- Проверки текстового соответствия не гарантируют, что конкретный host будет показывать все промежуточные сообщения.
- Статусы решений остаются `review`; `approved` ставит владелец.
