---
id: decision.kit.KIT-0003
title: "Самодостаточный домен picture: промптовая генерация изображений, конвейер звеньев и изоляция корня данных"
type: decision
status: review
authority: contract
visibility: internal
scope: kit
affects_domains: [kit]
affects:
  - "HYAI/core/domains/picture/manifest.yaml"
  - "HYAI/core/domains/picture/pictures/.gitkeep"
  - "HYAI/core/domains/picture/policy.md"
  - "HYAI/core/domains/picture/authority.md"
  - "HYAI/core/domains/picture/access.md"
  - "HYAI/meta/manifest.yaml"
  - "HYAI/meta/schema/rule-ids.yaml"
  - "HYAI/meta/schema/domains/picture.yaml"
  - "HYAI/meta/lint/terms/picture.json"
  - "HYAI/meta/architecture/picture.md"
  - "HYAI/tools/_shared.py"
  - "HYAI/tools/check_domains.py"
  - "HYAI/tools/check_manifest.py"
  - "HYAI/tools/check_indexes.py"
  - "AGENTS.md"
supersedes: null
---

# KIT-0003. Самодостаточный домен `picture`

## Решение

В каркас HYAI вводится самодостаточный домен `picture` (не вложенный в `narrative`, префикс правил и решений `PIC`, плоская модель контуров `flat`: `public / internal / restricted`, уровни нормативности `visual-canon / brief / prompt / stage / none`, профили `instant`, `pipeline`, `art-director`, `analysis` с активной парой `picture/instant`).

Рабочий корень данных домена (`<picture_root>`) задаётся полем `root_paths` манифеста активного домена:
- в самом репозитории HYAI это `HYAI/core/domains/picture/pictures` (чтобы корень репозитория не замусоривался каталогом `./pictures`);
- во внешнем проекте, подключающем HYAI как подмодуль, проект определяет собственный `<picture_root>` вне подмодуля через проектный манифест активного домена с `includes: ["HYAI/core/domains/picture/manifest.yaml"]` (либо `active[].root_paths`) и `path_map`, а универсальные движки HYAI ребазируют глобы профилей/линтера/схем и блокируют запись данных активного домена внутрь подмодуля (`PIC-POL-06`, `PIC-INV-05`).

Норма работы домена включает:
1. Блокирующие стартовые ворота безопасности `G0-SAF` (`PIC-SAF-01..05`): пока пользователь явно не задал `NSFW`, `Copyright`, `Person`, `Violence`, работа над задачей не ведётся.
2. Генерацию любого кадра, промежуточного звена и стилевого прохода строго через моноязычный промпт канонической структуры «Каркас 5+3» (`subject`, `environment`, `lighting`, `camera`, `style` + динамический `negative`, `weights`, `render_params`) с контролем `MinDetail` (`PIC-POL-01..02`, `PIC-PRM-01..05`).
3. Разделение однопроходного процесса `instant` и многозвенного `pipeline` (`layout`, `scene-block`, `background`, `subjects`, `lighting`, `masks-guides`, `base-final`, `style-final`) с обязательной VLM-приёмкой каждого шага (`Resolution`, `Aspect Ratio`, артефакты рук/лиц/текста/геометрии, `Consistency`) до предела `Iteration Limit` (`PIC-WF-01..02`, `PIC-QA-01..05`).
4. Обязательное сохранение принятых промежуточных звеньев в `<picture_root>/stages/` при немедленном удалении неудачных промежуточных попыток (`PIC-POL-04`) и наложение фильтра стиля исключительно после готовности конечного базового изображения `base-final` (`PIC-POL-05`).

## Почему

Генерация изображений имеет собственные инварианты провенанса, мультимодальной приёмки, безопасности и поэтапной сборки сцены, не сводимые к `narrative` (`KIT-POL-05`). Внутри самого репозитория HYAI рабочий каталог уместен внутри домена (`HYAI/core/domains/picture/pictures/`), тогда как при установке HYAI подмодулем правила и шаблоны обязаны опираться на `<picture_root>` активного домена проекта, никогда не направляя проектные файлы внутрь подмодуля.

## Последствия

- Любая задача генерации изображений получает след «бриф безопасности → промпт 5+3 → принятые звенья `<picture_root>/stages/` → стилизованный ассет `<picture_root>/assets/`».
- Корень репозитория HYAI остаётся чистым, а внешние проекты (например, `Eidolon---Pherin` с `meta/hyai/domains/picture/pictures/`) переопределяют `root_paths` декларативно без копирования профилей и без риска записи внутрь подмодуля.
- Соблюдение проверяется связкой `check_domains.py`, `check_manifest.py`, `check_indexes.py`, `check_rules.py`, `frontmatter.py --check`, `lint_terms.py --domain picture` и регрессионными тестами `HYAI/tools/tests/test_domains.py`.
