---
id: domain.cartography.templates.readme
title: "Шаблоны cartography"
type: meta
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Шаблоны

| Файл | Назначение |
| --- | --- |
| [`atlas-manifest.yaml`](atlas-manifest.yaml) | состав атласа, наборы IDs и общая vector/view policy |
| [`system-record.yaml`](system-record.yaml) | звёздная система, звёзды, орбитальные и календарные параметры |
| [`body-record.yaml`](body-record.yaml) | тело, фигура, датум/CRS, ось, вращение, сутки и год |
| [`geospatial-layer.yaml`](geospatial-layer.yaml) | пространственный слой и его geometry/provenance contract |
| [`climate-layer.yaml`](climate-layer.yaml) | поля климата и Köppen–Geiger с ограничениями адаптации |
| [`map-spec.yaml`](map-spec.yaml) | проекция, векторный файл, sidecar и интерактивный viewport |
| [`vector-export-checklist.md`](vector-export-checklist.md) | приёмка SVG/другого векторного deliverable |

Шаблоны задают структуру, но не создают вымышленные физические значения. Заполняй неизвестные поля как unknown/неизвестные и согласуй формат записи с валидатором проекта.
