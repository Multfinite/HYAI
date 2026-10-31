---
id: hyai.reports.readme
title: "HYAI/meta/reports/ — отчёты по областям"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.1"
updated: "2026-11-01"
---

# Отчёты

Отчёт — единственный след работы, который читает следующая сессия. Чат не след: он не переживает контекст.

## Структура

| Каталог | Что | Область |
| --- | --- | --- |
| [`kit/`](kit/) | изменения каркаса: домены, профили, проверки | `kit` |
| [`software/`](software/) | работа с кодом | `software` |
| [`docs/`](docs/) | работа с документами и схемами | `docs` |
| [`narrative/`](narrative/) | работа с миром и текстом | `narrative` |
| [`picture/`](picture/) | генерация изображений, конвейеров звеньев и серий через промпт | `picture` |
| [`video/`](video/) | планирование, continuity, звук, швы, сегменты и монтаж | `video` |
| [`cartography/`](cartography/) | планетарные атласы, spatial layers и векторные карты | `cartography` |
| [`plans/`](plans/README.md) | планы и матрицы, которые не являются отчётами о работе | — |
| [`archive/`](archive/README.md) | старое, сохранённое для истории | — |

Отчёты **общие внутри домена**: профиль работает на территории домена, поэтому `code`, `architect` и `analysis` пишут в один каталог `software/`. Разделение профилей видно в поле `profile`, а не в пути (`HYAI-ART-01`).

## Индекс

| Отчёт | Домен | Профиль | Вид |
| --- | --- | --- | --- |
| [`2026-10-26-agent-token-optimization.md`](kit/2026-10-26-agent-token-optimization.md) | `kit` | `kit/domain-builder` | `analysis` |
| [`2026-10-26-compact-agent-bootstrap.md`](kit/2026-10-26-compact-agent-bootstrap.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-10-26-followup-agent-optimization.md`](kit/2026-10-26-followup-agent-optimization.md) | `kit` | `kit/domain-builder` | `analysis` |
| [`2026-10-26-bootstrap-pointer-consolidation.md`](kit/2026-10-26-bootstrap-pointer-consolidation.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-10-28-process-step-narration.md`](kit/2026-10-28-process-step-narration.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-10-28-picture-domain-analysis.md`](kit/2026-10-28-picture-domain-analysis.md) | `kit` | `kit/domain-builder` | `analysis` |
| [`2026-10-28-picture-domain-implementation.md`](kit/2026-10-28-picture-domain-implementation.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-10-28-picture-data-root-separation.md`](kit/2026-10-28-picture-data-root-separation.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-10-29-video-domain-analysis.md`](kit/2026-10-29-video-domain-analysis.md) | `kit` | `kit/domain-builder` | `analysis` |
| [`2026-10-29-video-domain-implementation.md`](kit/2026-10-29-video-domain-implementation.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-10-29-parallel-execution-rule.md`](kit/2026-10-29-parallel-execution-rule.md) | `kit` | `kit/domain-builder` | `task` |
| [`2026-11-01-cartography-domain-implementation.md`](kit/2026-11-01-cartography-domain-implementation.md) | `kit` | `kit/domain-builder` | `task` |

Новый отчёт обязан появиться в этой таблице (`HYAI-ART-13`): `check_report.py` сверяет индекс с файловой системой.
