---
id: hyai.domains.readme
title: "HYAI/core/domains/ — предметные области"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Домены

Домен — предметная область со **своей** нормативностью и **своей** системой доступа. Профили домена не могут переопределять ни то, ни другое.

| Домен | Что покрывает | Профили |
| --- | --- | --- |
| [`kit`](kit/README.md) | создание доменов и профилей, правила каркаса | `domain-builder`, `profile-builder` |
| [`software`](software/README.md) | код, тесты, контракты, архитектура ПО | `code`, `architect`, `analysis` |
| [`docs`](docs/README.md) | ТЗ, спецификации, документация, диаграммы | `spec-author`, `tech-writer`, `diagrams`, `analysis` |
| [`narrative`](narrative/README.md) | факты мира, хронология, текст | `lore`, `history`, `prose`, `analysis` |
| [`picture`](picture/README.md) | промптовая генерация изображений, конвейеры звеньев и серии | `instant`, `pipeline`, `art-director`, `analysis` |
| [`_template`](_template/README.md) | скелет нового домена | — (образец) |

## Состав домена

```
manifest.yaml        границы, профили, проверки
README.md            что лежит в домене
policy.md            правила домена с собственным префиксом
agents.md            фрагмент AGENTS.md
authority.md         что значит «норма» в этом домене
schema/authority.yaml  машинный словарь уровней и статусов
access.md            контуры доступа домена
schema/access.yaml   машинное описание доступа
workflows/           процессы домена
templates/           формы результата домена
registry/            что читать первым
profiles/<p>/        тема, мыслительный процесс, зона, критерий готовности
```

## Правила

1. Домен без собственных правил и своей системы доступа не создаётся (`KIT-POL-05`).
2. Домены не импортируют друг друга: связь — через `HYAI/meta/decisions/project/` (`P-*`).
3. Создание и изменение домена — процесс [`kit/domain-authoring`](kit/workflows/domain-authoring.md).
