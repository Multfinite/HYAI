---
id: report.kit.2026-10-28-picture-data-root-separation
title: "Перенос рабочего каталога домена picture внутрь домена HYAI и изоляция подмодуля во внешних проектах"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-10-28"
workflow: kit/domain-authoring
decisions: ["KIT-0003"]
cross_scope:
  - path: "HYAI/core/domains/picture/pictures/.gitkeep"
    why: "Перенос рабочего каталога домена picture из корня репозитория в HYAI/core/domains/picture/pictures/ с сохранением структуры"
    profile: "picture/instant"
  - path: "HYAI/meta/manifest.yaml"
    why: "Синхронизация path_map домена picture с новым путём HYAI/core/domains/picture/pictures/**"
    profile: "project/maintainer"
  - path: "HYAI/meta/project.md"
    why: "Обновление карты репозитория и паспорта активных доменов HYAI"
    profile: "project/maintainer"
  - path: "HYAI/tools/_shared.py"
    why: "Поддержка includes в манифесте активного домена, ребазирования глобов root_paths и определения границ подмодуля без доменных имён (3D)"
    profile: "software/code"
  - path: "HYAI/tools/tests/test_domains.py"
    why: "Регрессионные проверки размещения данных picture в HYAI и разделения путей HYAI и внешнего проекта-потребителя"
    profile: "software/code"
  - path: "AGENTS.md"
    why: "Пересборка входного файла агента после обновления фрагмента HYAI/core/domains/picture/agents.md"
    profile: "project/maintainer"
---

# Перенос рабочего каталога домена `picture` внутрь домена HYAI и изоляция подмодуля во внешних проектах

## Задача

По прямому указанию владельца (`[А]`) требовалось исправить расположение рабочего каталога данных самодостаточного домена `picture` в репозитории HYAI и обеспечить строгое разделение путей при подключении HYAI как подмодуля во внешнем проекте:
1. Оставить домен `picture` самодостаточным (не вложенным в `narrative`), перенеся его рабочий каталог внутри HYAI из корневого `./pictures/` в `HYAI/core/domains/picture/pictures/` с полным сохранением структуры (`briefs/`, `prompts/`, `stages/`, `assets/`).
2. Синхронно обновить `HYAI/core/domains/picture/manifest.yaml`, `HYAI/meta/manifest.yaml` (`path_map`), профили, правила `lint_terms.py`, схему `frontmatter`, архитектурную и терминологическую документацию, процессы и шаблоны, после чего пересобрать `AGENTS.md`.
3. Учесть подключение HYAI подмодулем (включая сценарий `Eidolon---Pherin` с путём `meta/hyai/domains/picture/pictures/`): правила и шаблоны HYAI не должны направлять проектные данные внутрь подмодуля, а переопределение корня данных должно выражаться чисто через манифест активного домена.
4. Добавить регрессионные проверки как на размещение `HYAI/core/domains/picture/pictures/` в самом HYAI, так и на изоляцию путей между подмодулем HYAI и внешним проектом.
5. Сохранить исторические материалы и не выставлять статус `approved` без решения владельца (`HYAI-PERM-N05`).

## Что сделано

