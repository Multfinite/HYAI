---
id: report.kit.2026-10-29-video-domain-implementation
title: "Создание guide-only домена video"
type: report
report_kind: task
domain: kit
profile: kit/domain-builder
status: review
authority: none
visibility: internal
date: "2026-10-29"
workflow: kit/domain-authoring
decisions: ["KIT-0004", "P-0003"]
cross_scope:
  - path: "HYAI/meta/manifest.yaml"
    why: "Регистрация домена, активного профиля, отдельного root_paths, области VID и project handoff scope."
    profile: "project/maintainer"
  - path: "HYAI/meta/decisions/project/P-0003-picture-video-keyframe-handoff.md"
    why: "Зафиксирован общий контракт владения raster/keyframe assets между picture и video по подтверждённому варианту A."
    profile: "project/maintainer"
  - path: "HYAI/meta/decisions/README.md"
    why: "Обновлён проектный индекс decision scopes и общих решений."
    profile: "project/maintainer"
  - path: "HYAI/meta/questions.md"
    why: "Зарегистрировано пространство доменных вопросов Q-VID."
    profile: "project/maintainer"
  - path: "HYAI/meta/reports/README.md"
    why: "Добавлен task report в общий индекс и video-каталог отчётов."
    profile: "project/maintainer"
  - path: "AGENTS.md"
    why: "Пересобран генерируемый entrypoint по обновлённым манифестам; вручную не редактировался."
    profile: "project/maintainer"
---

# Создание guide-only домена `video`

## Задача

Создать отдельный домен HYAI для руководства агента по планированию и приёмке видео с сохранением контекста и плавными переходами. Перед созданием проведён интернет-анализ в `2026-10-29-video-domain-analysis.md`; пользователь подтвердил междоменный вариант A и уточнил обязательные требования к звуку, хранению и обработке швов.

## Что сделано

- Создан `HYAI/core/domains/video/` из `_template/`: собственные policy/authority/access, schema, workflows, templates, registry и пять профилей (`producer`, `continuity-director`, `sound-designer`, `editor`, `analysis`).
- Утверждён направляющий scope: domain — system of agent guidelines, не runtime generator; no API/ComfyUI/renderer integration and no dependency added (`VID-POL-10`).
- Зафиксированы обязательные вопросы для каждой видеозадачи: звук (предлагаемый default=yes, но ответ yes/no спрашивается явно), storage policy (project-level или согласование session-level до media), способ handoff сегмента (last frame/tail/reference/independent) (`VID-POL-02..04`).
- Сделана обязательной отдельная обработка и human review centered seam-window для каждой seamless boundary, включая связанное аудио, если оно включено; простая склейка/crossfade без проверки не принимается (`VID-POL-07`).
- Кадры и keyframes остаются под ownership `picture`, video содержит только ID/URI/hash. Междоменный контракт записан в `P-0003`, domain blueprint — в `KIT-0004`.
- Подключены отдельный `<video_root>`, `VID` policy/workflow/QA/invariant IDs, frontmatter overlay, 3 declarative term checks, report/decision/question/architecture/terminology indexes, active `video/producer`.
- `AGENTS.md` пересобран инструментом `assemble_agents.py`; вручную не менялся.

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| Domain profiles/workflows/scopes | `check_domains.py` | 0 проблем после исправления workflow analysis |
| Manifest | `check_manifest.py` | 0 проблем |
| Frontmatter | `frontmatter.py --check` | 0 проблем после настройки `<video_root>` metadata |
| Rule IDs / references | `check_rules.py` | 0 проблем |
| Domain terms/scopes | `lint_terms.py --domain video`, `lint_scopes.py --domain video` | 0 проблем |
| Decisions | `check_decisions.py` | 0 ошибок, 0 предупреждений |
| AGENTS generation | `assemble_agents.py --write` и `--check` | Успешно; generated file актуален (148 строк) |
| Общий конвейер без project subprocess | `run_checks.py --skip-project` | Успешно: 24 проверки, 0 падений; соответствует разделению CI на pipeline и отдельные unit tests |
| Project unit tests | `python -m unittest discover -s HYAI/tools/tests` во временном PyYAML venv | Успешно: 72 теста |
| Отчёты/навигация/ссылки | `check_report.py`, `check_indexes.py`, `check_links.py` | 10 отчётов, 0 проблем; индексы без проблем; 0 битых ссылок из 508 |

PyYAML используется только во временном окружении `/tmp/hyai-validate`; зависимости проекта не изменялись.

## Открытые вопросы

- Открытых архитектурных вопросов первой версии нет (`KIT-0004`, `P-0003`).
- На каждой реальной задаче агент всё равно обязан спросить explicit sound yes/no, storage policy и handoff method. Размер seam-window и способ обработки зависят от выбранного пользователем renderer/editor и должны быть заданы в этом project/session plan; без поддержки метода переход остаётся blocked, не `seamless`.
