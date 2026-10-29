---
id: report.kit.2026-10-29-parallel-execution-rule
title: "Глобальное правило параллельного исполнения"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-10-29"
workflow: task
decisions: ["KIT-0005"]
cross_scope:
  - path: "HYAI/core/kernel/policies/interaction.md"
    why: "Добавлена глобальная норма проверки process-capability, лимита параллельности и диспетчеризации удалённых задач."
    profile: "kit/domain-builder"
  - path: "HYAI/core/kernel/agents.md"
    why: "Проверка применимости перенесена в самый ранний bootstrap до выбора домена и профиля."
    profile: "kit/domain-builder"
  - path: "HYAI/core/kernel/workflows/parallel-execution.md"
    why: "Добавлен универсальный порядок работы с независимыми и удалёнными задачами."
    profile: "kit/domain-builder"
  - path: "HYAI/core/kernel/workflows/README.md"
    why: "Новый workflow зарегистрирован в каталоге процессов ядра."
    profile: "kit/domain-builder"
  - path: "HYAI/core/kernel/README.md"
    why: "Обновлён перечень общего ядра и диапазон INT."
    profile: "kit/domain-builder"
  - path: "HYAI/core/kernel/policies/README.md"
    why: "Уточнена навигация по глобальной политике взаимодействия."
    profile: "kit/domain-builder"
  - path: "HYAI/core/kernel/spec/rule-ids.md"
    why: "Документация диапазона ID и класса INT синхронизирована с новым правилом."
    profile: "kit/domain-builder"
  - path: "HYAI/meta/decisions/README.md"
    why: "KIT-0005 добавлен в общий индекс решений."
    profile: "kit/domain-builder"
  - path: "HYAI/meta/reports/README.md"
    why: "Task report добавлен в общий индекс отчётов."
    profile: "kit/domain-builder"
  - path: "AGENTS.md"
    why: "Пересобран общий entrypoint по изменённым kernel sources; вручную не редактировался."
    profile: "kit/domain-builder"
---

# Глобальное правило параллельного исполнения

## Задача

Ввести для всех доменов HYAI обязательную проверку возможностей agent runtime сразу при входе и правило эффективного параллельного выполнения независимых задач с ограничением по максимуму одновременных процессов. Для удалённых MCP/API/model вызовов требуется очередь и уведомление о завершении, чтобы агент обрабатывал готовые ответы без ожидания несвязанных заданий.

## Что сделано

- Добавлено `HYAI-INT-30` в `HYAI/core/kernel/policies/interaction.md`: проверка среды происходит до выбора домена/профиля; независимые задачи запускаются параллельно только при отсутствии зависимостей, конфликтующих записей и запрета доступа; до первого параллельного запуска нужен явный максимум одновременных задач.
- Для удалённых MCP, API-сервисов и API-моделей задана очередь с исполняющим диспетчером, состояниями задач и обратной связью о завершении. Callback — предпочтительный простой способ; допускаются события, MCP-уведомления и неблокирующее получение статуса. Готовые независимые результаты обрабатываются сразу.
- Создан `HYAI/core/kernel/workflows/parallel-execution.md` с графом зависимостей, лимитами, безопасным fallback и приоритетом простого развёртываемого решения.
- Общий вход расширен; `AGENTS.md` пересобран. Добавлено решение `KIT-0005` и обновлены индексы.
- Конкретная runtime, provider, callback-сервис или библиотека не предписаны; зависимость проекта не добавлялась.
- В этой сессии пользователь делегировал выбор concurrency cap; до параллельных операций выбран и сообщён предел 4 задачи. Это ограничение только текущей сессии, не глобальное значение по умолчанию.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Сборка entrypoint | `assemble_agents.py --write`, затем `--check` | Успешно; `AGENTS.md` актуален, 153 строки |
| Общий конвейер | `run_checks.py --skip-project` | 24 проверки, 0 падений; включая `check_rules.py` |
| Project unit tests | `python -m unittest discover -s HYAI/tools/tests` во временном PyYAML venv | 72 теста, успешно |
| Отчёты | `check_report.py` | 11 отчётов, 0 проблем |
| Индексы и решения | `check_indexes.py`, `check_decisions.py` | 0 проблем; 0 ошибок и 0 предупреждений |
| Ссылки | `check_links.py` | 0 битых из 514 проверенных |
| Whitespace | `git diff --check` | Успешно, ошибок нет |

PyYAML установлен только в `/tmp/hyai-validate`; зависимости проекта не менялись.

## Открытые вопросы

- Для конкретной agent runtime способ постановки в очередь выбирается во время задачи; HYAI не навязывает библиотеку, сервис или callback-протокол.
- Если очередь/уведомления недоступны или параллельное исполнение запрещено, агент сообщает ограничение и переходит к безопасному последовательному способу, не выдавая его за параллельный.
