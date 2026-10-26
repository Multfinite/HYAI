---
id: decision.kit.KIT-0001
title: "Структура общего входа агента"
type: decision
status: review
authority: contract
visibility: internal
scope: kit
affects_domains: []
affects:
  - "HYAI/core/kernel/agents.md"
  - "HYAI/core/domains/docs/agents.md"
  - "HYAI/core/domains/kit/agents.md"
  - "HYAI/core/domains/narrative/agents.md"
  - "HYAI/core/domains/software/agents.md"
  - "AGENTS.md"
supersedes: null
---

# KIT-0001. Структура общего входа агента

## Решение

Общий вход агента группирует инструкции по этапам работы; доменные фрагменты кратко задают область и ключевые отличия, а подробные требования остаются в политиках, профилях и workflow. `AGENTS.md` генерируется из ядра и фрагментов активных доменов.

## Почему

Фрагменты доменов попадают в общий entrypoint. Краткая выжимка уменьшает повторение подробных политик, сохраняя навигацию и критичные напоминания.

## Границы

- Решение касается структуры входного текста каркаса, а не изменения предметных правил доменов.
- Оно не задаёт численную цель экономии и не добавляет runtime, API провайдера или динамическую загрузку контекста.

## Открытые вопросы

- Нет в рамках этого решения.
