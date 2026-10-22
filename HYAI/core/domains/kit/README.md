---
id: domain.kit.readme
title: "Домен kit — создание доменов и профилей"
type: meta
status: approved
authority: invariant
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Домен `kit`

Отвечает на вопрос «как расширять каркас»: как добавить домен, как добавить профиль, как проверить, что расширение не сломало систему.

## Ключевое свойство

`kit` может менять **другие** домены и их профили. Он **не может** менять сам себя и ядро:

| Что | Можно | Почему |
| --- | --- | --- |
| `HYAI/core/domains/*/**` (кроме `kit`) | да, с решением `KIT-*` | задача домена — расширять систему |
| `HYAI/core/domains/kit/**` | **нет** | домен, который проверяет правила, не должен их себе писать |
| `HYAI/core/kernel/**` | **нет** | правила проверки каркаса не могут быть изменены проверяемым |

Обе зоны перечислены в `permissions.write.require_approval_for` манифеста, и `check_manifest.py` падает, если их там нет. Так «нельзя» становится данными, а не обещанием.

## Что здесь лежит

| Файл | Содержание |
| --- | --- |
| [`manifest.yaml`](manifest.yaml) | Каталоги домена, профили, доменные проверки |
| [`policy.md`](policy.md) | Правила `KIT-POL-01..10` |
| [`authority.md`](authority.md) | Уровни нормативности каркаса |
| [`schema/`](schema/README.md) | Машинные словари `authority` и `access` |
| [`access.md`](access.md) | Доступ к каркасу: кто видит решения о формате |
| [`agents.md`](agents.md) | Фрагмент `AGENTS.md` для домена `kit` |
| [`registry/`](registry/README.md) | Что читать перед изменением каркаса |
| [`templates/`](templates/README.md) | Почему отдельных шаблонов нет |
| [`workflows/`](workflows/README.md) | `domain-authoring`, `profile-authoring` |
| [`profiles/`](profiles/) | `domain-builder`, `profile-builder` |

Скелет нового домена: [`../_template/`](../_template/).
