---
id: root.claude
title: "CLAUDE.md — адаптер для Claude Code"
type: meta
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# CLAUDE.md

Единственная точка входа — [`AGENTS.md`](AGENTS.md). Он собирается из `HYAI/core/kernel/agents.md` и фрагментов активных доменов, поэтому здесь намеренно нет дублирования правил: копия неизбежно разойдётся с источником. Проверка расхождения — `python3 HYAI/tools/assemble_agents.py --check`.

Порядок чтения для Claude Code:

1. [`AGENTS.md`](AGENTS.md) — домен, профиль, ворота, запреты.
2. [`HYAI/core/kernel/principles.md`](HYAI/core/kernel/principles.md) — `3D`, `HaRD`, `INRA`.
3. [`HYAI/meta/project.md`](HYAI/meta/project.md) — что за проект.
4. [`HYAI/core/domains/<domain>/policy.md`](HYAI/core/domains/) — правила предметной области.
5. [`HYAI/core/domains/<domain>/profiles/<profile>/README.md`](HYAI/core/domains/) — зона и критерий готовности.

Если файл правил выглядит противоречиво — это повод для решения в [`HYAI/meta/decisions/<scope>/`](HYAI/meta/decisions/README.md), а не для выбора «более удобного» правила.
