---
id: decision.project.P-0001
title: "Единые требования общего входа агента"
type: decision
status: review
authority: contract
visibility: internal
scope: project
affects_domains: [kit, software, docs, narrative]
affects:
  - "HYAI/core/kernel/agents.md"
  - "HYAI/core/domains/docs/agents.md"
  - "HYAI/core/domains/kit/agents.md"
  - "HYAI/core/domains/narrative/agents.md"
  - "HYAI/core/domains/software/agents.md"
  - "AGENTS.md"
supersedes: null
---

# P-0001. Единые требования общего входа агента

## Решение

Общие требования из ядра применяются во всех активных доменах. Краткие доменные фрагменты дают контекст и ключевые отличия; они не заменяют и не ослабляют политики, access-правила, профили и workflow доменов. Перегруппировка не отменяет общие требования о выборе домена/профиля, permissions, провенансе, границах, воротах и результате работы.

## Почему

`AGENTS.md` собирает общее ядро и фрагменты всех активных доменов. Краткие сводки уменьшают повторы в общем входе, а чтение выбранных доменных источников сохраняет полные требования.

## Границы

- Решение распространяется на `kit`, `software`, `docs` и `narrative`.
- Оно не вводит численный порог токенов, требования к провайдеру или runtime-функции.

## Открытые вопросы

- `Q-KIT-01` остаётся открытым: способ загрузки `AGENTS.md` зависит от host/runtime.
