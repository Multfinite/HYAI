---
id: meta.questions
title: "Открытые вопросы: проектные"
type: meta
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-11-01"
---

# Открытые вопросы проекта

Вопрос — это долг, а не архив. Запись живёт здесь, пока неизвестность мешает решению; когда перестала мешать — она уходит.

## Пространства идентификаторов

| Префикс | Где живёт | Область |
| --- | --- | --- |
| `Q-P-NN` | этот файл | проект целиком |
| `Q-SW-NN` | [`questions/software.md`](questions/software.md) | домен `software` |
| `Q-DOC-NN` | [`questions/docs.md`](questions/docs.md) | домен `docs` |
| `Q-NR-NN` | [`questions/narrative.md`](questions/narrative.md) | домен `narrative` |
| `Q-PIC-NN` | [`questions/picture.md`](questions/picture.md) | домен `picture` |
| `Q-VID-NN` | [`questions/video.md`](questions/video.md) | домен `video` |
| `Q-CART-NN` | [`questions/cartography.md`](questions/cartography.md) | домен `cartography` |
| `Q-KIT-NN` | [`questions/kit.md`](questions/kit.md) | домен `kit` |

Маркер `[?]` в тексте обязан указывать на существующий `Q-*` (`HYAI-PROV-02`).

## Проектные вопросы

| ID | Вопрос | Почему важен | Что закроет | Статус |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

## Правила ведения

1. **Закрытый вопрос уходит.** Стал решением — в `decisions/`; стал определением — в `terminology`; оказался не вопросом — удаляется. Запись `closed` старше 30 дней удаляется при консолидации.
2. **Вопрос формулируется как вопрос.** «Нужно разобраться с кэшем» — не вопрос; «кэшировать ответы на уровне модуля или сервиса?» — вопрос.
3. **У вопроса есть цена.** Если ответ ничего не меняет — вопроса нет.
