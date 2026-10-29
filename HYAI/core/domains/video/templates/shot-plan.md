---
id: template.video.shot-plan
title: "Таймлайн и план сегментов"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
template: true
template_kind: output
---

# Shot plan — `<project_slug>`

Approved version/date:

| Shot ID | Scene | In/out | Duration | Visual goal/action beats | Start state → end state | Camera | Picture refs (IDs/URIs + hash) | Audio beats | Transition in/out | Continuity handoff mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | | | | | | | | | | |

Allowed boundary values: `cut`, `match-cut`, `bridge`, `dissolve`, `seamless-continuation`. For every boundary asking seamless continuity, link its required `seam-window` record. A hard cut must be intentional and recorded; do not propagate last-frame references across it by default.

Human storyboard approval:
- approved by/date:
- approved references and deviations:
