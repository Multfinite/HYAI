---
id: decision.project.P-0003
title: "Разделение владения keyframe-изображениями между picture и video"
type: decision
status: review
authority: contract
visibility: internal
scope: project
affects_domains: [picture, video]
affects:
  - "HYAI/core/domains/video/policy.md"
  - "HYAI/core/domains/video/workflows/continuity.md"
  - "HYAI/core/domains/video/templates/continuity-ledger.md"
  - "HYAI/meta/architecture/video.md"
  - "HYAI/meta/manifest.yaml"
supersedes: null
---

# P-0003. Разделение владения keyframe-изображениями между `picture` и `video`

## Решение

1. Домен `picture` остаётся владельцем растровых reference assets, storyboard/keyframe изображений и визуальных серий по собственным правилам и в собственном `root_paths`.
2. Домен `video` владеет временным планом, continuity state, handoff records, сегментами, аудио/монтажной документацией и seam-window records в отдельном `<video_root>`.
3. Видеопроект ссылается на принятую картинку по stable `picture` asset ID/URI, `sha256`, статусу и роли (`start_ref`, `end_ref`, `continuity_ref`). Дублировать бинарник или присваивать ownership `video` нельзя.
4. Наличие статического I2V reference не считается передачей видеодвижения. На каждой задаче агент спрашивает пользователя, как выбранное им средство получает continuity context — last frame, frame tail/previous clip, другой reference или независимые сегменты — и сохраняет фактически применённый режим.
5. Междоменный переход `video` ↔ `picture` проговаривается по общему процессу ядра `P-0002`; домены не копируют центральное правило озвучивания.

## Почему

`picture` уже имеет отдельные правила, root и процесс связанных изображений. `video` добавляет собственную временную нормативность: действие, длительность, начальное/конечное состояние shots и монтажные границы. Разделение binary assets от temporal records избегает двух владельцев одного каталога и не дублирует picture QA (`KIT-POL-06`, `VID-POL-08`).

## Последствия

- Создание/review изображений проходит через активный профиль `picture`, а результат переносится в video plan ссылкой и hash.
- Если нужный `picture` asset не принят или недоступен, зависимый видеошаг блокируется.
- Данный контракт не предписывает единый last-frame method всем моделям; способ continuity подтверждается пользователем для конкретной задачи.
