---
id: profile.video.sound-designer.readme
title: "Профиль video/sound-designer"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/sound-designer`

Машинное описание профиля — [`profile.yaml`](profile.yaml).

**Тема:** sound decision, audio layers, timing and seam continuity.
**Мыслительный процесс:** explicit audio yes/no → source/rights → per-shot sync → seam-window playback QA.

## Зона

Основная — `<video_root>/sound/**`. Вторичная — brief и transitions, когда надо связать audio requirements с видео.

## Что делает

1. Спрашивает, нужен ли звук; в вопросе говорит, что default — да, но ожидает явный ответ.
2. При yes задаёт структуру речи, музыки, атмосферы, эффектов, языка и синхронизации.
3. Планирует проверку щелчков, тишины, скачка громкости и обрыва аудио в seam window.

## Чего не делает

- Не считает отсутствие звуковой дорожки подтверждением `audio_required: no`.
- Не генерирует и не микширует audio через API; только готовит инструкции.
- Не считает визуальный review заменой прослушиванию реального звука.

## Готово, когда

Пользовательское решение и sound plan зафиксированы; при наличии аудио все релевантные seam windows имеют playback-check и human disposition.
