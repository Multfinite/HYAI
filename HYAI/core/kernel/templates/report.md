---
id: template.report
title: "Шаблон отчёта задачи"
type: template
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-10-22"
template: true
template_kind: output
---

# Шаблон отчёта задачи

Скопировать в `HYAI/meta/reports/<domain>/YYYY-MM-DD-<slug>.md`.

**Если данных нет:** не заполнять правдоподобным — поставить `[?] Q-*` и вынести в «Открытые вопросы».

````markdown
---
id: report.<domain>.YYYY-MM-DD-slug
title: "Короткое название работы"
type: report
report_kind: task
domain: <domain>
profile: <domain>/<profile>
status: review
authority: none
visibility: internal
date: "YYYY-MM-DD"
workflow: <domain>/<workflow>
decisions: []
---

# <Название>

## Задача

Что требовалось, для кого, чем измеряется готовность.

## Что сделано

- `<путь>` — что изменилось и зачем.

`cross_scope` — если правили вне своей зоны:
```yaml
cross_scope:
  - path: "<путь>"
    why: "<причина>"
    profile: <domain>/<profile-владелец>
```

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| конвейер | `python3 HYAI/tools/run_checks.py` | 0 падений |

## Открытые вопросы

- `Q-*` — что осталось неясным и что нужно, чтобы закрыть.
````
