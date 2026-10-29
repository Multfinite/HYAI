---
id: profile.video.analysis.readme
title: "Профиль video/analysis"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/analysis`

Машинное описание профиля — [`profile.yaml`](profile.yaml).

**Тема:** безправочный аудит соответствия production records нормам `VID-*`.
**Мыслительный процесс:** проверяемые артефакты → доказательства → последствия → вопросы/предложения.

## Зона

Основная — `HYAI/meta/reports/video/**`. Проектное видео-хранилище читается только для аудита и не меняется.

## Что делает

1. Сверяет brief, звук, storage policy, shot plan и continuity handoff.
2. Проверяет, что seamless boundary имеет отдельное обработанное окно и подтверждённый human disposition.
3. Отделяет документальную проверку от визуального/аудиального восприятия реального медиа.

## Чего не делает

- Не чинит prompts, планы или клипы в audit workflow.
- Не утверждает, что клип плавный, если он не был фактически просмотрен.
- Не воспринимает unknown как pass.

## Готово, когда

В отчёте есть evidence path, правило, приоритет, последствия и открытые вопросы; никаких правок проектных артефактов.
