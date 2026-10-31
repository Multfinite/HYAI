---
id: meta.architecture.cartography
title: "Архитектура домена cartography"
type: architecture
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Архитектура `cartography`

## Владение данными

`cartography` — единственный structured source of truth для параметров тел, spatial objects и геопривязанных слоёв; `narrative` владеет прозой и ссылается на stable IDs (`P-0005`, `CART-POL-01`). Картографическая геометрия не копируется в prose как второй изменяемый источник.

## Canonical model

Планетные системы, тела, CRS, географические объекты и тематические слои разделяются по стабильным IDs (`CART-POL-02..08`). Каждый слой несёт body/CRS, units, frame, epoch/time, source/method и uncertainty. Climate classification использует Köppen–Geiger; неизвестная non-terrestrial adaptation остаётся ограничением (`CART-POL-08`).

## Rendering и форматы

Сохраняемые карты — векторные SVG или другой явно согласованный векторный формат (`CART-POL-09`). QGIS/Inkscape/CesiumJS описываются как рекомендуемые кандидаты, а не уже выполненные интеграции (`KIT-0006`, `CART-POL-10..12`). Экранный 3D viewport может использовать растеризацию дисплея, но остаётся transient view над векторными слоями; не сохраняется как raster-map artifact.

## Неподтверждённые интерфейсы

Произвольные planet ellipsoid/CRS, temporal layers и совместимость экспорта не подтверждены одним выбором инструмента. Прототип на выбранном теле закрывает [`Q-CART-01`](../questions/cartography.md); до проверки не заявлять поддержку «из коробки».
