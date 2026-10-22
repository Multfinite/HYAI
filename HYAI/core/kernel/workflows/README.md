---
id: kernel.workflows.readme
title: "HYAI/core/kernel/workflows/ — универсальные процессы"
type: meta
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# Процессы ядра

Здесь только процессы, применимые к любой предметной области. Процесс, в котором есть слово «код» или «лор», живёт в домене.

| Процесс | Когда | Результат |
| --- | --- | --- |
| [`task.md`](task.md) | изменение уже согласовано | дифф + отчёт `task` |
| [`audit.md`](audit.md) | нужно исследовать, не меняя | отчёт `audit` с приоритетами |
| [`decision-consolidation.md`](decision-consolidation.md) | решения расползлись | слитые решения по `HYAI-DEC-09` |
| [`doc-cleanup.md`](doc-cleanup.md) | документы обросли водой | сокращённые документы с сохранением норм |

Доменные процессы: `HYAI/core/domains/<domain>/workflows/`. Профиль ссылается на процесс полем `workflow` в своём `profile.yaml`.

## Как читать процесс

Стадии `WF-00..WF-05`, ворота `G0..G3`, остановки `STOP-1..5` — см. [`../policies/interaction.md`](../policies/interaction.md). Ворота не пропускаются: `G1` (согласованный план) — обязательное условие любой записи в репозиторий.
