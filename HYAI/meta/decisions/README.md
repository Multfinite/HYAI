---
id: meta.decisions.readme
title: "Решения: индекс по областям"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Решения

Одно решение — одна действующая норма. Нумерация независима внутри области: `SW-0007` и `NR-0007` — разные решения (`HYAI-DEC-05`).

| Область | Каталог | Префикс | Что сюда попадает |
| --- | --- | --- | --- |
| проект | [`project/`](project/README.md) | `P` | то, что касается всех доменов |
| каркас | [`kit/`](kit/README.md) | `KIT` | формат доменов, профилей, проверок |
| `software` | [`software/`](software/README.md) | `SW` | архитектура, контракты, зависимости |
| `docs` | [`docs/`](docs/README.md) | `DOC` | типы документов, требования, формы ТЗ |
| `narrative` | [`narrative/`](narrative/README.md) | `NR` | канон, хронология, доступ |

## Действующие решения

| ID | Область | Название | Статус |
| --- | --- | --- | --- |
| [`P-0001`](project/P-0001-shared-agent-bootstrap.md) | project | Единые требования общего входа агента | review |
| [`KIT-0001`](kit/KIT-0001-agent-entrypoint-structure.md) | kit | Структура общего входа агента | review |

## Правила

1. Решение, касающееся двух доменов, живёт в `project/` (`HYAI-DEC-02`).
2. Файл без строки в этом индексе и строка без файла — ошибки (`HYAI-DEC-13`).
3. Уточнение вливается в исходное решение; номер-«вход» получает `status: merged` (`HYAI-DEC-09`).
