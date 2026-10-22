---
id: domain.software.workflows.readme
title: "Домен software: процессы"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Процессы домена `software`

Наследуют общий каркас [`../../../kernel/workflows/README.md`](../../../kernel/workflows/README.md) (стадии `WF-00..05`, ворота `G0..G3`). Здесь только то, что специфично для кода.

| Процесс | Когда |
| --- | --- |
| [`feature.md`](feature.md) | новая возможность по согласованному контракту |
| [`bugfix.md`](bugfix.md) | воспроизводимый дефект |
| [`refactor.md`](refactor.md) | изменение устройства без изменения поведения, либо проектирование |

Профили ссылаются на процесс полем `workflow`. Процесс `audit` — ядерный, домен его не дублирует.
