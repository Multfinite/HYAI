---
id: domain.cartography.profile.atlas-editor
title: "Профиль atlas-editor"
type: meta
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Профиль `atlas-editor`

Основная зона — map specifications и vector exports: проекция, оформление, sidecar, визуальная проверка и интерактивный просмотр исходных векторных слоёв.

Machine profile: [`profile.yaml`](profile.yaml).

## Чего не делает

- Не меняет каноническую геометрию/физические параметры ради удобства дизайна.
- Не сохраняет экранный raster viewport как карту и не добавляет raster underlay.
- Не считает возможность открытия в приложении доказательством корректности CRS.
- Не заявляет готовую поддержку custom-planet CRS до прототипа.
