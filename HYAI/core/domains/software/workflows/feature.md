---
id: domain.software.workflow.feature
title: "Процесс software/feature: новая возможность"
type: workflow
status: approved
authority: contract
visibility: internal
version: "2.0"
updated: "2026-10-22"
---

# `software/feature`

1. **Контракт.** Найти или создать: спека, тип, схема, решение `SW-*`. Нет контракта — задача уходит `software/architect`.
2. **Проверка первой.** Тест, который описывает новое поведение и падает.
3. **Реализация.** Минимальный дифф; никакой «подготовки на будущее».
4. **Прогон.** `run_checks.py` + доменные проверки (`checks` в `manifest.yaml` домена).
5. **Отчёт** `HYAI/meta/reports/software/…` с `report_kind: task`.

Ворота: `G1` — согласованный план файлов; `HYAI-PERM-G02`, если меняется публичный контракт.
