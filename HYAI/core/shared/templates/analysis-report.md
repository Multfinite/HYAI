---
id: shared.template.analysis-report
title: "Шаблон отчёта разбора (общий для доменов)"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-22"
template: true
template_kind: output
---

# Шаблон отчёта разбора

Скопировать в `HYAI/meta/reports/<domain>/YYYY-MM-DD-<slug>.md`, `report_kind: analysis`.
Разбор не меняет репозиторий (`HYAI-INT-09`).

**Если данных нет:** не заполнять правдоподобным — `[?] Q-*` и вопрос.

````markdown
---
id: report.<domain>.YYYY-MM-DD-analysis-slug
title: "Разбор: <вопрос>"
type: report
report_kind: analysis
domain: <domain>
profile: <domain>/analysis
status: review
authority: none
visibility: internal
date: "YYYY-MM-DD"
workflow: audit
decisions: []
---

# Разбор: <вопрос>

## Вопрос

Один вопрос, на который нужен ответ. Больше одного — это несколько разборов.

## Разбор

Факты с маркерами `[И]`/`[В]`, гипотезы с `[Г]` и условием проверки. Что прочитано, что нет.

## Варианты

| Вариант | Плюсы | Минусы | Цена | Что ломает |
| --- | --- | --- | --- | --- |

## Рекомендация

Какой вариант и почему; что должно быть верно, чтобы рекомендация осталась верной.

## Открытые вопросы

- `Q-*` — что нужно узнать, чтобы решение стало окончательным.
````