1. **Перенос рабочего каталога в самом HYAI (`[А]`).** Каталог `pictures/` перенесён через `git mv` в `HYAI/core/domains/picture/pictures/` с сохранением `.gitkeep` в корне и в подкаталогах `briefs/`, `prompts/`, `stages/`, `assets/`; корень репозитория очищен от `./pictures/`.
2. **Согласование конфигурации и документации домена `picture` (`[И]`, `[В]`).**
   - В `HYAI/core/domains/picture/manifest.yaml` задан `root_paths: ["HYAI/core/domains/picture/pictures"]`; в `HYAI/meta/manifest.yaml` запись `path_map` обновлена на `"HYAI/core/domains/picture/pictures/**": picture` (перекрывает `"HYAI/core/**": kit` по длине префикса в `_shared.resolve_scope`); обновлены `scope_primary` / `scope_secondary` профилей `instant`, `pipeline`, `art-director`, `HYAI/meta/lint/terms/picture.json` и `HYAI/meta/schema/domains/picture.yaml`.
   - Во всех нормативных текстах, профилях, процессах (`workflows/*.md`) и шаблонах (`templates/*.md`) жёсткий путь заменён на параметризованный корень `<picture_root>`, определяемый полем `root_paths` манифеста активного домена `picture` (`PIC-POL-06`, `PIC-INV-05`), а в `HYAI/core/domains/picture/agents.md` добавлен макрос `{{HYAI}}` для корректной сборки `AGENTS.md` во внешнем проекте.
   - Уточнено проектное решение [`KIT-0003`](../../decisions/kit/KIT-0003-picture-domain.md) (`status: review`) и закрытая формулировка `Q-KIT-02` в [`HYAI/meta/questions/kit.md`](../../questions/kit.md); исторические отчёты `2026-10-28-picture-domain-analysis.md` и `2026-10-28-picture-domain-implementation.md` сохранены без изменений.
3. **Универсальное выражение через манифест активного домена и барьер подмодуля (`3D`, `KIT-INV-01`, `[В]`).**
   - В `HYAI/tools/_shared.py` добавлена поддержка наследования `includes` для `AgentDomain` (где проектный манифест активного домена, например `meta/hyai/domains/picture/manifest.yaml`, включает `HYAI/core/domains/picture/manifest.yaml` и заменяет `root_paths` на проектный путь вроде `meta/hyai/domains/picture/pictures`, а также поддержана краткая форма `active[].root_paths`), автоматическое ребазирование глобов профилей (`rebase_globs`), а в `lint_terms.py` и `frontmatter.py` — ребазирование `applies_to` и `defaults_by_dir` на фактический `root_paths`.
   - В `check_domains.py`, `check_manifest.py` и `check_indexes.py` введены машинные проверки изоляции подмодуля: в проекте-потребителе (`./meta/manifest.yaml`) активный домен обязан иметь существующий каталог `root_paths` в дереве самого проекта и не может указывать `root_paths` или `path_map` внутрь подмодуля HYAI; одновременно рабочие каталоги данных (`working_data_roots`) освобождены от требования служебных `README.md` в каждом подкаталоге промптов и звеньев.
   - Ни один файл `HYAI/tools/*.py` не содержит доменных имён (`check_purity` в `check_domains.py`).
4. **Регрессионные тесты (`[В]`).** В `HYAI/tools/tests/test_domains.py` добавлен набор `PicturePlacementAndSubmoduleSeparationTest` (4 тестовых сценария): проверка размещения `HYAI/core/domains/picture/pictures/` и отсутствия `./pictures` в HYAI, проверка полного конвейера внешнего проекта с подмодулем HYAI и корнем `meta/hyai/domains/picture/pictures/` через манифест активного домена (`includes`), проверка `active[].root_paths` и проверка отказа (`rc=1`) при утечке `root_paths` или `path_map` внутрь подмодуля.

## Проверка

- `assemble_agents.py --write` и `assemble_agents.py --check` — `AGENTS.md` пересобран и актуален (`rc=0`).
- `run_checks.py --skip-project` — все проверки ядра, сборки и активных доменов (включая `picture`) пройдены (`rc=0`).
- `lint_terms.py --strict` — `0` ошибок, `0` предупреждений (`rc=0`).
- `python -m unittest discover -s HYAI/tools/tests` — все модульные и регрессионные тесты пройдены (`rc=0`).
- `git diff --check` — нарушений пробелов и переводов строк нет (`rc=0`).

## Открытые вопросы

Новых открытых вопросов нет (`Q-KIT-02..05` остаются закрытыми; утверждение статуса `approved` для `KIT-0003` и файлов домена `picture` остаётся за владельцем по `HYAI-PERM-N05`).
