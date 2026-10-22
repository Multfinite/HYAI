---
id: hyai.tests.readme
title: "HYAI/tools/tests/ — тесты каркаса"
type: tool
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Тесты

Проверяют не продукт, а каркас: что движки действительно читают данные, что профили не пустые и что добавление домена не требует правок Python.

| Файл | Что покрывает |
| --- | --- |
| [`_kit.py`](_kit.py) | Копия каркаса во временный каталог и правки-мутации для тестов |
| [`test_core_tools.py`](test_core_tools.py) | `frontmatter`, `check_links`, `lint_terms`, `whitespace`, `check_indexes` на синтетических репозиториях |
| [`test_domains.py`](test_domains.py) | Структура домена и профиля, контракт переопределений, зоны |
| [`test_reports_decisions.py`](test_reports_decisions.py) | Отчёты по доменам, виды отчётов, решения и `affects` |
| [`test_access.py`](test_access.py) | «Роль × призма», компетенции, карта понимания, выгрузки |
| [`test_rules.py`](test_rules.py) | Идентификаторы правил: формат, владелец, дубли, висячие ссылки, `retired`; ворота выгрузки |
| [`test_self_check.py`](test_self_check.py) | Матричный прогон по всем активным парам и сборка `AGENTS.md` |

Копия каркаса для мутаций — [`_kit.py`](_kit.py).
