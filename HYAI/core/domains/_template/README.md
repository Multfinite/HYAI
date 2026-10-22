---
id: domain._template.readme
title: "Скелет нового домена"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `_template` — скелет домена

Копируется в `HYAI/core/domains/<new>/` и заполняется по [`../kit/workflows/domain-authoring.md`](../kit/workflows/domain-authoring.md).

Домен `_template` не зарегистрирован в `HYAI/meta/manifest.yaml` и не проверяется `check_domains.py` как рабочий — он образец.

## Что заменить

| Файл | Заменить |
| --- | --- |
| `manifest.yaml` | `<domain>`, `root_paths`, `decisions_scope`, список профилей |
| `policy.md` | префикс `NEW-`, 5–12 правил предметной области |
| `authority.md`, `schema/authority.yaml` | уровни нормативности домена (могут отличаться от других) |
| `access.md`, `schema/access.yaml` | контуры доступа; `model: flat` или `role_prism` |
| `agents.md` | фрагмент `AGENTS.md`: что домен требует всегда |
| `registry/documents.yaml` | какие документы читать первыми |
| `templates/` | формы результата домена (`template_kind: output`) |
| `profiles/_template/` | один профиль: тема, мыслительный процесс, зона, критерий готовности |

## Чего в скелете нет и не должно быть

Правил из других доменов, собственных скриптов и `permissions`: домен добавляет данные и нормы, но не механику.
