---
id: kernel.spec.readme
title: "HYAI/core/kernel/spec/ — спецификация формата каркаса"
type: meta
status: approved
authority: invariant
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Спецификация формата

Документы этого каталога описывают, **как устроен сам каркас**: формат манифеста, правила слияния уровней, порядок миграции. Они не описывают продукт.

| Файл | Содержание |
| --- | --- |
| [`manifest-v2.md`](manifest-v2.md) | Поля `HYAI/meta/manifest.yaml`, домена и профиля; что чем проверяется |
| [`merge-rules.md`](merge-rules.md) | Слияние ядра, домена и профиля: что можно переопределить, что нельзя |
| [`rule-ids.md`](rule-ids.md) | Идентификаторы правил: владелец, класс, номер; запрет переиспользования |

Порядок создания нового домена или профиля — в домене `kit`: [`../../domains/kit/workflows/domain-authoring.md`](../../domains/kit/workflows/domain-authoring.md) и [`profile-authoring.md`](../../domains/kit/workflows/profile-authoring.md).
