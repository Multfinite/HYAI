---
id: meta.lint.readme
title: "HYAI/meta/lint/ — данные проверок"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-11-01"
---

# `HYAI/meta/lint/`

Правила проверок — данные, а не код. Новое правило добавляется строкой JSON, а не правкой Python.

| Файл | Чем читается | Что задаёт |
| --- | --- | --- |
| [`links.json`](links.json) | `check_links.py` | Исключения, расширения, шаблоны плейсхолдеров |
| [`whitespace.json`](whitespace.json) | `whitespace.py` | Проверяемые расширения, разрешённые хвостовые пробелы |
| [`terms/kernel.json`](terms/kernel.json) | `lint_terms.py` | Лесть, выпрашивание одобрения, отказ без ссылки на правило (`HELPER`, `HYAI-PERM-N10`) |
| [`terms/software.json`](terms/software.json) | `lint_terms.py` | Термины и паттерны кода |
| [`terms/docs.json`](terms/docs.json) | `lint_terms.py` | Вода в документах, TODO без владельца, схема картинкой |
| [`terms/narrative.json`](terms/narrative.json) | `lint_terms.py` | Термины и паттерны текста |
| [`terms/picture.json`](terms/picture.json) | `lint_terms.py` | Плейсхолдеры безопасности, пустой `negative`, штампы качества, смешение весов, хранение брака, ранняя стилизация |
| [`terms/cartography.json`](terms/cartography.json) | `lint_terms.py` | Растровые map exports, незаполненные body/CRS и не-Köppen climate scheme |

## Обязательные поля правила

| Поле | Зачем |
| --- | --- |
| `id` | Ссылка из политики и отчёта |
| `severity` | `error` (rc=1) или `warn` |
| `applies_to` | Глобы путей: без него правило ударит по чужому домену |
| `reason` | Ссылка на правило политики или решение |

Исключение без `reason` — ошибка конфигурации (`rc=2`): исключения обязаны объясняться, иначе они копятся.
