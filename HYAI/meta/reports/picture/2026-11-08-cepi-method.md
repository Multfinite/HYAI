---
id: report.picture.2026-11-08-cepi-method
title: "Перенос CEPI в домен picture: нормы, шаблоны и контрактная проверка"
type: report
status: review
authority: none
visibility: internal
report_kind: task
domain: picture
profile: picture/pipeline
date: "2026-11-08"
workflow: picture/crop-edit-paste-integrate
decisions: ["PIC-0005"]
cross_scope:
  - path: "HYAI/tools/tests/test_picture_cepi.py"
    why: "Регрессионные тесты новой доменной проверки"
    profile: software/code
---

# CEPI в домене picture

## Задача

[А] Владелец поручил обязательный crop-edit-paste-integrate для локальной
генеративной ремедиации, подробный анализ хороших/плохих практик и перенос
опыта из проекта-потребителя. Достаточность встроенного генератора подтверждена
приёмкой результата конкретной серии; универсального превосходства не заявляется.

## Что сделано

[В] Новый workflow описывает freeze/crop/edit/audit/paste/style/integrate/audit/deliver,
поимённые замки глаз, реестр малых объектов окружения, источник канона, строгие
границы маски и различие local/full-frame. Изменены конфликтующие нормы о
процедурном цветокоре, запрете генеративной геометрии и обязательном удалении старого
файла. Новые документы не дублируют проектный канон и конкретные DriveID.

[В] Шаблоны протокола/промптов связаны с prompt-spec, manifest и asset-card;
agents/registry/READMEмаршрутизируютследующегоагента. Новыйcheck_cepiживётвдомене,
беззависимостейотпроектаиниобходимостименятьобщийдвижок.29unit-тестовневызываютмодели.

[В] Исторический опыт:100%слой не равен гарантии достаточного стиля; широкие старые
полосы глаз дают стыки; full-frame может удалить канонический объект окружения;
интерполяция не восстанавливает native-деталь; успешный uploadID не равен downloadSHA.
Эти риски перенесены в нормы, но лица, названия мира и его физика в каркас не попали.

## Проверка

[В] До изменений полный baseline:29проверок,0падений. Контрактныеunit-тестыCEPI:
29/29OK. Итоговые команды/счётчики полного конвейера и список файлов фиксируются
после фактического выполнения, не предполагаются из baseline.

## Открытые вопросы

[В] Валидатор не доказывает визуальный канон, правдивость цитаты или содержимое
внешнего URI. Пустое discover не доказывает соответствия исторических работ.
Новые документы review; статус approved не выставлен агентом. Проектная регрессия
небесного тела оставлена вопросом владельцу в проекте, не новым фактом HYAI.


## Фактические результаты проверки

| Проверка | Результат |
| --- | --- |
| `python3 HYAI/tools/run_checks.py` до изменений |29проверок,0падений |
| `python3 HYAI/tools/run_checks.py` после изменений |30проверок,0падений,rc=0 |
| `python3 HYAI/tools/tests/test_picture_cepi.py` |29тестов,OK |
| `python3 HYAI/tools/check_report.py HYAI/meta/reports/picture/2026-11-08-cepi-method.md` |1отчёт,0проблем |
| `check_links.py`, `check_indexes.py`, `check_decisions.py`, `frontmatter.py --check` |0проблем |
| `check_rules.py` |359правил,0проблем |
| `check_cepi.py --discover` |0протоколов,неприменимо;непритворяетсяпроверкойстарыхзапусков |
| `git diff --check` |0ошибок |

[В] Конвейер30/0включаетполныйнаборunit-тестовкаркаса;отдельные29CEPI-тестов
неявляютсячисломвсехтестов. Доступкimageгенератору/Driveвэтомпереносеневыполнялся.
НикакихновыхбинарныхизображенийвHYAIнепомещалось.

## Файлы

| Файл | Действие | Назначение |
| --- | --- | --- |
| `AGENTS.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/agents.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/manifest.yaml` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/policy.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/profiles/audit/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/profiles/pipeline/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/registry/documents.yaml` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/templates/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/templates/asset-card.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/templates/pipeline-manifest.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/templates/prompt-spec.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/workflows/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/workflows/remediation.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/workflows/style-filter.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/decisions/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/decisions/picture/PIC-0004-handoff-final-integrity.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/decisions/picture/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/reports/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/reports/picture/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/tools/tests/README.md` | изменён | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/templates/cepi-manifest.md` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/templates/cepi-prompts.md` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/tools/README.md` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/tools/check_cepi.py` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/core/domains/picture/workflows/crop-edit-paste-integrate.md` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/decisions/picture/PIC-0005-crop-edit-paste-integrate.md` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/meta/reports/picture/2026-11-08-cepi-method.md` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
| `HYAI/tools/tests/test_picture_cepi.py` | создан | CEPI: норма, маршрут, шаблон, проверка или индекс |
