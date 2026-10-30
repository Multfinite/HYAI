---
id: domain.video.templates.readme
title: "Домен video: шаблоны"
type: meta
status: review
authority: none
visibility: internal
version: "1.1"
updated: "2026-10-30"
---

# Шаблоны `video`

| Шаблон | `template_kind` | Где использовать |
| --- | --- | --- |
| [`video-brief.md`](video-brief.md) | `request` | `videos/briefs/` |
| [`storage-policy.md`](storage-policy.md) | `output` | Project policy или `videos/briefs/` для session policy |
| [`shot-plan.md`](shot-plan.md) | `output` | `videos/plans/` |
| [`continuity-ledger.md`](continuity-ledger.md) | `output` | `videos/continuity/` |
| [`seam-window.md`](seam-window.md) | `output` | `videos/transitions/`, обязательно для seamless boundary |
| [`sound-plan.md`](sound-plan.md) | `output` | `videos/sound/`, если audio_required=yes |
| [`segment-record.md`](segment-record.md) | `output` | `videos/segments/` |
| [`delivery-card.md`](delivery-card.md) | `output` | `videos/assembly/` |
| [`frame-job.md`](frame-job.md) | `output` | `videos/segments/` или `videos/assembly/`, для каждого окна покадровой правки |
