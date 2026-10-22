---
id: shared.readme
title: "HYAI/core/shared/ — общие участки доменов"
type: meta
status: approved
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# `HYAI/core/shared/`

Место для того, что нужно **нескольким доменам в одинаковом виде**. Правило простое: если две копии одного участка обязаны меняться синхронно — участок живёт здесь, а домены подключают его через `includes`.

| Что | Где | Кто подключает |
| --- | --- | --- |
| Профиль разбора `analysis` (общая часть) | [`profiles/analysis/`](profiles/analysis/profile.yaml) | `software/analysis`, `docs/analysis`, `narrative/analysis` |
| Шаблон отчёта разбора | [`templates/analysis-report.md`](templates/analysis-report.md) | `report.templates.analysis` манифеста |

## Почему профиль `analysis` остаётся в каждом домене

Домены различаются предметом разбора: код, документ, корпус мира. Общая у них механика — вопрос, факты с маркерами, варианты с ценой, рекомендация, открытые вопросы. Механика — здесь, специфика — в домене.

## Как подключать

```yaml
# HYAI/core/domains/<domain>/profiles/analysis/profile.yaml
includes:
  - "HYAI/core/shared/profiles/analysis"
topic: "Разбор задач домена <domain>"
checklist:
  - "Свой вопрос этого домена"
```

Слияние: списки объединяются, словари дополняются, скалярные значения профиля побеждают. Подключение видно в `check_domains.py` — профиль без общего участка не ошибка, но дублирование его механики считается нарушением `3D`.
