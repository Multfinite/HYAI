---
id: kernel.templates.readme
title: "HYAI/core/kernel/templates/ — шаблоны результата и шаблоны запроса"
type: meta
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Шаблоны ядра

Шаблон — любая форма, которую можно переиспользовать: не только результат, но и **запрос** (`HYAI-ART-06`). Шаблон запроса экономит больше, чем шаблон отчёта: потеря контекста происходит на входе.

| Файл | `template_kind` | Назначение |
| --- | --- | --- |
| [`report.md`](report.md) | `output` | Отчёт задачи |
| [`audit-report.md`](audit-report.md) | `output` | Отчёт аудита |
| [`decision.md`](decision.md) | `output` | Решение `HYAI/meta/decisions/<scope>/` |
| [`task-brief.md`](task-brief.md) | `request` | Бриф: что спросить у пользователя до работы |

Шаблон отчёта разбора — общий для всех доменов и живёт в [`../../shared/templates/analysis-report.md`](../../shared/templates/analysis-report.md).

## Правила

1. Каждый шаблон несёт `template: true` и `template_kind` (`HYAI-ART-06`).
2. Плейсхолдеры `<...>` и `{{...}}` не проверяются линкером (`HYAI-ART-08`).
3. Шаблон обязан содержать строку «если данных нет»: остановиться и задать вопрос, а не подставлять правдоподобное (`HYAI-ART-07`).
4. Доменные шаблоны лежат в `HYAI/core/domains/<domain>/templates/`, профильные — в `.../profiles/<profile>/templates/`.
