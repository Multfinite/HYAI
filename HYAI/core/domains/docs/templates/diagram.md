---
id: template.docs.diagram
title: "Шаблон текстовой диаграммы"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-22"
template: true
template_kind: output
---

# Диаграмма

Скопировать в `diagrams/<тема>.md`. Схема отвечает на один вопрос (`DOC-POL-11`), хранится текстом (`DOC-POL-10`).

**Если данных нет:** строить по коду, а не по памяти; расхождение — `Q-*`.

````markdown
---
id: diagram.<тема>
title: "<Вопрос, на который отвечает схема>"
type: diagram
status: draft
authority: illustrative
visibility: internal
---

# <Вопрос, на который отвечает схема>

**Отвечает на вопрос:** <один вопрос>.
**Источник:** `<файл или документ>`.

```mermaid
flowchart LR
  A[Клиент] -->|HTTP| B[Сервис]
  B -->|SQL| C[(База)]
```

## Обозначения

| Элемент | Что значит |
| --- | --- |

## Что не показано

Сознательно убранное, чтобы схема осталась читаемой.
````
