---
id: domain.docs.templates.readme
title: "Домен docs: шаблоны документов"
type: meta
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# Шаблоны домена `docs`

| Файл | `template_kind` | Куда попадает результат |
| --- | --- | --- |
| [`tz.md`](tz.md) | `output` | `specs/<система>/tz.md` — техническое задание |
| [`tech-spec.md`](tech-spec.md) | `output` | `specs/<система>/<подсистема>.md` — техническая спецификация |
| [`guide.md`](guide.md) | `output` | `docs/<тема>.md` — руководство или README |
| [`diagram.md`](diagram.md) | `output` | `diagrams/<тема>.md` — текстовая схема с подписью |
| [`spec-questions.md`](spec-questions.md) | `request` | вопросы заказчику до написания ТЗ |

## Границы с другими доменами

- Контракт модуля (вход/выход функции) — шаблон `HYAI/core/domains/software/templates/spec.md`.
- Требование к системе (зачем, при каких условиях, критерий приёмки) — этот домен.
- Решение о выборе варианта — `HYAI/core/kernel/templates/decision.md`, а не ТЗ.
