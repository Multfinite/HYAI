---
id: template.video.storage-policy
title: "Согласованная политика хранения video media"
type: template
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-29"
template: true
template_kind: output
---

# Storage policy — `<project_slug>`

Policy level: `project` / `session`
User/owner approval and date:

| Data class | Allowed location/URI | Access contour | Retention/deletion | Backup | Rejected version handling |
| --- | --- | --- | --- | --- | --- |
| Briefs/prompts/shot plans | | | | | |
| Picture references (link only; owner `picture`) | | | | | |
| Generated video segments | | | | | |
| Audio, voices and source material | | | | | |
| Seam-window intermediates | | | | | |
| Final delivery | | | | | |

- External storage/provider explicitly allowed? `yes/no`; restrictions:
- Public export allowed? `yes/no`; rights/consent checks:
- Hash and sidecar requirements:
- Policy is effective before media is generated or imported: `yes/no`

Do not infer retention or upload permission from default values. If any required row is unresolved, stop before media work (`VID-POL-03`).
