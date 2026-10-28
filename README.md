---
id: root.readme
title: "HYAI — Help Your AI: домены, профили, проверки"
type: meta
status: approved
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# HYAI — Help Your AI

**Релиз 1.0.0.** Каркас, который говорит ИИ-агенту **где он работает, по каким правилам и чем измеряется готовность**, — и проверяет это скриптами, а не доброй волей.

Три слоя, у каждого своя судьба при обновлении:

| Слой | Что внутри | Кому принадлежит |
| --- | --- | --- |
| [`HYAI/core/`](HYAI/core/README.md) | инструкции агенту: ядро, домены, профили, общие участки | каркасу; единственная переносимая часть, ставится сабмодулем |
| [`HYAI/meta/`](HYAI/meta/README.md) | **шаблон** данных проекта: манифест, архитектура, словари, решения, отчёты | каркасу; в конкретном проекте живёт копия в `./meta` |
| [`HYAI/tools/`](HYAI/tools/README.md) | **встроенные** движки проверок каркаса | каркасу; проект кладёт свои движки в `./tools` |

Данные и движки конкретного проекта лежат **в корне проекта**: `meta/` (паспорт, манифест,
архитектура, решения, отчёты) и `tools/` (собственные проверки). `HYAI/meta/` — лишь шаблон,
из которого эти каталоги создаются; `HYAI/tools/` — встроенные движки, общие для всех проектов.

Всё остальное (`src/`, `docs/`, `specs/`, `diagrams/`, `world/`, `chapters/`, `drafts/`, `styles/`) — продукт проекта. Каркас его описывает, но не содержит.

## Четыре принципа

Они действуют на каждый файл, движок и правило (`HYAI/core/kernel/principles.md`):

| Принцип | Смысл | Чем проверяется |
| --- | --- | --- |
| `3D` — Dehardcode, Data Driven | предметное знание живёт в данных, а не в коде | `check_domains.py` (чистота движков), отсутствие `FALLBACK_*` |
| `HaRD` — Human Readable & Redactable | `.md`/`.yaml`/`.json`, единый frontmatter, бюджет строк | `frontmatter.py`, `whitespace.py`, `check_links.py` |
| `INRA` — If Not Restricted Then Allowed | ограничивает только записанное пользователем: `HYAI-PERM-N*`, `exclude`, `require_approval_for`, политика домена, контуры; агент запретов для себя не выдумывает | `check_manifest.py`, `lint_scopes.py`, `lint_terms.py` (`kernel.invented-ban`) |
| `HELPER` — AI are helper, not lickspittle | цель — решённая задача, а не довольный пользователь: без лести, без выпрашивания одобрения, без сокрытия провала | `lint_terms.py` (`kernel.no-flattery`, `kernel.no-approval-begging`) |

Из `INRA` следуют два запрета: на поля-флаги (`self_editable`, `assumed`, `activation` — решение принимает агент предложением или пользователь) и на выдуманные запреты (отказ обязан ссылаться на ID правила).

Из `HELPER` следует, что отчёт не хвалит, а показывает: что сделано, что проверено, что не сходится.

## Куда идти за ответом

| Вопрос | Файл |
| --- | --- |
| Как агенту начать работу | [`AGENTS.md`](AGENTS.md) — генерируется из [`HYAI/core/kernel/agents.md`](HYAI/core/kernel/agents.md) |
| Какой домен и профиль выбрать | [`HYAI/core/kernel/routing.md`](HYAI/core/kernel/routing.md) |
| Что за проект | [`HYAI/meta/project.md`](HYAI/meta/project.md) |
| Что нельзя делать никогда | [`HYAI/core/kernel/policies/permissions.md`](HYAI/core/kernel/policies/permissions.md) |
| Как агент разговаривает с пользователем | [`HYAI/core/kernel/policies/interaction.md`](HYAI/core/kernel/policies/interaction.md) — тон, вопросы, формат ответа, SPA |
| Как устроен домен | [`HYAI/meta/architecture.md`](HYAI/meta/architecture.md) → `HYAI/meta/architecture/<domain>.md` |
| Что значит слово | [`HYAI/meta/terminology.md`](HYAI/meta/terminology.md) → `HYAI/meta/terminology/<domain>.md` |
| Почему сделано именно так | [`HYAI/meta/decisions/README.md`](HYAI/meta/decisions/README.md) |
| Что ещё неизвестно | [`HYAI/meta/questions.md`](HYAI/meta/questions.md) → `HYAI/meta/questions/<domain>.md` |
| Какие проверки есть и как их запускать | [`HYAI/tools/README.md`](HYAI/tools/README.md) |
| Что делал агент в прошлый раз | [`HYAI/meta/reports/README.md`](HYAI/meta/reports/README.md) |
| Что вошло в релиз | [`CHANGELOG.md`](CHANGELOG.md) |

