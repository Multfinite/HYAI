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
  - path: "HYAI/core/domains/docs/agents.md"
    why: "Сокращение доменной сводки; полные правила остаются в политике docs"
    profile: "project/maintainer"
  - path: "HYAI/core/domains/software/agents.md"
    why: "Сокращение доменной сводки; полные правила остаются в политике software"
    profile: "project/maintainer"
  - path: "HYAI/core/domains/narrative/agents.md"
    why: "Сокращение доменной сводки; полные правила остаются в политике narrative"
    profile: "project/maintainer"
  - path: "HYAI/meta/decisions/project/P-0001-shared-agent-bootstrap.md"
    why: "Фиксация требований общего входа для всех активных доменов"
    profile: "project/maintainer"
  - path: "HYAI/tools/check_rules.py"
    why: "Устранение ложного срабатывания: ID вопроса Q-KIT-01 ошибочно распознавался как legacy-номер правила"
    profile: "project/maintainer"
  - path: "HYAI/tools/tests/test_rules.py"
    why: "Регрессионный тест для различения идентификаторов вопросов и правил"
    profile: "project/maintainer"
  - path: "src/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "tests/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "docs/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "specs/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "diagrams/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "world/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "chapters/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "drafts/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
  - path: "styles/.gitkeep"
    why: "Восстановление пустого корня, объявленного root_paths; продуктовые данные не добавлялись"
    profile: "project/maintainer"
---

# Перегруппировка общего входа агента

## Задача

Сделать общий вход агента короче и яснее за счёт группировки по этапам работы и сокращения повторов. Численная цель по токенам не ставилась; обязательные правила и их смысл должны сохраниться.

## Что сделано

- `HYAI/core/kernel/agents.md` — сгруппированы домен/профиль, источники, ограничения, общение, провенанс, ворота и результат; сокращены повторы с сохранением обязательных деталей.
- `HYAI/core/domains/docs/agents.md`, `HYAI/core/domains/software/agents.md`, `HYAI/core/domains/narrative/agents.md` — оставлены краткое назначение, ключевые отличия и ссылки на полные политики/профили/workflow.
- `HYAI/core/domains/kit/agents.md` — сокращён по одобренному владельцем draft; сохранены границы, ключевые условия и ссылка на политику/workflow.
- `AGENTS.md` — пересобран из обновлённых источников, активной конфигурации и доменных фрагментов.
- `HYAI/meta/decisions/kit/KIT-0001-agent-entrypoint-structure.md` — уточнено решение о структуре общего входа (`status: review`).
- `HYAI/meta/decisions/project/P-0001-shared-agent-bootstrap.md` — зафиксированы общие требования для активных доменов (`status: review`).
- `HYAI/tools/check_rules.py` — исправлено ложное распознавание `Q-KIT-01` как legacy-ID правила; добавлен регрессионный тест.
- В девяти объявленных `root_paths` добавлены пустые `.gitkeep`-заполнители. Продуктовое содержимое не добавлялось; каталоги отсутствовали и в исходном commit, из-за чего `check_indexes.py` падал независимо от изменений.
- Обновлены индексы решений и отчётов.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Формат патча | `git diff --check` | Успешно (`rc=0`) |
| Сборка entrypoint | `/tmp/hyai-token-check-venv/bin/python HYAI/tools/assemble_agents.py --check` | Успешно; `AGENTS.md` актуален (125 строк). |
| Конвейер | `/tmp/hyai-token-check-venv/bin/python HYAI/tools/run_checks.py --skip-project` | Успешно после восстановления объявленных product-root каталогов: 19 проверок, упало 0. |
| Набор тестов | `/tmp/hyai-token-check-venv/bin/python -m unittest discover -s HYAI/tools/tests` | 68 тестов, успешно. |
| Окружение | PyYAML 6.0.3 во временном `/tmp/hyai-token-check-venv` | Только для диагностики; зависимости проекта не менялись. |

## Открытые вопросы

- `Q-KIT-01` — поведение host/runtime при загрузке `AGENTS.md` не установлено; поэтому эффект на фактические токены не измерялся.
- Решения оставлены в `review`; `approved` ставит владелец.
