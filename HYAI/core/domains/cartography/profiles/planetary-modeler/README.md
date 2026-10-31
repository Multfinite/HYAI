---
id: domain.cartography.profile.planetary-modeler
title: "Профиль planetary-modeler"
type: meta
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Профиль `planetary-modeler`

Основная зона — записи систем и тел; общий model specification принадлежит этому профилю, а thematic layer creation координируется с `cartographer`.

Machine profile: [`profile.yaml`](profile.yaml).

## Чего не делает

- Не дополняет неизвестные физические значения «правдоподобными» числами без решения владельца.
- Не меняет карту/слой только по художественному описанию.
- Не считает визуализатор физической моделью.
- Не заменяет Köppen–Geiger другой классификацией и не изобретает категории для не-земного климата.
