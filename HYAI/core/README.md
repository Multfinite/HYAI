---
id: core.readme
title: "HYAI/core/ — инструкции агенту"
type: meta
status: approved
authority: invariant
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# `HYAI/core/` — инструкции агенту

Переносимая часть каркаса: правила, домены, профили, процессы, шаблоны. Это единственный каталог, который обновляется из общего репозитория. Здесь **нет** данных проекта и нет скриптов: шаблон данных лежит в [`../meta/`](../meta/README.md), встроенные движки — в [`../tools/`](../tools/README.md). Данные и движки конкретного проекта живут в его корне — `./meta` и `./tools`.

## Состав

| Путь | Что | Меняет |
| --- | --- | --- |
| [`kernel/`](kernel/README.md) | Правила для любого домена, принципы, маршрутизация, спецификация формата | только владелец |
| [`domains/`](domains/README.md) | `kit`, `software`, `docs`, `narrative`, скелет `_template` | домены; чужие — через `kit` |
| [`shared/`](shared/README.md) | Общие участки, подключаемые доменами (`analysis`, шаблоны) | `kit` |

## Порядок чтения

1. [`kernel/principles.md`](kernel/principles.md) — четыре принципа: `3D`, `HaRD`, `INRA`, `HELPER`.
2. [`kernel/policies/permissions.md`](kernel/policies/permissions.md) — что нельзя никогда.
3. [`kernel/routing.md`](kernel/routing.md) — как выбрать домен и профиль.
4. Домен: `domains/<domain>/policy.md` и `domains/<domain>/profiles/<profile>/README.md`.

Собранная версия этих инструкций — `AGENTS.md` в корне проекта; она генерируется [`../tools/assemble_agents.py`](../tools/assemble_agents.py) и не правится руками.

## Чего здесь нет

Слов «код», «лор», «глава» в ядре нет: если такое слово понадобилось в `kernel/`, правило принадлежит домену.
