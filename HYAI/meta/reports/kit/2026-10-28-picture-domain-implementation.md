---
id: report.kit.2026-10-28-picture-domain-implementation
title: "Реализация и подключение самодостаточного домена picture"
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
  - path: "AGENTS.md"
    why: "Пересборка входного файла агента после активации домена picture"
    profile: "project/maintainer"
  - path: "README.md"
    why: "Обновление сводной таблицы доменов и профилей каркаса"
    profile: "project/maintainer"
  - path: "HYAI/meta/project.md"
    why: "Регистрация активного домена picture и корневого каталога pictures/ в паспорте проекта"
    profile: "project/maintainer"
  - path: "pictures/.gitkeep"
    why: "Инициализация пустого продуктового корня pictures/ и его потоков briefs/, prompts/, stages/, assets/"
    profile: "picture/instant"
---

# Реализация и подключение самодостаточного домена `picture`

## Задача

По итогам фазы исследования ([`2026-10-28-picture-domain-analysis.md`](2026-10-28-picture-domain-analysis.md)) и явных решений владельца (`[А]`) по `Q-KIT-02..05` и ворот `HYAI-PERM-G05` требовалось спроектировать, создать и подключить в HYAI самодостаточный домен `picture` (префикс `PIC`, корень `pictures/`, без зависимости от других доменов и без правок Python-движков `HYAI/tools/*.py`, `KIT-POL-07`), закрепив обязательные правила владельца:
- генерация любого изображения всегда исключительно через промпт (`PIC-POL-01`) с динамическим подбором уточнений, особенно секции `negative` (`PIC-POL-02`);
- блокирующие стартовые ворота по 4 правилам безопасности (`NSFW`, `Copyright`, `Person`, `Violence`): пока все четыре не заданы пользователем явно, работа над задачей не ведётся (`PIC-SAF-01..05`);
- каноническая структура промпта «Каркас 5+3» (`subject`, `environment`, `lighting`, `camera`, `style` + `negative`, `weights`, `render_params`), порог `MinDetail`, моноязычность под модель (`en` по умолчанию) и корректный синтаксис весов (`PIC-PRM-01..05`);
- процессы `instant` (однопроходная генерация базового кадра) и `pipeline` (отдельные звенья для разметки, сцены, фона, персонажей/объектов, света и масок с поштучной VLM-приёмкой до сборки конечного кадра), а также `series` и `style-filter` (`PIC-WF-01..02`);
- обязательный цикл VLM-проверки (`Resolution`, `Aspect Ratio`, детекция артефактов рук/лиц/текста/геометрии, `Consistency` серии) до предела `Iteration Limit` (`PIC-POL-03`, `PIC-QA-01..05`);
- сохранение всех принятых промежуточных звеньев в `pictures/stages/` при немедленном удалении результатов неудачной промежуточной генерации (`PIC-POL-04`);
- применение фильтра стиля строго в самом конце, когда конечное базовое изображение `base-final` готово (`PIC-POL-05`).

## Что сделано

- Создан самодостаточный домен `HYAI/core/domains/picture/` (`status: review`, `HYAI-PERM-N05`):
  - `manifest.yaml`, `README.md`, `agents.md` — манифест домена (`root_paths: ["pictures"]`), навигация и краткий входной фрагмент для `AGENTS.md`;
  - `policy.md` — 23 нормативных правила `PIC-POL-01..06`, `PIC-SAF-01..05`, `PIC-PRM-01..05`, `PIC-WF-01..02`, `PIC-QA-01..05` с привязкой к проверкам (`HYAI-PROV-09`);
  - `authority.md` и `schema/authority.yaml` — уровни `visual-canon / brief / prompt / stage / none`;
  - `access.md` и `schema/access.yaml` — плоская модель `flat` (`public / internal / restricted`), правила `person_disclaimer` при выгрузке и пресет `Exports/public`;
  - `registry/documents.yaml` и `registry/README.md` — список `read_first` домена;
  - `workflows/{instant,pipeline,series,style-filter,README}.md` — регламенты и Mermaid-схемы однопроходной генерации, восьмизвенного конвейера `S1..S8`, серийной консистентности и финального фильтра стиля;
  - `templates/{task-safety-brief,prompt-spec,pipeline-manifest,series-anchor,asset-card,README}.md` — шаблоны ворот безопасности (`request`), промпта «Каркас 5+3», карты звеньев конвейера, эталона серии и паспорта готового ассета (`output`);
  - `profiles/{instant,pipeline,art-director,analysis}/{profile.yaml,README.md}` — четыре профиля с попарно непересекающимися `scope_primary` (`KIT-POL-08`).