## Домены и профили

| Домен | Профили | Что покрывает |
| --- | --- | --- |
| [`kit`](HYAI/core/domains/kit/README.md) | `domain-builder`, `profile-builder` | создание доменов и профилей; себя и ядро не меняет |
| [`software`](HYAI/core/domains/software/README.md) | `code`, `architect`, `analysis` | код, тесты, контракты, архитектура ПО |
| [`docs`](HYAI/core/domains/docs/README.md) | `spec-author`, `tech-writer`, `diagrams`, `analysis` | ТЗ, технические спецификации, документация, комментарии, схемы |
| [`narrative`](HYAI/core/domains/narrative/README.md) | `lore`, `history`, `prose`, `analysis` | факты мира, хронология, текст |
| [`picture`](HYAI/core/domains/picture/README.md) | `instant`, `pipeline`, `art-director`, `analysis` | генерация изображений, конвейеров звеньев и серий через промпт |

Профиль описывает **тему, задачу и мыслительный процесс**, а не права: права у агента общие, профиль заявляет зону ответственности, а выход за зону объявляется полем `cross_scope`. Домен и профиль агент либо берёт из слов пользователя, либо предлагает 2–3 варианта с ценой, либо объявляет выбор одной строкой — и фиксирует его в отчёте.

Активные пары этого репозитория — в [`HYAI/meta/manifest.yaml`](HYAI/meta/manifest.yaml).

## Установка в проект

Каркас ставится в каталог `HYAI/` проекта: переносится `HYAI/core/` (инструкции), `HYAI/meta/` —
шаблон данных, `HYAI/tools/` — встроенные движки. Данные и движки **конкретного проекта** живут
в его корне — `./meta` и `./tools` — и каркасу не принадлежат.

```bash
git submodule add <repo-url> HYAI   # каркас целиком: core + шаблон meta + встроенные tools
```

Порядок подключения:

1. Поставить каркас каталогом `HYAI/` (сабмодуль или копия).
2. Скопировать шаблон `HYAI/meta/` в `./meta` проекта, свои движки положить в `./tools`.
3. В `meta/manifest.yaml` оставить нужные пары в `active`, поправить `paths` и `path_map`
   под свои каталоги; `framework.root` указать так, как каркас лежит в репозитории (`HYAI/`).
4. Заполнить `meta/project.md` и `meta/architecture/<domain>.md`.
5. Добавить команды своего стека в `validation.project`.
6. Собрать инструкции: `python3 HYAI/tools/assemble_agents.py --write`.
7. Прогнать конвейер: `python3 HYAI/tools/run_checks.py`.

## Быстрый старт

```bash
python3 HYAI/tools/run_checks.py                            # весь конвейер, 18 проверок
python3 HYAI/tools/assemble_agents.py --check               # AGENTS.md не дрейфует
python3 -m unittest discover -s HYAI/tools/tests            # 67 тестов каркаса
```

Падающая проверка исправляется, а не отключается (`HYAI-PERM-N01`).

## Лицензия

**GNU General Public License v3.0** (`GPL-3.0-only`) — полный текст в [`LICENSE`](LICENSE). Идентификатор SPDX: `GPL-3.0-only`; он проставлен в заголовке каждого Python-движка.

Почему GPLv3, а не AGPL: каркас распространяется как файлы в репозитории и не является сетевым сервисом, поэтому сетевой оговорки AGPL не требуется. Копилефт здесь уместен: правила, которые проверяют работу, должны оставаться открытыми у тех, кто их использует.

Производные проекты, установившие `HYAI/core` сабмодулем, распространяют свой код под своей лицензией, но изменения в самом `HYAI/core` остаются под GPL-3.0.

## Чего здесь нет

Монолитного CLI, базы данных, скрытых состояний и «умных» умолчаний в коде: только Python-скрипты без зависимостей, Markdown и YAML, которые читаются глазами. Нет данных — движок возвращает код `2`, а не догадку (`3D`).
