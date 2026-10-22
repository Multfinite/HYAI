---
id: kernel.spec.manifest-v2
title: "Формат HYAI: манифест, домен, профиль"
type: spec
status: approved
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# Формат HYAI

Три уровня данных, три владельца. Флаги-состояния не используются: то, что нужно решить, решает агент или пользователь, а не константа в конфиге.

## 1. Уровни

| Уровень | Файл | Содержит |
| --- | --- | --- |
| Проект | `HYAI/meta/manifest.yaml` | `active`, `domains`, `paths`, `path_map`, `report`, `decisions`, `permissions`, `validation` |
| Домен | `HYAI/core/domains/<d>/manifest.yaml` | `root_paths`, `authority`, `access`, `schema`, `lint`, `policy`, `agents`, `registry`, `profiles`, `checks` |
| Профиль | `HYAI/core/domains/<d>/profiles/<p>/profile.yaml` | `topic`, `thought_process`, `scope_primary`/`scope_secondary`, `produced_artifacts`, `workflow`, `definition_of_done`, `checklist`, `includes`, `checks` |

Профиль **не содержит** `permissions` и не содержит флагов включения: права общие, зона ответственности описана путями и объявляется в отчёте полем `cross_scope`.

## 2. Поля манифеста проекта

| Поле | Смысл | Проверяется |
| --- | --- | --- |
| `apiVersion: hyai/v1` | Формат | `check_manifest.py` |
| `active[].domain/.profile` | Что включено | `check_domains.py` |
| `domains` | Реестр доменов | `check_indexes.py` |
| `paths` | Все каталоги и файлы | `check_indexes.py` |
| `path_map` | Путь → домен | `frontmatter.py` |
| `report` | Виды отчётов, поля, шаблоны, индекс | `check_report.py` |
| `decisions` | Области, префиксы, бюджет | `check_decisions.py` |
| `permissions` | Запреты и зоны одобрения | `check_manifest.py` |
| `validation` | Списки команд конвейера | `run_checks.py` |

## 3. Поля домена

| Поле | Обязательно | Смысл |
| --- | --- | --- |
| `metadata.name` | да | Совпадает с именем каталога |
| `root_paths` | да | Каталоги продукта, принадлежащие домену |
| `authority.schema` | да | Словарь уровней нормативности и статусов |
| `access.schema` | да | Контуры доступа, правила, пресеты выгрузки |
| `policy` | да | Политика домена с собственным префиксом |
| `profiles` | да, ≥1 | Карта профилей |
| `schema` | да | Оверлей frontmatter в `HYAI/meta/schema/domains/` |
| `registry`, `workflows_dir`, `templates_dir`, `lint`, `checks` | нет | Дополнительные данные и проверки |

## 4. Поля профиля

| Поле | Смысл |
| --- | --- |
| `topic` | Одна строка: что делает профиль |
| `thought_process` | Как профиль рассуждает: короткий цикл или длинная цепочка |
| `scope_primary` / `scope_secondary` | Где работает по умолчанию и где может работать с объявлением |
| `produced_artifacts` | Что остаётся после работы |
| `workflow` | Основной процесс: `<domain>/<slug>` или ядерный |
| `definition_of_done` | Проверяемые условия завершения |
| `checklist` | Вопросы, которые профиль обязан закрыть сам |
| `includes` | Общие участки из `HYAI/core/shared/` |
| `checks` | Профильные команды (необязательно) |

## 5. Чего в формате нет

| Чего нет | Почему |
| --- | --- |
| Флагов включения и режимов (`activation`, `assumed`, `self_editable`) | Решение принимает агент предложением или пользователь указанием; константа это решение подменяет |
| Прав в профиле | Права у агента общие; зона ответственности — про territorio работы, а не про разрешения |
| Отдельного «гибридного» профиля | Несколько доменов — это несколько пар в `active` |
| Списка процессов в коде | Процессы обнаруживаются по файлам домена |
