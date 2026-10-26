---
id: hyai.reports.readme
title: "HYAI/meta/reports/ — отчёты по областям"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
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
| [`plans/`](plans/README.md) | планы и матрицы, которые не являются отчётами о работе | — |
| [`archive/`](archive/README.md) | старое, сохранённое для истории | — |

Отчёты **общие внутри домена**: профиль работает на территории домена, поэтому `code`, `architect` и `analysis` пишут в один каталог `software/`. Разделение профилей видно в поле `profile`, а не в пути (`HYAI-ART-01`).

## Индекс

| Отчёт | Домен | Профиль | Вид |
| --- | --- | --- | --- |
| [`2026-10-26-agent-token-optimization.md`](kit/2026-10-26-agent-token-optimization.md) | `kit` | `kit/domain-builder` | `analysis` |
| [`2026-10-26-compact-agent-bootstrap.md`](kit/2026-10-26-compact-agent-bootstrap.md) | `kit` | `kit/domain-builder` | `task` |

Новый отчёт обязан появиться в этой таблице (`HYAI-ART-13`): `check_report.py` сверяет индекс с файловой системой.
