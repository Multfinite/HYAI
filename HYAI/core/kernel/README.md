---
id: kernel.readme
title: "HYAI/core/kernel/ — ядро: правила, действующие в любом домене"
type: meta
status: approved
authority: invariant
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `HYAI/core/kernel/` — ядро

Ядро содержит только то, что действует **в любом домене**: защиту данных, алфавит маркеров провенанса, формат артефактов, протокол взаимодействия, процессы, применимые к любой предметной области.

Ядро не знает слов «код», «лор», «глава». Всё предметное живёт в [`../domains/`](../domains/README.md).

## Состав

| Файл | Правила | Что регулирует |
| --- | --- | --- |
| [`policies/permissions.md`](policies/permissions.md) | `PERM-N`, `PERM-G`, `PERM-A` | Неотменяемые запреты, ворота одобрения, значения по умолчанию |
| [`policies/provenance.md`](policies/provenance.md) | `HYAI-PROV-01..08` | Оси документа, маркеры `[А]/[И]/[В]/[Г]/[?]`, наследование нормативности |
| [`policies/artifacts.md`](policies/artifacts.md) | `HYAI-ART-01..14` | Отчёты, шаблоны, имена, индексы, `cross_scope` |
| [`policies/decisions.md`](policies/decisions.md) | `HYAI-DEC-01..13` | Области решений, префиксы, слияние, индекс |
| [`policies/interaction.md`](policies/interaction.md) | `HYAI-INT-01..27` | Работа с пользователем: язык и тон, когда спрашивать и когда нет, формат вопроса, формат ответа, SPA, режим анализа, выход за профиль, ошибки, передача смены |
| [`agents.md`](agents.md) | — | Фрагмент ядра для сборки `AGENTS.md` (протокол старта, запреты, провенанс) |
| [`principles.md`](principles.md) | — | Четыре принципа каркаса: `3D`, `HaRD`, `INRA`, `HELPER` |
| [`routing.md`](routing.md) | — | Как выбрать домен и профиль по формулировке задачи |
| [`workflows/`](workflows/README.md) | — | `task`, `audit`, `decision-consolidation`, `doc-cleanup` |
| [`templates/`](templates/README.md) | — | Шаблоны артефактов и запросов (`template_kind`) |
| [`spec/`](spec/README.md) | — | Формат манифеста v2 и правила слияния уровней |

## Что ядру запрещено

`HYAI/core/kernel/**` и `HYAI/core/domains/kit/**` входят в `permissions.write.require_approval_for`: изменение ядра или правил самого `kit` требует одобрения владельца (`HYAI-PERM-N05`, `HYAI-PERM-G05`) и решения `scope: kit`. Остальные домены меняются без ворот — иначе `kit` не смог бы расширять систему (`INRA`).