- Подключены данные проекта в `HYAI/meta/` и корне репозитория:
  - `HYAI/meta/manifest.yaml` — добавлены домен `picture`, активная пара `picture/instant`, маршрут `"pictures/**": picture`, область отчётов `picture` и область решений `PIC`;
  - `HYAI/meta/schema/rule-ids.yaml` и `HYAI/meta/schema/domains/picture.yaml` — зарегистрирован владелец `PIC` с классами `[POL, SAF, PRM, WF, QA, INV]` и frontmatter-оверлей `picture`;
  - `HYAI/meta/lint/terms/picture.json` — 7 машинных правил (`pic.unset-safety-placeholder`, `pic.empty-negative-prompt`, `pic.filler-quality-tags`, `pic.mixed-weight-syntax`, `pic.rejected-artifact-stored`, `pic.premature-style-on-base`, `pic.todo-without-owner`);
  - `HYAI/meta/architecture/picture.md` (`PIC-INV-01..04`), `HYAI/meta/terminology/picture.md`, `HYAI/meta/questions/picture.md`, `HYAI/meta/decisions/picture/README.md`, `HYAI/meta/reports/picture/README.md`;
  - `HYAI/meta/decisions/kit/KIT-0003-picture-domain.md` и закрытие `Q-KIT-02..05` в `HYAI/meta/questions/kit.md`;
  - обновлены все родительские индексы (`HYAI/core/domains/README.md`, `HYAI/meta/project.md`, `HYAI/meta/architecture.md`, `HYAI/meta/architecture/README.md`, `HYAI/meta/schema/domains/README.md`, `HYAI/meta/terminology.md`, `HYAI/meta/terminology/README.md`, `HYAI/meta/questions.md`, `HYAI/meta/questions/README.md`, `HYAI/meta/lint/README.md`, `HYAI/meta/lint/terms/README.md`, `HYAI/meta/decisions/README.md`, `HYAI/meta/decisions/kit/README.md`, `HYAI/meta/reports/README.md`, `HYAI/meta/reports/kit/README.md`, `README.md`);
  - создан продуктовый каркас `pictures/{briefs,prompts,stages,assets}/.gitkeep` и пересобран `AGENTS.md`.
- Файлы `HYAI/tools/*.py` не изменялись (`0` строк диффа в движках, `KIT-POL-07`).

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| сборка `AGENTS.md` | `python3 HYAI/tools/assemble_agents.py --check` | `rc=0`, дрейфа нет |
| конвейер каркаса и домена `picture` | `python3 HYAI/tools/run_checks.py --skip-project` | `rc=0`, все проверки пройдены |
| строгий линт терминов | `python3 HYAI/tools/lint_terms.py --strict` | `rc=0`, 0 предупреждений |
| контуры и пресет выгрузки `picture` | `python3 HYAI/tools/lint_scopes.py --domain picture && python3 HYAI/tools/build_export.py --domain picture --preset public --dry-run` | `rc=0` |
| модульные тесты движков | `python3 -m unittest discover -s HYAI/tools/tests` | `rc=0`, 68 тестов ОК |
| пробелы и переносы Git | `git diff --check` | `rc=0`, замечаний нет |

## Открытые вопросы

- По созданию домена `picture` открытых вопросов нет (`Q-KIT-02..05` закрыты решением `KIT-0003`).
- Общекаркасный вопрос `Q-KIT-01` в `HYAI/meta/questions/kit.md` остаётся в прежнем статусе `open` (не входит в рамку этой задачи).
