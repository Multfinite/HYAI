---
id: decision.picture.PIC-0005
title: "Локальная генеративная ремедиация — обязательный crop-edit-paste-integrate"
type: decision
status: review
authority: none
visibility: internal
scope: picture
affects_domains: [picture]
affects:
  - "HYAI/core/domains/picture/policy.md"
  - "HYAI/core/domains/picture/agents.md"
  - "HYAI/core/domains/picture/workflows/crop-edit-paste-integrate.md"
  - "HYAI/core/domains/picture/templates/cepi-manifest.md"
  - "HYAI/core/domains/picture/templates/cepi-prompts.md"
supersedes: null
---

# PIC-0005. CEPI для локальной генеративной ремедиации

## Решение

[А] Владелец поручил закрепить crop-edit-paste-integrate как обязательный метод
аудита и исправления локальных ошибок перегенерацией. Встроенный image-edit
допустим; внешний сервис не является условием качества.

[В] Реализация: PIC-POL-20..22, PIC-QA-12..13; совместимые уточнения PIC-POL-19,
PIC-QA-09..10, процесса remediation и шаблонов. До генерации база/кроп/замки,
после каждого звена аудит, после paste согласованное сведение. Full-frame — только
явно разрешённый единичный integrate с повторным аудитом всей сцены.

## Почему

[В] Сильные локальные edits и масочная сборка позволили довести сложные лица и
кисти, но слабый стиль и широкие полосы защиты глаз потребовали интеграции.
Full-frame может удалить маленький канонический объект; нулевой diff композита
не доказывает сохранность финала. Поэтому отдельны реестр окружения, native/export
размеры, одобрение владельца и обратная SHA-проверка доставки.

## Последствия

- Нельзя заменить локальную правку новой композицией или выбранный генератор цветокором.
- Нельзя универсализировать параметры одной серии, цену, скрытую модель и лимит среды.
- Политика описывает обязательства, workflow порядок, шаблоны запись, tool структуру;
  визуальное соответствие проверяется отдельно. Проверки —29unit-тестов,
  `check_cepi.py`, `assemble_agents.py --check`, полный `run_checks.py`.
- Старое решение PIC-0004 о доставке применяется с уточнением режимов: add-version
  не требует удаления старого, replace-final требует разрешения и SHA-верификации.
