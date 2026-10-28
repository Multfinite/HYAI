---
id: template.picture.pipeline-manifest
title: "Шаблон карты промежуточных звеньев конвейера picture/pipeline"
type: template
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-28"
template: true
template_kind: output
---

# Карта промежуточных звеньев конвейера (`pipeline-manifest`)

Создаётся в `pictures/stages/<slug>/pipeline-manifest.md` при работе по процессу [`../workflows/pipeline.md`](../workflows/pipeline.md) (`PIC-POL-04`, `PIC-WF-01..02`).

**Если данных нет:** если звено не требуется по геометрии сцены (например, `S1 layout` или `S6 masks-guides`), оно помечается статусом `skipped-by-design` с коротким обоснованием; обязательные звенья (`S3`, `S4`, `S7` и `S8` при наличии целевого стиля) пропускать нельзя.

````markdown
---
id: picture.stage.<slug>.manifest
title: "Конвейер звеньев: <название сцены>"
type: stage-manifest
status: review
authority: stage
visibility: internal
---

# Конвейер звеньев: <название сцены>

- **Бриф:** `pictures/briefs/<slug>.md`
- **Лимит попыток на звено (`iteration_limit`):** `<N>`

## Реестр принятых звеньев (`S1..S8`)

| Звено | Статус | Промпт звена (`PIC-POL-01`) | Принятый файл звена (`PIC-POL-04`) | Попытки (`k/N`) | Сводка VLM-проверки | Отбракованные дубли |
| --- | --- | --- | --- | --- | --- | --- |
| `S1 layout` | `accepted` / `skipped-by-design` | `pictures/prompts/<slug>-s1.md` | `pictures/stages/<slug>/s1-layout.png` | `1/5` | пропорции и силуэты в норме | удалены (`0` в хранилище) |
| `S2 scene-block` | `accepted` / `skipped-by-design` | `pictures/prompts/<slug>-s2.md` | `pictures/stages/<slug>/s2-scene.png` | `1/5` | перспектива и масштаб согласованы | удалены (`0` в хранилище) |
| `S3 background` | `accepted` | `pictures/prompts/<slug>-s3.md` | `pictures/stages/<slug>/s3-background.png` | `2/5` | чистая среда без паразитных фигур | 1 дубль удалён |
| `S4 subjects` | `accepted` | `pictures/prompts/<slug>-s4.md` | `pictures/stages/<slug>/s4-subject-01.png` | `2/5` | руки, лицо и костюм без артефактов | 1 дубль удалён |
| `S5 lighting` | `accepted` | `pictures/prompts/<slug>-s5.md` | `pictures/stages/<slug>/s5-lighting.png` | `1/5` | единый вектор ключевого и контрового света | удалены (`0` в хранилище) |
| `S6 masks-guides` | `accepted` / `skipped-by-design` | `pictures/prompts/<slug>-s6.md` | `pictures/stages/<slug>/s6-masks.png` | `1/5` | точные зоны опоры и перекрытий | удалены (`0` в хранилище) |
| `S7 base-final` | `accepted` | `pictures/prompts/<slug>-s7-base.md` | `pictures/stages/<slug>/s7-base-final.png` | `2/5` | полная базовая сцена без стилизации принята | 1 дубль удалён |
| `S8 style-final` | `accepted` | `pictures/prompts/<slug>-s8-style.md` | `pictures/assets/<slug>.png` | `1/5` | целевой стиль наложен без потери деталей `S7` | удалены (`0` в хранилище) |
````
