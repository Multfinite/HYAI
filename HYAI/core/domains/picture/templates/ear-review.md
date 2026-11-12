---
id: template.picture.ear-review
title: "Дополнение ear/1 к CEPI: роли, замки и область приёмки"
type: template
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-11-08"
template: true
template_kind: output
---


# Дополнение для новых ушных CEPI-задач

В [cepi-manifest](cepi-manifest.md) ставить `crops[].anatomy_kind: ear` и
`frames[].ear_review`. Это **шаблон, не свидетельство выполненного осмотра**.
Исторические данные не превращать задним числом в complete-протокол.
`ear/1` — версия дополнения; корень остаётся `cepi/1` для совместимости.

| Поле `ear_review` | Что записывается |
| --- | --- |
| `schema` | `ear/1` |
| `reference_roles` | непустой список `{uri,sha256,role,scope,evidence}`; role: `geometry`, `colour`, `shadow_layout`, `hair`, `accepted_full_frame` |
| `geometry_lock` | `{source_sha256,source_box,source_silhouette_sha256,no_enlargement,view_evidence,measurement_evidence,contour_overlay_evidence}` |
| `shadow` | `{mode,palette_source_sha256,footprint_evidence,scope_evidence}`; mode: `unchanged`, `generative`, `layer-opacity` |
| `shadow.layer` | при layer-opacity: `{base_sha256,layer_sha256,mask_sha256,strength,authorization,evidence}`; сила 0..1, не boolean |
| `mask_review` | наблюдения/пути `ear_skin`, `hair`, `seam`, `source_boundary_overlay`, `composite_boundary_observation` |
| `audit` | доказательства `native_crop_evidence`, `full_frame_evidence`, `contour_evidence`, `hair_evidence`, `colour_evidence`, `shadow_evidence`, `post_style_colour_evidence` |
| `approval_events` | список `{scope,approved,quote,artifact_sha256}`; может быть пуст до приёмки |

`source_box` в координатах исходного холста; `no_enlargement: true` означает
обязательство сохранить принятую геометрию. Когда сама задача меняет размер,
поставить false и объяснить разрешённое изменение в `measurement_evidence`.
Источник geometry_lock может быть отдельной ранее принятой базой, но не
отвергнутым увеличенным кандидатом. `source_box` обязан помещаться в исходный
холст текущего кадра (перерегистрация — явно в evidence).

Области approval: `working_reference`, `geometry`, `colour_local`,
`shadow_layout`, `shadow_strength`, `hair_seam`, `full_frame`.
При `owner_approval.approved: true` требуется положительное событие **full_frame**
на точный `output.sha256`; одобрение геометрии/локального цвета не заменяет его.
Отказ записывается `approved: false`, а не уничтожением истории принятия.

Ссылки на файлы и осмысленные наблюдения обязательны, но валидатор не видит
пиксели, не доказывает качество маски и не проверяет подлинность цитаты.
`post_style_colour_evidence` содержит новую проверку после style либо причину,
почему новый style не выполнялся (например, только opacity существующего слоя).
Для неизменённых волос/тени всё равно записывается сверка или явная неприменимость.
