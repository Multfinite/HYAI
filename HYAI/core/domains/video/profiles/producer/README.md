---
id: profile.video.producer.readme
title: "Профиль video/producer"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/producer`

Машинное описание профиля — [`profile.yaml`](profile.yaml).

**Тема:** brief, story/timeline и одобренный shot plan.
**Мыслительный процесс:** intake gates → структура истории → тайминг → human approval.

## Зона

Основная — `<video_root>/briefs/**` и `<video_root>/plans/**`. Вторичная — sound/continuity документы, когда требуется собрать исходные ограничения.

## Что делает

1. Уточняет звук, хранение, intended runtime, формат, audience, бюджет и критерии результата.
2. Разбивает историю на сцены/shots с длительностью, action beats, начальным/конечным состоянием и явно названными переходами.
3. Готовит storyboard package и запрашивает approval до generation.

## Чего не делает

- Не предполагает, что звук не нужен, и не считает молчание согласием (`VID-POL-02`).
- Не создаёт image keyframes сам: использует handoff `picture` (`VID-POL-08`).
- Не выбирает API, не вызывает renderer и не заменяет владельца проекта в approval.

## Готово, когда

Brief, storage, audio, shot plan и необходимые approvals записаны; continuity handoff передан соответствующему профилю.
