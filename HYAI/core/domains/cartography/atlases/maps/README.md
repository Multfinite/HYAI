---
id: domain.cartography.atlases.maps.readme
title: "Спецификации карт"
type: meta
status: review
authority: source-record
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Maps

Храни map specs по [`map-spec.yaml`](../../templates/map-spec.yaml). Каждая спецификация фиксирует body/CRS, projection, source layer IDs, масштаб/экстент, стиль, формат файла и sidecar. Выбирай vector output; интерактивное отображение слоёв включай отдельной настройкой и не архивируй его пиксельный viewport как карту.
