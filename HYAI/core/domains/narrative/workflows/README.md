---
id: domain.narrative.workflows.readme
title: "Домен narrative: процессы"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Процессы домена `narrative`

Каркас стадий и ворот — ядерный ([`../../../kernel/workflows/README.md`](../../../kernel/workflows/README.md)).

| Процесс | Когда | Результат |
| --- | --- | --- |
| [`lore-change.md`](lore-change.md) | новый или изменённый факт мира | карточка/правка + проверка противоречий |
| [`prose-cleanup.md`](prose-cleanup.md) | текст оброс водой или потерял голос | правка текста без изменения фактов |
| [`entity-card.md`](entity-card.md) | новая сущность: персонаж, страна, фракция, локация, событие | карточка по шаблону + проверка `NR-ENT-01..04` |
| [`species.md`](species.md) | вид, подвид или наследуемая линия | карточка с ценой, пределами и наследованием |
| [`export-book.md`](export-book.md) | нужна читательская, игровая или мастерская сборка | выгрузка по пресету + отчёт + ворота `HYAI-ART-22` |
| [`image.md`](image.md) | иллюстрация, обложка, промпт | промпт, проверка деталей, файл вне git |

Аудит корпуса (`NR`-противоречия) идёт ядерным процессом `audit` с профилем `narrative/analysis`.
