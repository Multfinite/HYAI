---
id: domain.cartography.profile.analysis
title: "Профиль analysis"
type: meta
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Профиль `analysis`

Основная зона — `HYAI/meta/reports/cartography/**`. Это независимый read-only аудит данных, карт, инструментов и evidence.

Machine profile: [`profile.yaml`](profile.yaml).

## Чего не делает

- Не исправляет canonical atlas records или геометрию.
- Не утверждает точность только по виду карты или факту открытия файла.
- Не предполагает совместимость произвольной планетной CRS.
- Не представляет неизвестную величину как ошибку/факт без доказательства.
