---
id: domain.cartography.profile.cartographer
title: "Профиль cartographer"
type: meta
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Профиль `cartographer`

Основная зона — тематические vector layers в `<atlas_root>/layers/**`. Ссылка на machine profile — [`profile.yaml`](profile.yaml).

## Чего не делает

- Не выдумывает отсутствующие физические параметры или источник наблюдений.
- Не меняет планетарную CRS без согласования владельца тела.
- Не принимает scientific model или климатическую классификацию без provenance.
- Не создаёт растровый map export и не дублирует прозу домена `narrative`.
