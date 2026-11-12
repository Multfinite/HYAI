---
id: meta.decisions.readme
title: "Решения: индекс по областям"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.4"
updated: "2026-11-10"
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
| `picture` | [`picture/`](picture/README.md) | `PIC` | промпт-генерация, конвейер звеньев, приёмка и стиль |
| `video` | [`video/`](video/README.md) | `VID` | временная связность, сегменты, sound plan, швы и монтаж |
| `cartography` | [`cartography/`](cartography/README.md) | `CART` | планетарные атласы и векторная картография |

## Действующие решения

| ID | Область | Название | Статус |
| --- | --- | --- | --- |
| [`P-0001`](project/P-0001-shared-agent-bootstrap.md) | project | Единые требования общего входа агента | approved |
| [`P-0002`](project/P-0002-process-step-narration.md) | project | Единое озвучивание шагов работы во всех доменах | approved |
| [`KIT-0001`](kit/KIT-0001-agent-entrypoint-structure.md) | kit | Структура общего входа агента | approved |
| [`KIT-0002`](kit/KIT-0002-core-process-narration.md) | kit | Общее правило озвучивания этапов в ядре | approved |
| [`KIT-0003`](kit/KIT-0003-picture-domain.md) | kit | Самодостаточный домен `picture` | approved |
| [`KIT-0004`](kit/KIT-0004-video-domain.md) | kit | Самостоятельный домен `video` для temporal continuity, звука и монтажа | approved |
| [`KIT-0005`](kit/KIT-0005-parallel-execution.md) | kit | Общее правило параллельного выполнения и очереди удалённых задач | approved |
| [`P-0003`](project/P-0003-picture-video-keyframe-handoff.md) | project | Разделение владения keyframe-изображениями между picture и video | approved |
| [`P-0004`](project/P-0004-resource-bootstrap.md) | project | Общий вход: провайдер генерации, стоимость и правила расхода | approved |
| [`P-0005`](project/P-0005-cartography-world-canon.md) | project | Владение структурированным планетарным и пространственным каноном | approved |
| [`P-0006`](project/P-0006-style-asked-not-assumed.md) | project | Стиль базы и стиль-фильтр выбирает пользователь, а не агент | approved |
| [`KIT-0006`](kit/KIT-0006-cartography-domain.md) | kit | Самостоятельный домен cartography для планетарного атласа и векторных карт | approved |
| [`PIC-0001`](picture/PIC-0001-handoff-page.md) | picture | Форма переноса промптов и изображений в другой чат — страница по шаблону | review |
| [`PIC-0002`](picture/PIC-0002-body-refs-and-manual-photoreal.md) | picture | Эталоны частей тела не удаляются; фотореалистичный финал делает владелец | review |
| [`PIC-0003`](picture/PIC-0003-concept-method-gate.md) | picture | Способ генерации концепт-арта задаёт пользователь до первой генерации | review |
| [`PIC-0004`](picture/PIC-0004-handoff-final-integrity.md) | picture | Handoff переносит только принятые финалы; замена финального ассета — четырёхшаговый протокол | review |

## Правила

1. Решение, касающееся двух доменов, живёт в `project/` (`HYAI-DEC-02`).
2. Файл без строки в этом индексе и строка без файла — ошибки (`HYAI-DEC-13`).
3. Уточнение вливается в исходное решение; номер-«вход» получает `status: merged` (`HYAI-DEC-09`).

| [PIC-0005](picture/PIC-0005-crop-edit-paste-integrate.md) | picture | Обязательный CEPI и границы сохранности после интеграции | review |

| [PIC-0006](picture/PIC-0006-ear-remediation.md) | picture | Ушная специализация CEPI и доказательства ear/1 | review |

| [KIT-0007](kit/KIT-0007-ear-evidence-extension.md) | kit | Совместимое дополнение ушных доказательств ear/1 | review |
