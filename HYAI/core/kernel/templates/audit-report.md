---
id: template.audit-report
title: "Шаблон отчёта аудита"
type: template
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-10-22"
template: true
template_kind: output
---

# Шаблон отчёта аудита

Скопировать в `HYAI/meta/reports/<domain>/YYYY-MM-DD-<slug>.md`, `report_kind: audit`.

````markdown
---
id: report.<domain>.YYYY-MM-DD-audit-slug
title: "Аудит: <область>"
type: report
report_kind: audit
domain: <domain>
profile: <domain>/analysis
status: review
authority: none
visibility: internal
date: "YYYY-MM-DD"
workflow: audit
decisions: []
---

# Аудит: <область>

## Рамка и источники

Что проверялось, по каким правилам (ID), что заведомо вне охвата и почему.

## Находки

| # | Место | Наблюдение | Правило | Приоритет |
| --- | --- | --- | --- | --- |
| 1 | `путь:строка` | что не так | `SW-POL-04` / `HYAI-PROV-05` | P1 |

Подтверждение: `P0`/`P1` — воспроизведение или цитата нормы; остальное — `[Г]`.

## Предложения

| Предложение | Цена | Риск | Что проверяет результат |
| --- | --- | --- | --- |

## Открытые вопросы

- `Q-*` — что мешает закрыть находку.
````
