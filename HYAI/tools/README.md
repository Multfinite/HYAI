---
id: tools.readme
title: "HYAI/tools/ — движки проверок"
type: tool
status: approved
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# Движки

Движки принадлежат **этому проекту**, а не переносимому ядру: набор из поставки — рабочая основа, которую проект правит под свой стек. Неприкосновенно одно — `3D`: движок не знает предметной области, поэтому новый домен, профиль или правило не должны требовать правки Python.

Каждый скрипт — самостоятельный файл с `--root` и `--json`, зависимость только `PyYAML`. Ни один движок не знает имён доменов: пути, перечисления и списки читаются из [`../meta/manifest.yaml`](../meta/manifest.yaml) и доменных схем (`3D`, `KIT-INV-01`).

| Файл | Что проверяет | Данные откуда |
| --- | --- | --- |
| [`_shared.py`](_shared.py) | Резолвер «путь → домен», слияние профилей, обход файлов | — |
| [`frontmatter.py`](frontmatter.py) | Обязательные поля, enum, значения чужого домена | `HYAI/meta/schema/`, `core/domains/*/schema/` |
| [`check_links.py`](check_links.py) | Ссылки `.md → .md` и `.md → код` | `HYAI/meta/lint/links.json` |
| [`whitespace.py`](whitespace.py) | Хвостовые пробелы, концовка файла | `HYAI/meta/lint/whitespace.json` |
| [`lint_terms.py`](lint_terms.py) | Термины и паттерны в тексте и в коде | `HYAI/meta/lint/terms/*.json` |
| [`check_decisions.py`](check_decisions.py) | Решения: области, префиксы, `affects`, индекс | `decisions` манифеста |
| [`check_report.py`](check_report.py) | Отчёты: домен, профиль, вид, разделы, индекс | `report` манифеста |
| [`check_domains.py`](check_domains.py) | Полнота домена и профиля, зоны, чистота движков | `domains` манифеста |
| [`check_manifest.py`](check_manifest.py) | Версия формата, зоны одобрения, права в профилях | манифест |
| [`check_indexes.py`](check_indexes.py) | README каталогов, реестры, пути манифеста | `paths`, `registry` |
| [`assemble_agents.py`](assemble_agents.py) | Сборка и дрейф `AGENTS.md` | `core/kernel/agents.md`, `domains/*/agents.md` |
| [`resolve_access.py`](resolve_access.py) | Вердикт «роль × призма» и карта понимания | `domains/*/schema/access.yaml` |
| [`lint_scopes.py`](lint_scopes.py) | Секреты без носителя, закрытое в открытой выгрузке | `access.yaml` → `checks` |
| [`build_export.py`](build_export.py) | Сборка проекций по пресетам | `access.yaml` → `export.presets` |
| [`run_checks.py`](run_checks.py) | Конвейер: сборка + ядро + домены + проект | `validation` манифеста |

## Запуск

```bash
python3 HYAI/tools/run_checks.py            # весь конвейер
python3 HYAI/tools/check_domains.py --json  # одна проверка, машинный вывод
```

Тесты движков — [`tests/`](tests/README.md); они не зависят от рабочего дерева: каждый работает на одноразовой копии каркаса.
