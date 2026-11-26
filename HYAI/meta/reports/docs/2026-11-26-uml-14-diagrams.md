---
id: report.docs.2026-11-26-uml-14-diagrams
title: "Регламент и навыки по 14 диаграммам UML 2.5"
type: report
report_kind: task
domain: docs
profile: docs/diagrams
status: approved
authority: none
visibility: internal
date: "2026-11-26"
workflow: docs/diagrams
decisions: [DOC-0001]
cross_scope:
  - path: "HYAI/core/shared/skills/uml/SKILL.md"
    why: "общая активация UML — авторский навык вне зоны профиля docs/diagrams"
    profile: kit/domain-builder
  - path: ".claude/agents/Technical Writer.md"
    why: "унаследованный хвостовой пробел ронял проверку whitespace; удалён минимальным диффом"
    profile: kit/domain-builder
---

# Регламент и навыки по 14 диаграммам UML 2.5

## Задача

Добавить инструкции и регламенты, как делать все 14 UML-диаграмм, навык по каждой диаграмме
и общую активацию UML. Домен — `docs`, профиль — `docs/diagrams`. Готовность измеряется:
список из 14 типов UML 2.5 закрыт, правила определены и проходят `check_rules.py`,
навыки собираются `build_skills.py`, конвейер проверок зелёный.

## Что сделано

- `HYAI/core/domains/docs/policy.md` — добавлены общие правила `DOC-POL-16..20` и правила
  по каждому из 14 типов `DOC-POL-21..34`; разделы перенумерованы, версия 1.2.
- `HYAI/core/domains/docs/uml.md` — создан регламент: каркас из девяти шагов, таблица выбора
  типа, по разделу на каждую диаграмму (вопрос, источник, нотация, элементы, связи, ошибки,
  проверка) и чек-лист публикации.
- `HYAI/core/domains/docs/workflows/uml-*.md` — создано 14 процессов с триггерами `when_to_use`;
  из них собраны навыки `hyai-docs-uml-*`.
- `HYAI/core/shared/skills/uml/SKILL.md` — создан авторский навык общей активации: выбор типа
  по вопросу, таблица перехода к 14 точечным навыкам, регламент и границы.
- `HYAI/core/domains/docs/workflows/README.md`, `HYAI/core/domains/docs/README.md`,
  `HYAI/core/domains/docs/profiles/diagrams/README.md`,
  `HYAI/core/domains/docs/registry/documents.yaml` — навигация и реестр обновлены.
- `HYAI/meta/decisions/docs/DOC-0001-uml-14-diagrams.md` — зафиксирована норма; индексы
  решений обновлены.
- `.claude/agents/Technical Writer.md` — удалён хвостовой пробел, который падал ещё до задачи.
- `.claude/skills/` — пересобрано: 62 навыка, 69 файлов, устаревших удалено 0.
- Владелец дал `approved` [А]: 17 файлов переведены в `approved`, `Q-DOC-01` закрыт.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| полный конвейер | `python3 HYAI/tools/run_checks.py --skip-project` | 30 проверок, 0 падений |
| сборка навыков | `python3 HYAI/tools/build_skills.py --check` | дрейфа нет |
| правила | `python3 HYAI/tools/check_rules.py` | `DOC-POL-16..34` определены и ссылаются корректно |
| навигация | `python3 HYAI/tools/check_indexes.py` | все новые файлы упомянуты в README и реестрах |

Ручная проверка смысла: 14 процессов соответствуют 14 правилам `DOC-POL-21..34`; каждый
процесс ссылается на `uml.md` и `policy.md`; навык активации не подменяет процесс, а только
выбирает его.

## Открытые вопросы

- `Q-DOC-02` — нужна ли генерация Mermaid/PlantUML-файлов в `diagrams/**` как рабочие примеры,
  либо достаточно регламента и навыков.
