---
id: domain.software.readme
title: "Домен software — разработка программного обеспечения"
type: meta
status: approved
authority: invariant
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Домен `software`

Отвечает за код, тесты, контракты, схемы данных и архитектуру ПО. Не отвечает за художественный текст и факты мира — это домен `narrative`.

## Что здесь лежит

| Файл | Содержание |
| --- | --- |
| [`manifest.yaml`](manifest.yaml) | Каталоги домена, профили, проверки |
| [`policy.md`](policy.md) | Правила `SW-POL-01..12` |
| [`authority.md`](authority.md) | Что значит «норма» в коде: `invariant / contract / implementation / convention` |
| [`schema/authority.yaml`](schema/authority.yaml) | Машинный словарь уровней и статусов |
| [`access.md`](access.md) | Контуры доступа к коду и документации |
| [`schema/`](schema/README.md) | Машинные словари уровня и доступа |
| [`schema/access.yaml`](schema/access.yaml) | Машинные контуры и правила export |
| [`agents.md`](agents.md) | Фрагмент `AGENTS.md` для этого домена |
| [`registry/documents.yaml`](registry/documents.yaml) | Что читать первым при работе с кодом |
| [`workflows/`](workflows/README.md) | `feature`, `bugfix`, `refactor` |
| [`templates/`](templates/README.md) | Спека, модульная карточка, runbook |
| [`profiles/`](profiles/) | `code`, `architect`, `analysis` |

## Профили домена

| Профиль | Тема | Мыслительный процесс |
| --- | --- | --- |
| [`code`](profiles/code/README.md) | реализация | короткий цикл: контракт → тест → код |
| [`architect`](profiles/architect/README.md) | проектирование ПО | длинная цепочка: ограничения → варианты → решение |
| [`analysis`](profiles/analysis/README.md) | разбор задачи | исследование без правок, по просьбе пользователя |
