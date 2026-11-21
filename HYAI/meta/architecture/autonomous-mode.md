---
id: meta.architecture.autonomous-mode
title: "Автономный режим и состояния установки HYAI"
type: architecture
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-21"
---

# Автономный режим и состояния установки HYAI

Описывает три состояния установки каркаса и правила резолвинга путей. Это описание
существующего поведения, а не норма: проверяемые требования — `REQ-01`..`REQ-06`
ниже, тесты — `AutonomousModeTest` в `HYAI/tools/tests/test_domains.py`.

## Состояния установки

| Состояние | Признаки | Резолвинг | Требования |
| --- | --- | --- | --- |
| `standalone` | нет `./meta/manifest.yaml`; манифест `HYAI/meta/manifest.yaml` | `fw_root = <root>/HYAI`; данные в `HYAI/meta/` | `REQ-01`, `REQ-02` |
| `consumer/submodule` | `./meta/manifest.yaml`; `.gitmodules` объявляет `framework.root` | `fw_root = <root>/<framework.root>`; данные в `./meta` | `REQ-03`, `REQ-04` |
| `consumer/copy` | `./meta/manifest.yaml`; `HYAI/` скопирован, `.gitmodules` нет | идентичен `consumer/submodule` | `REQ-04` |

Состояние выводит функция `resolve_mode(root)` из `HYAI/tools/_shared.py` по файловой
структуре, а не по полю конфигурации. `.gitmodules` различает только происхождение
установки: на резолвинг путей не влияет.

## Резолвинг путей

| Правило | Смысл | Требование |
| --- | --- | --- |
| `PROJECT_ROOT` | корень берётся из рабочего каталога (`Path.cwd()`), не из места запуска скрипта | `REQ-01` |
| `FRAMEWORK_ROOT` | `<root>/<framework.root>`; пустое или `.` — сам `root` | `REQ-01`, `REQ-03` |
| `fw(root, rel)` | сначала `<root>/rel` (данные проекта), затем `<FRAMEWORK_ROOT>/rel` (пути каркаса) | `REQ-04` |
| `submodule_prefixes` | только для consumer: `HYAI` + `framework.root`/`framework.prefix` | `REQ-03` |

## Требования

| ID | Требование | Критерий приёмки |
| --- | --- | --- |
| `REQ-01` | `standalone` опознаётся автономно | `resolve_mode(root) == "standalone"`, `manifest_path == HYAI/meta/manifest.yaml`, `fw_root == <root>/HYAI`, `submodule_prefixes == []` |
| `REQ-02` | автономный конвейер работает на Windows без внешней переменной | `python3 HYAI/tools/run_checks.py --skip-project` → `rc=0`, без `UnicodeDecodeError` |
| `REQ-03` | связка с проектом сохраняется | фикстура consumer проходит без правок; `submodule_prefixes` содержит `HYAI` |
| `REQ-04` | локальная структура без подмодуля работает | проект с `./meta/manifest.yaml` и скопированным `HYAI/` без `.gitmodules`: проверки зелёные, `resolve_mode == "consumer/copy"` |
| `REQ-05` | один код поддерживает оба расклада | полный `run_checks.py` зелёный в standalone и consumer; тесты не ослаблены |
| `REQ-06` | правила задокументированы | `README.md`, [`HYAI/meta/architecture/`](README.md) и этот файл описывают состояния; `check_links.py` зелёный |

## Соответствие `REQ-AUT-0N` ↔ `REQ-0N`

В §4 архитектуры (`ee6222f5`) шесть пунктов сформулированы с префиксом `REQ-AUT-0N`.
`check_rules.py` требует регистрации владельца ID в `HYAI/meta/schema/rule-ids.yaml`
(`HYAI-PERM-G05`); владелец `REQ` в реестре отсутствует, защищённую схему не трогаем.
Поэтому в этом документе принят канонический префикс `REQ-0N` (`DOC-POL-02`).
Соответствие взаимно-однозначное, формулировки и критерии приёмки из §4 не меняются:

| Пункт §4 (`ee6222f5`) | Канонический ID | Требование |
| --- | --- | --- |
| `REQ-AUT-0N` / 01 | `REQ-01` | S1 опознаётся автономно |
| `REQ-AUT-0N` / 02 | `REQ-02` | автономный конвейер работает на Windows без внешней переменной |
| `REQ-AUT-0N` / 03 | `REQ-03` | связка с проектом сохраняется |
| `REQ-AUT-0N` / 04 | `REQ-04` | локальная структура без подмодуля работает |
| `REQ-AUT-0N` / 05 | `REQ-05` | один код поддерживает оба расклада без регрессии |
| `REQ-AUT-0N` / 06 | `REQ-06` | правила задокументированы |

## Открытые вопросы

- `[?]` `Q-AUT-01` — нужен ли явный флаг `framework.deployment`? Черновик `KIT-0010` из задания `ee6222f5`; требует одобрения владельца (`HYAI-PERM-G05`).
- `[?]` `Q-AUT-02` — префикс `REQ-AUT-*` из задания `ee6222f5` не проходит `check_rules.py`: владелец `REQ` не зарегистрирован в `HYAI/meta/schema/rule-ids.yaml`. Здесь использован канонический `REQ-NN`; регистрация `REQ` — отдельное одобрение (`HYAI-PERM-G05`).
