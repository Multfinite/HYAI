---
id: template.picture.pipeline-manifest
title: "Шаблон карты промежуточных звеньев конвейера picture/pipeline"
type: template
status: review
authority: none
visibility: internal
version: "1.1"
updated: "2026-11-09"
template: true
template_kind: output
---

# Карта промежуточных звеньев конвейера (`pipeline-manifest`)

Создаётся в `<picture_root>/stages/<slug>/pipeline-manifest.md` при работе по процессу [`../workflows/pipeline.md`](../workflows/pipeline.md) (`PIC-POL-04`, `PIC-WF-01..02`), где `<picture_root>` — `root_paths` манифеста активного домена `picture` (вне подмодуля HYAI для внешних проектов — `PIC-POL-06`).

**Если данных нет:** если звено не требуется по геометрии сцены (например, `S1 layout` или `S6 masks-guides`), оно помечается статусом `skipped-by-design` с коротким обоснованием; обязательные звенья (`S3`, `S4`, `S7`, `S7C` при `concept_method: monochrome-sketch + color-pass` (`PIC-POL-18`) и `S8` при наличии целевого стиля) пропускать нельзя.

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

- **Бриф:** `<picture_root>/briefs/<slug>.md`
- **Лимит попыток на звено (`iteration_limit`):** `<N>`

## Реестр принятых звеньев (`S1..S8`)

| Звено | Статус | Промпт звена (`PIC-POL-01`) | Принятый файл звена (`PIC-POL-04`) | Попытки (`k/N`) | Сводка VLM-проверки | Отбракованные дубли |
| --- | --- | --- | --- | --- | --- | --- |
| `S1 layout` | `accepted` / `skipped-by-design` | `<picture_root>/prompts/<slug>-s1.md` | `<picture_root>/stages/<slug>/s1-layout.png` | `1/5` | пропорции и силуэты в норме | удалены (`0` в хранилище) |
| `S2 scene-block` | `accepted` / `skipped-by-design` | `<picture_root>/prompts/<slug>-s2.md` | `<picture_root>/stages/<slug>/s2-scene.png` | `1/5` | перспектива и масштаб согласованы | удалены (`0` в хранилище) |
| `S3 background` | `accepted` | `<picture_root>/prompts/<slug>-s3.md` | `<picture_root>/stages/<slug>/s3-background.png` | `2/5` | чистая среда без паразитных фигур | 1 дубль удалён |
| `S4 subjects` | `accepted` | `<picture_root>/prompts/<slug>-s4.md` | `<picture_root>/stages/<slug>/s4-subject-01.png` | `2/5` | руки, лицо и костюм без артефактов | 1 дубль удалён |
| `S5 lighting` | `accepted` | `<picture_root>/prompts/<slug>-s5.md` | `<picture_root>/stages/<slug>/s5-lighting.png` | `1/5` | единый вектор ключевого и контрового света | удалены (`0` в хранилище) |
| `S6 masks-guides` | `accepted` / `skipped-by-design` | `<picture_root>/prompts/<slug>-s6.md` | `<picture_root>/stages/<slug>/s6-masks.png` | `1/5` | точные зоны опоры и перекрытий | удалены (`0` в хранилище) |
| `S7 base-final` | `accepted` | `<picture_root>/prompts/<slug>-s7-base.md` | `<picture_root>/stages/<slug>/s7-base-final.png` | `2/5` | полная базовая сцена без стилизации принята | 1 дубль удалён |
| `S7C color-pass` | `accepted` / `skipped-by-design` | `<picture_root>/prompts/<slug>-s7c-color.md` | `<picture_root>/stages/<slug>/s7c-color-final.png` | `1/5` | раскраска принятого `S7` без потери композиции, лиц и предметов; `skipped-by-design`, если `concept_method` — не скетч | удалены (`0` в хранилище) |
| `S8 style-final` | `accepted` | `<picture_root>/prompts/<slug>-s8-style.md` | `<picture_root>/assets/<slug>.png` | `1/5` | целевой стиль наложен без потери деталей `S7C` (или `S7`) | удалены (`0` в хранилище) |
````

## Дополнение при локальной ремедиации (CEPI)

Связать этот документ с [cepi-manifest](cepi-manifest.md) и выполнить
[CEPI](../workflows/crop-edit-paste-integrate.md). Дополнительные поля:
`source_sha256`, `crop_box_xyxy`, `mask_sha256`, `protected_regions`, `eye_lock`,
`generation_tool`, `prompt_verbatim`, `prompt_provenance`, `native_dimensions`,
`export_dimensions`, `resampling`, `integrate_mode`, `integrate_calls`,
`audit_evidence`, `owner_approval`, `delivery_mode`, `download_sha256`.
Не подставлять реконструированный промпт как дословный лог вызова и не переносить
нулевой diff композита на полнокадровый финал (`PIC-QA-12..13`).
