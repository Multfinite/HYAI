---
id: report.kit.2026-11-07-picture-precall-context
title: "Предвызовной контекст проблемы и цели для picture"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-11-07"
workflow: task
decisions: []
cross_scope:
  - path: "HYAI/core/domains/picture/policy.md"
    why: "добавлено обязательное правило PIC-POL-15"
  - path: "HYAI/core/domains/picture/workflows/"
    why: "предвызовной контекст закреплён в instant, pipeline, series, style-filter и remediation"
  - path: "HYAI/core/domains/picture/templates/prompt-spec.md"
    why: "добавлен отдельный формат сообщения до image tool call, отделённый от промпта модели"
  - path: "HYAI/core/domains/picture/agents.md"
    why: "добавлен обязательный краткий указатель для агента picture"
  - path: "AGENTS.md"
    why: "сгенерирован из источников после обновления инструкции домена"
---

# Предвызовной контекст проблемы и цели для picture

## Задача

Зафиксировать требование явно показывать известную проблему и цель генерации перед каждым созданием/исправлением изображения, особенно на повторных итерациях, не домысливая отсутствующий контекст.

## Что сделано

- В `policy.md` добавлено `PIC-POL-15`: отдельное сообщение перед каждым image tool call содержит `Проблема` и `Цель генерации`; при повторе дополнительно названы наблюдаемый дефект, конкретное изменение и ожидаемая проверка. Неуказанная проблема маркируется как неуказанная, а неясная цель уточняется до вызова.
- В шаблон `prompt-spec.md` добавлен предвызовной формат, явно отделённый от сохраняемого промпта и текста для модели.
- Правило закреплено в `instant`, `pipeline`, `series` (включая `anchor-base` и каждый кадр), `style-filter` и `remediation`.
- Краткие указатели обновлены в `agents.md`, доменном `README.md` и индексе процессов. Документы получили актуальные версии и даты; `AGENTS.md` пересобран из источников.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Сборка общего входа | `python HYAI/tools/assemble_agents.py --write` и `--check` | успешно, 172 строки |
| Конвейер | `python HYAI/tools/run_checks.py --skip-project` | 26 проверок, 0 ошибок |
| Unit-тесты | `python -m unittest discover -s HYAI/tools/tests -v` | 78 тестов, успешно |
| Пробелы diff | `git diff --check` | успешно на финальном наборе изменений |

## Открытые вопросы

Нет. Неясная пользовательская цель должна разрешаться вопросом до генерации, согласно `PIC-POL-15`.
