---
id: report.picture.2026-11-04-handoff-page
title: "Норма формы переноса «промпт + картинка» в домене picture"
type: report
report_kind: task
domain: picture
profile: picture/pipeline
status: review
authority: none
visibility: internal
date: "2026-11-04"
workflow: picture/handoff-page
decisions: ["PIC-0001"]
cross_scope:
  - path: "AGENTS.md"
    why: "Собираемый вход агента получил триггер формы переноса из фрагмента домена picture."
  - path: "HYAI/meta/decisions/README.md"
    why: "Новое решение PIC-0001 внесено в общий индекс решений."
  - path: "HYAI/meta/reports/README.md"
    why: "Отчёт внесён в общий индекс отчётов."
  - path: "HYAI/tools/tests/test_handoff_page.py"
    why: "Добавлен тест сборщика страницы переноса в наборе тестов каркаса."
  - path: "HYAI/tools/tests/README.md"
    why: "Новый тест внесён в индекс тестов каркаса."
---

# Норма формы переноса «промпт + картинка»

## Задача

`[А]` Пользователь 2026-11-04 задал норму: если он просит удобную форму для копирования и вставки в другой чат, где изображения обрабатываются промптами, агент должен выводить страницу того же вида по шаблону, а не только текст. Требуется выгрузить в HYAI политику, шаблон, воркфлоу и сопровождающие документы и оформить PR.

## Что сделано

| Файл | Действие |
| --- | --- |
| `HYAI/core/domains/picture/policy.md` | добавлены `PIC-POL-10`, `PIC-POL-11`, `PIC-WF-03`, `PIC-QA-07` |
| `HYAI/core/domains/picture/templates/handoff-page.html` | каркас автономной страницы с плейсхолдерами |
| `HYAI/core/domains/picture/templates/handoff-page.md` | спецификация полей манифеста, структуры и приёмки |
| `HYAI/core/domains/picture/templates/build_handoff_page.py` | сборщик HTML + TXT + ZIP на стандартной библиотеке |
| `HYAI/core/domains/picture/workflows/handoff-page.md` | процесс `picture/handoff-page`: триггер, шаги, проверка |
| `HYAI/core/domains/picture/{templates,workflows}/README.md` | новые файлы внесены в индексы каталогов |
| `HYAI/core/domains/picture/registry/documents.yaml` | зарегистрированы процесс и шаблоны |
| `HYAI/core/domains/picture/{README.md,agents.md}` | обновлены перечень правил и входной триггер |
| `AGENTS.md` | пересобран из источников |
| `HYAI/meta/decisions/picture/PIC-0001-handoff-page.md` | решение о новой норме |
| `HYAI/tools/tests/test_handoff_page.py` | тест сборщика: автономность HTML, ZIP, отказ на битом манифесте |
| `HYAI/tools/tests/README.md` | индекс тестов каркаса |
| `HYAI/meta/decisions/{README.md,picture/README.md}` | индексы решений |
| `HYAI/meta/reports/picture/2026-11-04-handoff-page.md` | этот отчёт |
| `HYAI/meta/reports/{README.md,picture/README.md}` | индексы отчётов |

Страница не генерирует и не меняет изображения; промпты переносятся дословно. Прогон остаётся за пользователем.

## Проверка

`[В]` Результаты приводятся по факту запуска, непроверенное не заявлено: `python3 HYAI/tools/run_checks.py` — все проверки `rc=0`; `python3 -m unittest discover -s HYAI/tools/tests` — без падений. Сборщик отрендерен на тестовом манифесте: число карточек и `data:` URI совпало с числом пар, внешних `http(s)`-ресурсов и `sandbox:`-ссылок `0`, `node --check` извлечённого JS — `rc=0`, `zipfile.testzip()` — `None`.

## Открытые вопросы

- `status: review` у новых документов и решения: статус `approved` ставит только владелец (`HYAI-PERM-N05`).
- `[?]` Нужен ли отдельный профиль для форм переноса, или процесс остаётся в зоне `picture/pipeline`: сейчас выбран второй вариант как минимальный.
- `[В]` Свойство «`sandbox:`-ссылки в чате не открываются» зафиксировано наблюдением в сессии; в документах каркаса оно не описано и при смене клиента требует повторной проверки.
