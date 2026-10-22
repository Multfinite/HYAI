---
id: domain.kit.workflow.domain-authoring
title: "Процесс kit/domain-authoring: создание домена"
type: workflow
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `kit/domain-authoring`

## 1. Проверить необходимость

`KIT-POL-05`: домен нужен, если у предметной области есть **своя** нормативная база — свои уровни нормативности и своя система доступа. Если отличается только папка или чек-лист — это профиль существующего домена.

## 2. Зафиксировать зону

- `root_paths`: какие каталоги продукта принадлежат домену (`KIT-POL-06`: не пересекаются с другими).
- `path_map` в `HYAI/meta/manifest.yaml`: как резолвер узнаёт домен по пути.
- Границы с существующими доменами: что делает домен и **чего он не делает** (последнее важнее).

## 3. Создать скелет

Скопировать [`../../_template/`](../../_template/README.md) в `HYAI/core/domains/<new>/`. Минимальный состав (`KIT-POL-04`):

```
manifest.yaml  README.md  policy.md  agents.md
authority.md  schema/authority.yaml
access.md     schema/access.yaml
workflows/    templates/    registry/
profiles/<profile>/{profile.yaml,README.md}
```

## 4. Заполнить нормативную базу

1. `policy.md`: 5–12 правил с собственным префиксом. Правило без проверки — пометка `enforced: prose-only` и причина (`HYAI-PROV-09`).
2. `authority.md` + `schema/authority.yaml`: уровни и статусы. Словарь домена обязан отличаться от других доменов только там, где действительно различается смысл.
3. `access.md` + `schema/access.yaml`: контуры и правила. `model: flat` или `role_prism`.
4. `lint/terms.json`: доменные правила терминов с обязательным `applies_to`.

## 5. Подключить

- `HYAI/meta/manifest.yaml`: `domains.<new>`, при необходимости `active`, `path_map`, `decisions.scopes.<new>`.
- `HYAI/meta/schema/domains/<new>.yaml`: оверлей frontmatter.
- `HYAI/meta/architecture/<new>.md`, `HYAI/meta/terminology/<new>.md`, `HYAI/meta/questions/<new>.md`.

## 6. Проверить

```bash
python3 HYAI/tools/check_domains.py
python3 HYAI/tools/check_manifest.py
python3 HYAI/tools/frontmatter.py --check
python3 HYAI/tools/run_checks.py
```

`KIT-POL-07`: если проверка потребовала правки `HYAI/tools/*.py`, работа не закончена — нужно исправить каркас, а не домен.

## 7. Записать решение

`HYAI/meta/decisions/kit/KIT-NNNN-<slug>.md`: что за домен, какие границы, почему не профиль, чем проверяется.
