---
id: meta.terminology.cartography
title: "Терминология домена cartography"
type: meta
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Термины `cartography`

| Термин | Определение |
| --- | --- |
| `body_id` | Стабильный ID планетарного тела, на котором определены CRS и пространственный слой. |
| `CRS` | Coordinate reference system: правила интерпретации численных координат, осей, единиц и привязки к телу. |
| `datum` | Опорная модель/система, к которой привязаны координаты и ориентация тела. |
| `epoch` | Момент или reference epoch, для которого заданы координаты, положение оси или движение. |
| `ellipsoid` | Математическая аппроксимация фигуры тела, заданная параметрами и datum; Earth ellipsoid не предполагается по умолчанию. |
| `layer` | Идентифицируемый набор spatial features одного тематического назначения с общим body/CRS/time/provenance contract. |
| `map sidecar` | Отдельная metadata-запись к SVG/vector output, сохраняющая body, CRS, projection, units, epoch и provenance. |
| `Köppen–Geiger` | Климатическая классификация, чьи версия/пороги/период должны быть заданы; не-земная адаптация маркируется и не создаёт выдуманных классов. |
| `transient viewport` | Экранное отображение интерактивного renderer, не являющееся canonical data или сохраняемым картографическим файлом. |
