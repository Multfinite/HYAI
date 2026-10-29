---
id: template.picture.asset-card
title: "Шаблон паспорта готового изображения и протокола VLM-приёмки"
type: template
status: review
authority: none
visibility: internal
version: "1.1"
updated: "2026-10-29"
template: true
template_kind: output
---

# Паспорт готового изображения (`asset-card`)

Создаётся в `<picture_root>/assets/<slug>.md` рядом с финальным изображением (или ссылкой на внешнее хранилище при размере > 10 МБ, `HYAI-ART-19`), где `<picture_root>` — `root_paths` манифеста активного домена `picture` (вне подмодуля HYAI для внешних проектов — `PIC-POL-06`).

**Если данных нет:** карточка с пустой отметкой по любой из осей безопасности (`PIC-SAF-01..05`) или VLM-проверки качества (`PIC-QA-01..05`) приёмку не проходит; недостающая проверка выполняется до закрытия задачи.

````markdown
---
id: picture.asset.<slug>
title: "Ассет: <название изображения>"
type: asset-card
status: review
authority: stage
visibility: internal
---

# Ассет: <название изображения>

## 1. Файл и провенанс

- **Путь к финальному файлу (или URI внешнего хранилища):** `<picture_root>/assets/<slug>.png`
- **`sha256`:** `<хэш файла>`
- **Рабочий процесс:** `picture/instant` | `picture/pipeline` | `picture/series`
- **Бриф безопасности:** `<picture_root>/briefs/<slug>.md`
- **Принятый базовый кадр до фильтра стиля (`PIC-POL-04..05`):** `<picture_root>/stages/<slug>/<base-final>.png`
- **Карта промежуточных звеньев (для `pipeline`):** `<picture_root>/stages/<slug>/pipeline-manifest.md`
- **Промпт базового кадра (`PIC-POL-01`):** `<picture_root>/prompts/<slug>-base.md`
- **Промпт фильтра стиля (`PIC-POL-05`):** `<picture_root>/prompts/<slug>-style.md` (или `none-by-brief`)
- **Эталон серии (`PIC-QA-04`):** `<<picture_root>/briefs/<series>-anchor.md или "одиночный кадр">`
- **Канон окружения кадра (`PIC-ENV-01`):** `<env_canon_source>`, якоря: `<env_anchor_ids>`, `env_ok`: `<true / false>`
- **Тип синтетического источника (IPTC):** `trainedAlgorithmicMedia` | `compositeWithTrainedAlgorithmicMedia`

## 2. Контроль безопасности и публичных оговорок (`PIC-SAF-01..05`)

- `safety_nsfw`: `<значение [А]>` — соблюдено (`nsfw_clear: true`)
- `safety_copyright`: `<значение [А]>` — соблюдено (`copyright_clear: true`)
- `safety_person`: `<значение [А]>` — `person_disclaimer`: `<явный текст оговорки или "не применимо">`
- `safety_violence`: `<значение [А]>` — соблюдено (`violence_clear: true`)

## 3. Протокол проверки качества (`PIC-QA-01..05`)

| Правило | Порог брифа | Фактический результат | Вердикт |
| --- | --- | --- | --- |
| `PIC-QA-01` `Resolution` | `<min_resolution>` | `<WxH>` | `pass` |
| `PIC-QA-02` `Aspect Ratio` | `<allowed_aspect_ratios>` | `<W:H>` | `pass` |
| `PIC-QA-03` `Artifact: hands` | без лишних/сломанных пальцев и сгибов | `<результат осмотра VLM>` | `pass` |
| `PIC-QA-03` `Artifact: faces` | симметрия черт, чистые зрачки и мимика | `<результат осмотра VLM>` | `pass` |
| `PIC-QA-03` `Artifact: text` | точные глифы либо отсутствие псевдотекста/водяных знаков | `<результат осмотра VLM>` | `pass` |
| `PIC-QA-03` `Artifact: geometry` | перспектива, опоры, контактные тени, отсутствие швов | `<результат осмотра VLM>` | `pass` |
| `PIC-QA-04` `Consistency` | совпадение с `series-anchor` | `<результат парной сверки или n/a>` | `pass` |
| `PIC-QA-05` `Iteration Limit` | `<= <iteration_limit>` | `база: <k1/N>, стиль: <k2/N>; брак удалён` | `pass` |
| `PIC-QA-06` `Environment` | пять осей `PIC-ENV-02` сверены с якорями канона | `<свет звезды / флора / небо / небесные тела / тёплые источники: совпало или not applicable>` | `pass` |
````
