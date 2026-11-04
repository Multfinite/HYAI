---
id: decision.picture.PIC-0001
title: "Форма переноса промптов и изображений в другой чат — страница по шаблону"
type: decision
status: review
authority: none
visibility: internal
scope: picture
affects_domains: [picture]
affects:
  - "HYAI/core/domains/picture/policy.md"
  - "HYAI/core/domains/picture/agents.md"
  - "HYAI/core/domains/picture/README.md"
  - "HYAI/core/domains/picture/templates/handoff-page.html"
  - "HYAI/core/domains/picture/templates/handoff-page.md"
  - "HYAI/core/domains/picture/templates/build_handoff_page.py"
  - "HYAI/core/domains/picture/templates/README.md"
  - "HYAI/core/domains/picture/workflows/handoff-page.md"
  - "HYAI/core/domains/picture/workflows/README.md"
  - "HYAI/core/domains/picture/registry/documents.yaml"
  - "HYAI/tools/tests/test_handoff_page.py"
  - "HYAI/tools/tests/README.md"
  - "AGENTS.md"
  - "HYAI/meta/decisions/picture/README.md"
  - "HYAI/meta/decisions/README.md"
  - "HYAI/meta/reports/picture/2026-11-04-handoff-page.md"
  - "HYAI/meta/reports/picture/README.md"
  - "HYAI/meta/reports/README.md"
supersedes: null
---

# PIC-0001. Страница переноса «промпт + картинка»

## Решение

Ввести в домене `picture` норму: при просьбе пользователя дать удобную форму для копирования и вставки в другой чат, где изображения обрабатываются промптами, агент обязан выдать **автономную HTML-страницу по единому шаблону**, а не только список промптов в сообщении.

Норма записывается правилами `PIC-POL-10` (триггер и обязательный вывод), `PIC-POL-11` (границы страницы), `PIC-WF-03` (процесс `picture/handoff-page`) и `PIC-QA-07` (приёмка). Канонический каркас — `templates/handoff-page.html`, спецификация полей — `templates/handoff-page.md`, детерминированный сборщик — `templates/build_handoff_page.py`. Обязательный комплект выдачи: `<slug>-handoff.html`, `<slug>-handoff.txt`, `<slug>-handoff.zip` в `<picture_root>/stages/<slug>/`.

Форма страницы фиксируется: шапка с переключателем вариантов, блок-инструкция и по одной карточке на пару «изображение + промпт» с кнопками копирования текста, копирования картинки в буфер, скачивания PNG и исходника. Изображения встраиваются в `data:` URI; сеть, CDN и внешние шрифты запрещены.

## Почему

Перенос пары «картинка + промпт» в другой чат — два разных действия (приложить файл и вставить текст). Стена текста в чате заставляет пользователя вручную сопоставлять кадры с промптами и искать файлы; Markdown-ссылки вида `sandbox:` в чате только подчёркиваются, но не открывают файл воркспейса. Страница с карточками снимает оба дефекта и остаётся самодостаточной даже без сети.

Страница — артефакт **переноса**, а не звено генерации: она не создаёт и не меняет изображения, не подменяет промпт и не запускает прогон. Поэтому `PIC-POL-01` («только через промпт») к ней не применяется, а прогон остаётся за пользователем (`HYAI-RES-*`).

## Последствия

- Новые правила используют существующие классы `PIC` (`POL`, `WF`, `QA`); реестр `HYAI/meta/schema/rule-ids.yaml` и ядро не меняются, ворота `HYAI-PERM-G05` не затрагиваются.
- Шаблон и сборщик живут в домене `picture`, а рабочие артефакты остаются в `<picture_root>` проекта-потребителя (`PIC-POL-06`). Внутрь подмодуля HYAI проектные данные не пишутся.
- Запрещены секреты, токены, PII, `sandbox:`-ссылки, телеметрия, выгрузка во внешние хранилища без приёмки владельца и статус `approved` (`HYAI-PERM-N02`, `HYAI-PERM-N05`).
- Процесс `picture/handoff-page` добавляется в каталог процессов и реестр обязательного чтения; фрагмент `picture/agents.md` и собираемый из него `AGENTS.md` получают триггер, чтобы норма срабатывала на входе, а не по догадке.
- Для переноски файлов в другой чат выдаётся ZIP; если чат принимает картинку из буфера, достаточно кнопки «Копировать картинку».

## Уточнение 2026-11-04

`[А]` Владелец указал, что промпты формы переноса обязаны включать стиль-фильтр. Проверка файлов показала: блок присутствовал, но стоял после длинного замка содержания и в видимой части карточки не читался. Норма уточнена: при заданном `style_filter` (`PIC-POL-08`) дословный блок `STYLE FILTER` ставится **в первую строку каждого промпта**, карточка получает метку, шапка — счётчик, а сборщик при `require_style_filter: true` машинно отвергает промпт, в котором фильтр спрятан или отсутствует (`PIC-QA-07`).

## Проверка

`python3 HYAI/tools/run_checks.py` (`rc=0`), в том числе `check_rules.py` на новые ID, `check_links.py`, `check_indexes.py`, `check_decisions.py`, `check_report.py`, `assemble_agents.py --check`. Отдельно — рендер тестового манифеста сборщиком, `node --check` извлечённого JS и `zipfile.testzip()`.
