---
id: domain.narrative.readme
title: "Домен narrative — литература: мир, хронология, текст"
type: meta
status: approved
authority: invariant
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Домен `narrative`

Отвечает за факты мира, хронологию, стиль и текст. Не отвечает за код.

Домен держит четыре вещи, без которых литературный корпус не проверяется: шкалу нормативности `core / setting / detail / presentation`, маркеры провенанса, двухосевую систему доступа «роль × призма» и шкалу компетенции. Двухосевость нужна потому, что в литературе читатель видит **не часть мира, а версию мира**, зависящую от того, кто смотрит.

## Что здесь лежит

| Файл | Содержание |
| --- | --- |
| [`manifest.yaml`](manifest.yaml) | Каталоги домена, профили, проверки |
| [`policy.md`](policy.md) | Правила `NR-POL-01..14` |
| [`text.md`](text.md) | Правила чистки текста `NR-TXT-01..14`: вода, голос, вайб, бюджет |
| [`levels.md`](levels.md) | Шкала компетенции `УН–У14`: что означает каждый уровень |
| [`schema/competence.yaml`](schema/competence.yaml) | Каталог доменов знания и формулировки «знает до …» |
| [`authority.md`](authority.md) | Уровни `core / setting / detail / presentation` |
| [`schema/authority.yaml`](schema/authority.yaml) | Машинный словарь уровней и статусов |
| [`access.md`](access.md) | Роли, призмы, компетенции, карта понимания |
| [`schema/access.yaml`](schema/access.yaml) | Машинное описание доступа: роли × призмы, пороги, пресеты выгрузки |
| [`agents.md`](agents.md) | Фрагмент `AGENTS.md` для этого домена |
| [`registry/`](registry/README.md) | Что читать первым при работе с корпусом |
| [`workflows/`](workflows/README.md) | `lore-change`, `prose-cleanup`, `entity-card`, `export-book`, `image`, `species` |
| [`templates/`](templates/README.md) | Карточка сущности |
| [`profiles/`](profiles/) | `lore`, `history`, `prose`, `analysis` |

## Профили домена

| Профиль | Тема | Мыслительный процесс |
| --- | --- | --- |
| [`lore`](profiles/lore/README.md) | факты мира, сущности, устройство | расширение без противоречий |
| [`history`](profiles/history/README.md) | хронология и инварианты | поиск конфликтов во времени |
| [`prose`](profiles/prose/README.md) | текст и стиль | ритм и голос, факты не меняются |
| [`analysis`](profiles/analysis/README.md) | противоречия и пробелы корпуса | аудит по просьбе пользователя |
