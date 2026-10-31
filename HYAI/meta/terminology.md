---
id: meta.terminology
title: "Терминология: кросс-доменные термины"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-11-01"
---

# Терминология проекта

Здесь только термины, которые используются **больше чем в одном домене**. Термин, живущий в одном домене, живёт в `terminology/<domain>.md` — иначе этот файл станет местом, где встречаются чужие смыслы.

| Термин | Значение | Где используется |
| --- | --- | --- |
| `домен` | Предметная область со своей нормативностью и системой доступа | все |
| `профиль` | Тема, задача и мыслительный процесс внутри домена | все |
| `контур` | Уровень доступа документа (`visibility`) | все |
| `норма` | Утверждение, определяющее поведение системы (`authority` выше `convention`) | все |
| `решение` | Зафиксированная норма с номером в `HYAI/meta/decisions/<scope>/` | все |
| `открытый вопрос` | Неизвестное, оформленное как `Q-*` | все |
| `провенанс` | Маркер происхождения утверждения: `[А]/[И]/[В]/[Г]/[?]` | все |
| `требование` | Проверяемое утверждение о должном с `REQ-ID` и критерием приёмки | `docs`, `software` |

## Правила

1. Два разных определения одного термина в разных доменах — ошибка (`lint_terms.py`, `rc=1`).
2. Термин, использующийся в коде, привязывается к типу или модулю: `контур → Visibility`.
3. Синоним не вводится: если термин переименован, старое имя уходит в `HYAI/meta/lint/terms/*.json` как правило с `reason`.

## Доменные словари

- [`terminology/software.md`](terminology/software.md)
- [`terminology/docs.md`](terminology/docs.md)
- [`terminology/narrative.md`](terminology/narrative.md)
- [`terminology/picture.md`](terminology/picture.md)
- [`terminology/cartography.md`](terminology/cartography.md)
- [`terminology/kit.md`](terminology/kit.md)
