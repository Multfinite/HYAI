---
id: template.video.segment-record
title: "Журнал фактически созданного сегмента"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
template: true
template_kind: output
---

# Segment record — `<segment_id>`

- Shot/scene ID and approved shot-plan version:
- User-selected renderer/tool and model/version (or `not reported`):
- Generation mode/capabilities confirmed by user:
- Exact prompt and prompt version/location:
- Reference assets: picture ID/URI/hash and role:
- Continuity handoff mode: last frame / tail frames or previous clip / picture refs / independent / other:
- Actual source frame/time window and hash passed to this segment:
- Requested and actual duration, FPS, dimensions, aspect ratio, frame count:
- Output location/hash under agreed storage policy:
- Attempt number/limit:
- Technical preflight result:
- Visual/audio review result and defect notes:
- User decision: review / approved / rejected / blocked:
- Next boundary type and seam-window ID, if required:

Do not infer an input was passed merely because it appears in a prompt; record the actual handoff reported or visible in the provided workflow/output (`VID-POL-04`, `VID-POL-12`).
