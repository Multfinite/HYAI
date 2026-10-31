---
id: report.kit.2026-11-01-cartography-domain-implementation
title: "Создание домена cartography для планетарных атласов"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
authority: contract
visibility: internal
status: review
date: "2026-11-01"
workflow: kit/domain-authoring
cross_scope:
  - path: "HYAI/core/domains/cartography/**"
    why: "создан самостоятельный домен и его atlas data roots"
  - path: "HYAI/core/domains/narrative/**"
    why: "закреплена ссылка на structured canon по P-0005"
  - path: "HYAI/meta/manifest.yaml"
    why: "домен и active profile зарегистрированы в метаданных"
decisions: [KIT-0006, P-0005]
---

## Задача

Создать самостоятельный домен `cartography` для структурированных планетарных атласов, геопривязанных слоёв и векторных карт; определить границу с `narrative`, подготовить технологические рекомендации и зарегистрировать домен в метаданных HYAI.

## Что сделано

- Добавлен домен с authority/access, 14 правилами `CART-POL-*`, четырьмя профилями (`cartographer`, `planetary-modeler`, `atlas-editor`, `analysis`), пятью workflow, шаблонами записей звёздной системы/тела/слоя/климата/map spec и деревом `atlases/`.
- Зафиксировано в `P-0005`: `cartography` владеет структурированными планетарными/пространственными и политическими данными; `narrative` хранит прозу и ссылается на stable IDs.
- Зафиксировано в `KIT-0006`: map files/exports остаются векторными; интерактивный viewport может временно отображать векторные слои с экранной растеризацией и не сохраняется как raster deliverable.
- Зарегистрированы `cartography/cartographer`, decision scope `CART`, rule owner `CART`, schema overlay, terms lint, architecture/terminology/questions и необходимые индексы.

## Исследование инструментов

| Инструмент | Роль в рекомендации | Ограничение |
| --- | --- | --- |
| [QGIS](https://github.com/qgis/QGIS) | Векторные геоданные, CRS-инструменты и SVG export | Произвольные планетные эллипсоиды/CRS требуют проверки |
| [Inkscape](https://github.com/inkscape/inkscape) | Редакторская работа с SVG | Не является GIS-источником истины для CRS |
| [CesiumJS](https://github.com/CesiumGS/cesium) | Кандидат на интерактивный 3D-глобус и просмотр векторных слоёв | Экранный renderer не является научной моделью; custom planetary CRS/временные слои тестируются прототипом |
| [MapLibre globe guide](https://github.com/maplibre/maplibre-gl-js/blob/main/developer-guides/globe.md) | Сравнительная альтернатива для vector-layer/globe сценариев | Не выбран универсальным движком для произвольных планет |
| [CesiumJS Mars ellipsoid PR](https://github.com/CesiumGS/cesium/pull/12828) | Иллюстрация planetary ellipsoid/trajectory направления | Наличие примера не подтверждает поддержку любой пользовательской CRS |

## Проверка

- Созданы frontmatter/schema/policy/profile/workflow/template документы и зарегистрированы в мета-индексах.
- Lint rules нацелены на растровые map formats, незаполненные body/CRS и unset/non-Köppen climate scheme; они не заменяют GIS topology/scientific validation.
- `AGENTS.md` обновлён только через `assemble_agents.py --write`; `assemble_agents.py --check` прошёл.
- `run_checks.py --skip-project`: 26 проверок, 0 ошибок; `unittest discover`: 72 теста, успешно.
- PyYAML установлен только во временное окружение `/tmp/hyai-cartography-validate`; зависимости проекта не менялись.
- QGIS/CesiumJS prototype на конкретной планете не запускался, так как целевое тело/CRS ещё не выбраны (`Q-CART-01`); runtime-библиотеки и интеграции не добавлялись.

## Открытые вопросы

- [`Q-CART-01`](../../questions/cartography.md): какое тело/эллипсоид/CRS и временной набор использовать для первого прототипа QGIS и интерактивного renderer. До выбора и теста универсальная поддержка не заявляется.
- Совместимость конкретных planetary CRS с SVG export и интерактивным CesiumJS viewport остаётся на проверку прототипом.
