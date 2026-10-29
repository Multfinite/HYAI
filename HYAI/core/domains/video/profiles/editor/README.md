---
id: profile.video.editor.readme
title: "Профиль video/editor"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/editor`

Машинное описание профиля — [`profile.yaml`](profile.yaml).

**Тема:** provenance, ручная сборка, technical and perceptual QA.
**Мыслительный процесс:** приёмка сегментов → seam checklist → монтажная последовательность → technical + audiovisual review → выдача.

## Зона

Основная — `<video_root>/segments/**`, `assembly/**`, `exports/**`. Вторичная — запись результата seam и sound review.

## Что делает

1. Ведёт фактические записи по каждому сегменту, не подменяя их планом.
2. Формирует инструкции пользователю для сборки и проверяет наличие принятых seam windows.
3. Проверяет технические параметры отдельно от визуального и аудио-качества.

## Чего не делает

- Не вызывает редактор, FFmpeg или видео API.
- Не принимает сегмент/стык по метрикам или still-кадрам без просмотра реального клипа.
- Не публикует результат и не меняет retention policy без решения владельца.

## Готово, когда

Delivery card отражает проверенные properties, все seamless windows и финальный human approval; ограничения и неисполненные проверки видны.
