---
id: meta.schema.readme
title: "HYAI/meta/schema/ — машинная схема frontmatter"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `HYAI/meta/schema/`

Данные, которые читает [`../../HYAI/tools/frontmatter.py`](../../../HYAI/tools/frontmatter.py). Доменная семантика сюда не попадает: движок один, схем несколько.

| Файл | Что |
| --- | --- |
| [`frontmatter.yaml`](frontmatter.yaml) | Базовая схема: обязательные поля, общие enum, пропуски, умолчания, правила слияния |
| [`domains/software.yaml`](domains/software.yaml) | Оверлей домена `software` |
| [`domains/docs.yaml`](domains/docs.yaml) | Оверлей домена `docs` |
| [`domains/narrative.yaml`](domains/narrative.yaml) | Оверлей домена `narrative` |
| [`domains/kit.yaml`](domains/kit.yaml) | Оверлей домена `kit` |

## Правила слияния (`MERGE`)

| Элемент | Правило |
| --- | --- |
| `required` | Объединение: домен может требовать больше, никогда меньше |
| `enums` | Замена по ключу: `visibility` домена заменяет базовый |
| `defaults_by_dir` | Переопределение по ключу |
| `skip_parts` / `skip_prefixes` | Объединение |
| `field_aliases` | Объединение |

| [`rule-ids.yaml`](rule-ids.yaml) | Владельцы и классы идентификаторов правил, файлы-источники, вышедшие номера | `check_rules.py` |
| [`frontmatter.yaml`](frontmatter.yaml) | Базовая схема frontmatter и запрещённые поля-флаги | `frontmatter.py` |

## Чего здесь нет

Словаря уровней нормативности (`authority`) и статусов: они принадлежат строгой зоне домена — `HYAI/core/domains/<domain>/schema/authority.yaml` (`PROV`, `MERGE-05`).
