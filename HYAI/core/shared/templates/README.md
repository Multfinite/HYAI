---
id: shared.templates.readme
title: "Общие шаблоны"
type: meta
status: approved
authority: none
visibility: internal
version: "1.0"
updated: "2026-10-22"
---

# Общие шаблоны

| Файл | `template_kind` | Кто использует |
| --- | --- | --- |
| [`analysis-report.md`](analysis-report.md) | `output` | Профили `*/analysis` всех доменов |
| [`skill-router.md`](skill-router.md) | `output` | `HYAI/tools/build_skills.py`: навык выбора домена и профиля |
| [`skill-domain.md`](skill-domain.md) | `output` | `HYAI/tools/build_skills.py`: навык домена с профилями и проверками |
| [`skill-procedure.md`](skill-procedure.md) | `output` | `HYAI/tools/build_skills.py`: навык процедуры с собственным триггером |

Шаблоны навыков — форма, а не норма: право остаётся в `AGENTS.md` и в политике домена, поэтому
формулировки можно уточнять без решения `KIT-*`.

Шаблоны конкретного домена живут в `HYAI/core/domains/<domain>/templates/`: домен описывает свою форму, общая часть остаётся здесь.
