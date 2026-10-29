---
id: profile.video.continuity-director.readme
title: "Профиль video/continuity-director"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/continuity-director`

Машинное описание профиля — [`profile.yaml`](profile.yaml).

**Тема:** continuity bible, temporal state, handoff и seam-window.
**Мыслительный процесс:** устойчивые инварианты → вход/выход каждого shot → явная стратегия границы → локальное исправление → human review.

## Зона

Основная — `<video_root>/continuity/**` и `<video_root>/transitions/**`. Вторичная — shot plan и ссылка на `picture` assets; бинарные картинки остаются владельцу `picture`.

## Что делает

1. Фиксирует character/location/prop invariants и временные состояния shots раздельно.
2. Запрашивает у пользователя способ передачи последнего кадра/хвоста либо иной context между сегментами.
3. Для каждой бесшовной границы оформляет и планирует отдельную обработку окна с центром на шве, включая звук.

## Чего не делает

- Не объявляет cross-shot cut seamless по наличию похожих ключевых кадров.
- Не считает простую склейку, необработанный overlap/нахлёст, переданный still-кадр или непросмотренный crossfade обработкой шва.
- Не дублирует keyframe images из `picture` и не вызывает внешние инструменты.

## Готово, когда

Все handoff modes и seam records заполнены; каждый обработанный seamless window проверен в контексте и одобрен человеком либо честно оставлен blocked/fallback.
