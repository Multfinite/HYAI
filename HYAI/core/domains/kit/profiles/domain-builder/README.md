---
id: profile.kit.domain-builder
title: "Профиль kit/domain-builder — создание домена"
type: meta
status: approved
authority: none
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `kit/domain-builder`

Машинное описание профиля — [`profile.yaml`](profile.yaml): зона, процесс, критерии готовности.

**Тема:** новые домены и перестройка существующих.
**Мыслительный процесс:** сначала границы, потом файлы. Домен определяется тем, чего он не делает и каким словарём нормативности пользуется.

## Зона

Основная — `HYAI/core/domains/**`, `HYAI/meta/schema/**`, `HYAI/meta/architecture/**`. Вторичная — `HYAI/meta/manifest.yaml`, `HYAI/meta/terminology/**` (подключение домена), с `cross_scope`.

## Что делает

1. Проверяет, нужен ли домен, или это профиль (`KIT-POL-05`).
2. Создаёт скелет из `_template/`, заполняет нормативную базу.
3. Подключает домен: `domains`, `active`, `path_map`, `decisions.scopes`, оверлей схемы, мета-документы.
4. Добивается зелёных `check_domains.py`, `check_manifest.py`, `run_checks.py`.
5. Записывает решение `KIT-NNNN`.

## Чего не делает

- Не правит `HYAI/core/kernel/**` и `HYAI/core/domains/kit/**` (`KIT-POL-01`).
- Не «подгоняет» домен правкой `HYAI/tools/*.py` (`KIT-POL-07`).
- Не создаёт домен ради каталога: домен без своих правил и своего доступа не создаётся.
