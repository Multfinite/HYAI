---
id: decision.kit.KIT-0003
title: "Самодостаточный домен picture: промптовая генерация изображений, конвейер звеньев и отложенный стиль"
type: decision
status: review
authority: contract
visibility: internal
scope: kit
affects_domains: [kit]
affects:
  - "HYAI/core/domains/picture/manifest.yaml"
  - "HYAI/core/domains/picture/policy.md"
  - "HYAI/core/domains/picture/authority.md"
  - "HYAI/core/domains/picture/access.md"
  - "HYAI/meta/manifest.yaml"
  - "HYAI/meta/schema/rule-ids.yaml"
  - "HYAI/meta/schema/domains/picture.yaml"
  - "HYAI/meta/lint/terms/picture.json"
  - "HYAI/meta/architecture/picture.md"
  - "AGENTS.md"
supersedes: null
---

# KIT-0003. Самодостаточный домен `picture`

## Решение

В каркас HYAI вводится самодостаточный домен `picture` (префикс правил и решений `PIC`, продуктовый корень `pictures/`, плоская модель контуров `flat`: `public / internal / restricted`, уровни нормативности `visual-canon / brief / prompt / stage / none`, профили `instant`, `pipeline`, `art-director`, `analysis` с активной парой `picture/instant`) без зависимости от других предметных доменов и без правок Python-движков (`KIT-POL-07`).

Норма работы домена включает:
1. Блокирующие стартовые ворота безопасности `G0-SAF` (`PIC-SAF-01..05`): пока пользователь явно не задал `NSFW`, `Copyright`, `Person`, `Violence`, работа над задачей не ведётся.
2. Генерацию любого кадра, промежуточного звена и стилевого прохода строго через моноязычный промпт канонической структуры «Каркас 5+3» (`subject`, `environment`, `lighting`, `camera`, `style` + динамический `negative`, `weights`, `render_params`) с контролем `MinDetail` (`PIC-POL-01..02`, `PIC-PRM-01..05`).
3. Разделение однопроходного процесса `instant` и многозвенного `pipeline` (`layout`, `scene-block`, `background`, `subjects`, `lighting`, `masks-guides`, `base-final`, `style-final`) с обязательной VLM-приёмкой каждого шага (`Resolution`, `Aspect Ratio`, артефакты рук/лиц/текста/геометрии, `Consistency`) до предела `Iteration Limit` (`PIC-WF-01..02`, `PIC-QA-01..05`).
4. Обязательное сохранение принятых промежуточных звеньев в `pictures/stages/` при немедленном удалении неудачных промежуточных попыток (`PIC-POL-04`) и наложение фильтра стиля исключительно после готовности конечного базового изображения `base-final` (`PIC-POL-05`).

## Почему

Генерация изображений имеет собственные инварианты провенанса, мультимодальной приёмки, лицензионно-этической безопасности и декомпозиции сцены на слои, не сводимые к коду, текстовой документации или литературной прозе (`KIT-POL-05`). Ранняя стилизация маскирует дефекты анатомии и перспективы, а хранение бракованных дублей засоряет репозиторий и размывает источник истины.

## Последствия

- Любая задача генерации изображений получает воспроизводимый след «бриф безопасности → промпт 5+3 → принятые звенья `stages/` → стилизованный ассет `assets/`».
- Невозможны старт задачи без явно заданных пользователем 4 правил безопасности, генерация в обход промпта, хранение отбракованных рендеров и применение фильтра стиля до готовности `base-final`.
- Соблюдение проверяется связкой `check_domains.py`, `check_manifest.py`, `check_rules.py`, `frontmatter.py --check`, `lint_terms.py --domain picture` и протоколами VLM-приёмки в `asset-card.md` (`enforced: prose-only` для визуальной экспертизы).
