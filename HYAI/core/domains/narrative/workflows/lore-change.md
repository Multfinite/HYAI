---
id: domain.narrative.workflow.lore-change
title: "Процесс narrative/lore-change: изменение факта мира"
type: workflow
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `narrative/lore-change`

1. **Найти существующее.** Карточка сущности, упоминания в тексте, решения `NR-*`. Новый факт проверяется против уже установленных.
2. **Определить уровень.** `core` / `setting` / `detail` / `presentation`. От уровня зависит, нужно ли одобрение (`NR-POL-02`).
3. **Проверить конфликты.** Что ломается: даты, связи, способности, география. Каждый конфликт — явно, с решением (`NR-POL-01`).
4. **Доступ.** Определить `visibility` и `knowledge`; для секрета — `known_by` (`NR-POL-11`).
5. **Записать.** Карточка по шаблону `templates/entity-card.md`; правка с маркерами `[А]/[И]/[В]/[Г]`.
6. **Проверить.** `run_checks.py`, `lint_scopes.py`; при изменении `core` — решение `NR-NNNN`.

Запрещено: править факт «заодно» при работе над текстом (`NR-POL-03`, `cross_scope`).
