---
id: template.video.seam-window
title: "Отдельная обработка и проверка окна видеошва"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
template: true
template_kind: output
---

# Seam window — `<left_segment>` → `<right_segment>`

- Boundary type / seamless requirement:
- Boundary timecode and exact frame index:
- Actual FPS/timebase:
- Window start/end (must include material before and after the boundary):
- Left/right source clip URIs + hashes:
- Character/prop/action/camera state expected at boundary:
- Chosen handling method and why it is supported by user's renderer/editor:
- Prompt/reference(s) for the separate bridge/continuation/refinement step:
- Attempt limit and observed attempts:

## Audio window
- `audio_required`: explicit yes/no:
- Time range and source audio IDs/hashes:
- Speech/music/ambience continuity and sync handling:
- Observed click, gap, loudness jump, cut-off line or mismatch:

## Review of processed window
- New processed window URI/hash and provenance:
- Normal-speed review of both clips in context:
- Frame-level/technical checks:
- Audio playback, if applicable:
- Issues and local correction:
- Human decision: `approved` / `rejected` / `fallback requested`; approver/date:

A seam is not treated or accepted based only on a simple cut/stitch, a raw overlap, passing a still frame, or a crossfade without separate review. These alone do not establish that the seam was removed. If the chosen tool cannot separately process and verify this centered window, mark `blocked`; do not call it seamless (`VID-POL-07`).
