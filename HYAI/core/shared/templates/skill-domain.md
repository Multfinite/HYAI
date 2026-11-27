---
id: shared.template.skill-domain
title: "Каркас навыка домена: профили, закон и проверки"
type: template
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-11-19"
template: true
template_kind: output
---

# Домен `{{domain}}` — {{title}}

## Когда использовать

{{when_to_use}}

## Закон домена

{{policy_classes}}

Правил домена: {{rule_count}}.

Разделы политики:

{{policy_sections}}

Индекс по идентификаторам — [`references/rules.md`]({{rules_index_link}}); полный текст —
[`policy.md`]({{policy_link}}).

## Профили

{{profiles_table}}

Профиль задаёт тему, зону ответственности и критерий готовности, но не права (`KIT-POL-09`).
Правка за пределами зоны объявляется в `cross_scope` отчёта, а не отменяется.

## Проверки

{{checks}}

Перед завершением — проверки по зоне правки (`HYAI-INT-31`); полный конвейер — только по необходимости.

## Читать первым

{{read_first}}

## Границы

- Домен не даёт прав: контуры доступа — в [`access.md`]({{access_link}}), ворота — в
  `{{entrypoint}}`.
- Правило домена старше профиля: профиль уточняет, но не отменяет (`MERGE-01..06`).
- Навык — проекция. Источник правила остаётся в файлах домена; правка навыка правилом не
  является.
