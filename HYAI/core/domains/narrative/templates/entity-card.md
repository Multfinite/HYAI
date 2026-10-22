---
id: template.narrative.entity-card
title: "Шаблон карточки сущности мира"
type: template
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-10-22"
template: true
template_kind: output
---

# Карточка сущности

Один документ — одна сущность (`NR-POL-13`).

**Если данных нет:** `[?] Q-*` и вопрос; не заполнять «примерно так».

````markdown
---
id: entity.<раздел>.<slug>
title: "<Имя>"
type: entity
status: draft
authority: setting
visibility: internal
knowledge: common
---

# <Имя>

## Кратко

Одно-два предложения, зачем существует эта сущность в мире.

## Факты

| Факт | Маркер | Источник |
| --- | --- | --- |
| | `[А]` / `[И]` / `[В]` / `[Г]` | `<файл или решение>` |

## Связи

| С кем/чем | Тип связи | Направление |
| --- | --- | --- |

## Пределы

Что эта сущность не может (жёсткие ограничения уровня `core`/`setting`).

## Секреты

| Секрет | `visibility` | `knowledge` | `known_by` |
| --- | --- | --- | --- |

## Требования к пониманию

```yaml
requires:
  - domain: <область>
    min: <0..14>
```

## Открытые вопросы

- `Q-*`
````
