---
id: report.kit.2026-11-08-ear-remediation-transfer
title: "Передача опыта исправления ушей в picture: нормы, промпты и ear/1"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-11-08"
workflow: kit/domain-authoring
decisions: [KIT-0007, PIC-0006]
cross_scope:
  - path: "HYAI/core/domains/picture/"
    why: "Передача повторяющихся дефектов ремедиации в доменную норму, workflow и шаблоны"
    profile: picture/pipeline
  - path: "HYAI/tools/tests/test_picture_ear_review.py"
    why: "Регрессия доменного доказательного контракта"
    profile: software/code
---

# Передача опыта ушей

## Задача

[А] Передать опыт исправления ушей в целом и ушей паллидов по правилам проекта:
изменить действующие политики/шаблоны/промпты/workflow, а не оставить только отчёт.
G0/G1: основание — прямое поручение владельца; план — общая часть HYAI,
проектная часть отдельно, проверки и отдельные PR. Лимит окружения три задачи,
не более одной тяжёлой; git и запись общих файлов последовательно.

## Что сделано

[В] Введены PIC-POL-23..24/PIC-QA-14, ear-remediation, ear-prompts и ear-review.
Референсы имеют роли; приёмки формы, локального цвета, разметки/силы тени,
волос/стыка и полного кадра адресуются отдельно. Зафиксированы: не увеличивать
принятое ухо при исправлении света; не менять палитру вместо ослабления черноты;
нулевой diff не оправдывает неверную маску; style повторно проверяется по цвету.

[В] Встроенный Arena подходит, внешняя модель не требуется. Техническая прозрачность
существующей тени по поручению отличена от содержательной перекраски. Новый
opacity не объявляется новым style. Видовой канон/числа/цвета/DriveID не попали в HYAI.

[В] Прежняя рекомендация непременно спрятать ухо прядью заменена условной окклюзией
по исходнику/поручению. Коэффициенты одной проекции не являются универсальными.
Маршрутизация обновлена в agents, профилях, CEPI, README/registry; AGENTS собран.

[В] Совместимое ear/1 проверяет структуру доказательств. Новые 26 тестов сначала
дали 22 ожидаемых отказа, затем все26OK; прежние29CEPIтестов не изменены и проходят.
JSON-validator не смотрит пиксели и не проверяет подлинность чужого approval.
Исторические incomplete-данные не легализованы как complete CEPI.

## Проверка

[В] Фактические результаты итоговых команд записываются после выполнения в разделе
«Результаты проверок». Проверены первый прогон30/0, unit26/26 и старые29/29;
первый полный прогон мог пересечься с подготовкой файлов, не назван чистым baseline.
Новые файлы проходят полный повторный конвейер. Генерации изображений и Drive
при переносе не выполняются. Секреты в изменения/логи не включены.

## Открытые вопросы

[В] Машина не доказывает, что контур или цвет визуально верны. Это остаётся аудитом
нативного кропа и полного собранного кадра. Нормы review; их статус не повышен
из приёмки изображения. Отдельный проектный Q-CEPI-01 не закрывается этим переносом.

## Файлы

| Файл | Действие | Назначение |
| --- | --- | --- |
| `AGENTS.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/agents.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/policy.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/profiles/audit/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/profiles/pipeline/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/registry/documents.yaml` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/templates/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/templates/cepi-manifest.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/templates/cepi-prompts.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/templates/ear-prompts.md` | создан | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/templates/ear-review.md` | создан | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/templates/refs-part-readme.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/tools/check_cepi.py` | изменён | Структурная проверка/регрессионные тесты, без удалённых вызовов |
| `HYAI/core/domains/picture/workflows/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/workflows/crop-edit-paste-integrate.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/workflows/ear-remediation.md` | создан | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/core/domains/picture/workflows/remediation.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/decisions/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/decisions/kit/KIT-0007-ear-evidence-extension.md` | создан | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/decisions/kit/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/decisions/picture/PIC-0006-ear-remediation.md` | создан | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/decisions/picture/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/reports/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/reports/kit/2026-11-08-ear-remediation-transfer.md` | создан | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/meta/reports/kit/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/tools/tests/README.md` | изменён | Рабочая норма/шаблон/маршрутизация и провенанс ушного CEPI |
| `HYAI/tools/tests/test_picture_ear_review.py` | создан | Структурная проверка/регрессионные тесты, без удалённых вызовов |

## Результаты проверок

| Команда | Фактический результат |
| --- | --- |
| `python3 HYAI/tools/run_checks.py` | 30 проверок, 0 падений, rc=0 после исправления новых YAML/link/scope дефектов |
| `python3 HYAI/tools/tests/test_picture_ear_review.py` | 26 тестов OK; до реализации22 ожидаемых отказа |
| `python3 HYAI/tools/tests/test_picture_cepi.py` | 29 прежних тестов OK |
| `check_report.py`, `check_domains.py`, `check_indexes.py`, `check_decisions.py`, `check_links.py` | 0 проблем; ссылки719, отчёты18 |
| `check_rules.py`, `frontmatter.py --check` | 362 правила/0проблем, 291файл/0проблем |
| `assemble_agents.py --check`, `git diff --check` | AGENTS актуален185строк, whitespace0 |

[В] Полный прогон включает unit-discover всех тестов каркаса, не только 55 CEPI/ear.
Успешный discover без пользовательских протоколов означает N/A, не приёмку истории.
