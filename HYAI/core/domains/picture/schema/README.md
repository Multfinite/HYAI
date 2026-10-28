---
id: domain.picture.schema.readme
title: "Схемы домена picture"
type: meta
status: review
authority: invariant
visibility: internal
version: "1.0"
updated: "2026-10-28"
---

# Схемы домена `picture`

Строгая зона домена: профили не могут переопределять эти словари.

| Файл | Что задаёт |
| --- | --- |
| [`authority.yaml`](authority.yaml) | Уровни нормативности `visual-canon / brief / prompt / stage / none`, статусы и маркеры |
| [`access.yaml`](access.yaml) | Контуры доступа `public / internal / restricted`, наследование строгости и пресет публичной выгрузки |

Оверлей frontmatter для продуктовых документов в `pictures/` — в `HYAI/meta/schema/domains/picture.yaml`.
