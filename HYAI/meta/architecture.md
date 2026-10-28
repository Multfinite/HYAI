---
id: meta.architecture.hub
title: "Архитектура: хаб доменов"
type: architecture
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Архитектура: хаб

Здесь нет норм — только границы и ссылки. Нормы живут в `HYAI/meta/architecture/<domain>.md`, по одному файлу на домен.

## Домены

| Домен | Архитектура домена | Границы |
| --- | --- | --- |
| `software` | [`architecture/software.md`](architecture/software.md) | код, тесты, контракты модулей, схемы данных |
| `docs` | [`architecture/docs.md`](architecture/docs.md) | ТЗ, спецификации, документация, диаграммы |
| `narrative` | [`architecture/narrative.md`](architecture/narrative.md) | факты мира, хронология, текст |
| `picture` | [`architecture/picture.md`](architecture/picture.md) | брифы, промпты «5+3», промежуточные звенья и финальные изображения |
| `kit` | [`architecture/kit.md`](architecture/kit.md) | домены, профили, проверки каркаса |

## Правила хаба

1. Хаб не содержит правил: если здесь появилось «мы не используем X», это норма домена и ей не место в хабе.
2. Домены не ссылаются друг на друга напрямую: связь идёт через `HYAI/meta/decisions/project/` (`P-*`).
3. Новая связь между доменами оформляется решением `P-*`, а не правкой двух архитектур сразу.
