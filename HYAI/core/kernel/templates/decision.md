---
id: template.decision
title: "Шаблон решения (ADR)"
type: template
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-10-22"
template: true
template_kind: output
---

# Шаблон решения

Скопировать в `HYAI/meta/decisions/<scope>/<PREFIX>-NNNN-<slug>.md`. Бюджет — `decisions.max_lines`.

Норма, а не журнал: только действующее правило и последствия (`HYAI-DEC-08`).

````markdown
---
id: decision.<scope>.<PREFIX>-NNNN
title: "<Что решено, одной строкой>"
type: decision
status: review
authority: contract
visibility: internal
scope: <project|kit|software|narrative>
affects_domains: []
affects: []
supersedes: null
---

# <PREFIX>-NNNN. <Название>

## Решение

Одно-два предложения: что теперь является нормой.

## Почему

3–5 строк контекста. Не хронология.

## Последствия

- Что становится проще.
- Что становится невозможным.
- Чем проверяется соблюдение (`python3 HYAI/tools/...` или `enforced: prose-only`).
````
