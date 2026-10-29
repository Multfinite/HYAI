---
id: template.video.video-brief
title: "Brief видеозадачи"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
template: true
template_kind: request
---

# Video brief — `<project_slug>`

## Задача и результат
- Goal / audience:
- Format, aspect ratio, target resolution/FPS:
- Runtime and delivery target:
- Story/source material and right to use:
- Acceptable retry limit / budget, if applicable:

## Обязательные подтверждения до media
- **Нужен ли звук?** По умолчанию предполагается `yes`; пользователь должен явно ответить `yes/no`: `[?]`
- **Где хранятся медиа?** Project-level policy `[...]` или session policy `[...]`; доступ, срок хранения/удаления, backup, отклонённые клипы и аудио: `[?]`
- **Как следующий segment получает continuity context?** Последний кадр / несколько конечных кадров или видеохвост / отдельный picture reference / независимые сегменты / иной способ: `[?]`
- Выбранное пользователем средство/model/mode и подтверждённые им ограничения:
- Human approver and approval gates:

## Критерии
- Visual continuity:
- Audio continuity / `not applicable` with explicit `audio_required: no`:
- Seamless boundaries and unacceptable seam defects:
- Technical output requirements:

Без явных ответов на blocking fields не переходить к генерации (`VID-POL-01..04`).
