---
id: domain.docs.workflows.readme
title: "Домен docs: процессы"
type: meta
status: approved
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# Процессы домена `docs`

| Процесс | Когда | Результат |
| --- | --- | --- |
| [`spec.md`](spec.md) | нужно ТЗ или техническая спецификация | набор проверяемых требований |
| [`documentation.md`](documentation.md) | нужна документация, руководство, README, комментарии | текст, который решает вопрос читателя |
| [`diagrams.md`](diagrams.md) | нужна схема: UML, C4, поток данных, состояния | текстовая диаграмма + подпись и контекст |

## UML 2.5: 14 точечных процессов

Каждый процесс имеет триггер `when_to_use` и собирается навыком `hyai-docs-uml-*`. Общий вход —
[`../uml.md`](../uml.md), правила — `DOC-POL-16..34` в [`../policy.md`](../policy.md).
Общая активация — авторский навык `uml`.

| Процесс | Тип диаграммы | Правило |
| --- | --- | --- |
| [`uml-class.md`](uml-class.md) | классов | `DOC-POL-21` |
| [`uml-component.md`](uml-component.md) | компонентов | `DOC-POL-22` |
| [`uml-deployment.md`](uml-deployment.md) | развёртывания | `DOC-POL-23` |
| [`uml-object.md`](uml-object.md) | объектов | `DOC-POL-24` |
| [`uml-package.md`](uml-package.md) | пакетов | `DOC-POL-25` |
| [`uml-profile.md`](uml-profile.md) | профилей | `DOC-POL-26` |
| [`uml-composite-structure.md`](uml-composite-structure.md) | композитной структуры | `DOC-POL-27` |
| [`uml-activity.md`](uml-activity.md) | активности | `DOC-POL-28` |
| [`uml-use-case.md`](uml-use-case.md) | вариантов использования | `DOC-POL-29` |
| [`uml-state-machine.md`](uml-state-machine.md) | состояний | `DOC-POL-30` |
| [`uml-sequence.md`](uml-sequence.md) | последовательности | `DOC-POL-31` |
| [`uml-communication.md`](uml-communication.md) | коммуникации | `DOC-POL-32` |
| [`uml-timing.md`](uml-timing.md) | тайминга | `DOC-POL-33` |
| [`uml-interaction-overview.md`](uml-interaction-overview.md) | обзора взаимодействий | `DOC-POL-34` |

Каркас стадий и ворот — ядерный ([`../../../kernel/workflows/README.md`](../../../kernel/workflows/README.md)).
