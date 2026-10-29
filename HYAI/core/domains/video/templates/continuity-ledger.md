---
id: template.video.continuity-ledger
title: "Visual bible и temporal continuity ledger"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
template: true
template_kind: output
---

# Continuity ledger — `<project_slug>`

## Project invariants
- Style / palette / camera language:
- Character IDs, immutable appearance and wardrobe:
- Location IDs and layout invariants:
- Props and ownership/state constraints:
- Audio invariants, if any:

For every visual image reference: record picture asset ID, URI, `sha256`, approval status and intended role. Do not copy image binaries into `<video_root>` (`VID-POL-08`, `P-0003`).

## Per-shot temporal state
| Boundary/shot | Incoming state | Allowed changes | End state handed forward | Actual continuity reference/mode | Link to seam-window |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Identity/props/location facts are not a substitute for actual temporal handoff. Fill the selected last-frame/tail/reference/independent mode from the user-confirmed brief (`VID-POL-04`).
