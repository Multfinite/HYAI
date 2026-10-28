---
id: domain.picture.templates.readme
title: "Домен picture: шаблоны документов"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-28"
---

# Шаблоны домена `picture`

Во всех шаблонах **`<picture_root>`** подставляется из `root_paths` манифеста активного домена `picture`: в самом репозитории HYAI это `HYAI/core/domains/picture/pictures`, а во внешнем проекте с HYAI в роли подмодуля — собственный путь проекта вне подмодуля (например, `meta/hyai/domains/picture/pictures`, `PIC-POL-06`).

| Файл | `template_kind` | Куда попадает результат |
| --- | --- | --- |
| [`task-safety-brief.md`](task-safety-brief.md) | `request` | Запрос пользователю на воротах `G0-SAF` и запись брифа в `<picture_root>/briefs/<slug>.md` |
| [`prompt-spec.md`](prompt-spec.md) | `output` | `<picture_root>/prompts/<slug>-<pass>.md` — спецификация промпта по каркасу «5+3» и журнал итераций |
| [`pipeline-manifest.md`](pipeline-manifest.md) | `output` | `<picture_root>/stages/<slug>/pipeline-manifest.md` — карта принятых промежуточных звеньев `S1..S8` |
| [`series-anchor.md`](series-anchor.md) | `output` | `<picture_root>/briefs/<series>-anchor.md` — эталон консистентности серии и единого фильтра стиля |
| [`asset-card.md`](asset-card.md) | `output` | `<picture_root>/assets/<slug>.md` — паспорт готового изображения, провенанс и протокол VLM-приёмки |

## Правило заполнения шаблонов

В каждом шаблоне соблюдаются `HYAI-ART-06..08`: нет данных — останавливаемся и спрашиваем пользователя (особенно по четырём правилам безопасности `PIC-SAF-01`), а не подставляем выдуманные значения.
