---
id: domain.video.data.readme
title: "Рабочие данные домена video"
type: meta
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `<video_root>`

Корень — `HYAI/core/domains/video/videos/` в самом HYAI и путь проекта-владельца во внешней установке подмодулем. Project media размещаются только по заранее утверждённой project/session storage policy (`VID-POL-03`); бинарные клипы не добавлять в Git по умолчанию.

| Каталог | Содержимое |
| --- | --- |
| `briefs/` | Задача, аудио-ответ, delivery и storage gates |
| `plans/` | Timeline и storyboard shot plan |
| `continuity/` | Канонические инварианты и состояния shot boundaries |
| `transitions/` | Seam-window records и инструкции обработки стыков |
| `sound/` | Sound plan, source references, audio timing and QA |
| `segments/` | Sidecar-record каждого внешне сгенерированного segment |
| `assembly/` | Последовательность, монтажная карта и финальный QC |
| `exports/` | Только одобренная поставка/ссылка на согласованное хранилище |

Изображения keyframes принадлежат `picture`; в этой структуре указываются только ID/URI/hash и назначение референса.
