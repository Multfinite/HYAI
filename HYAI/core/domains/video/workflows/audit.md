---
id: domain.video.workflow.audit
title: "Процесс video/audit: аудит video-пакета без изменений"
type: workflow
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/audit`

Применяет универсальный read-only workflow [`HYAI/core/kernel/workflows/audit.md`](../../../kernel/workflows/audit.md) к артефактам `video`; не копирует его общие правила.

1. Объявить проверяемый project package и ограничения доступа; не запускать внешние модели.
2. Сверить brief и project/session storage record, explicit audio yes/no, shot-plan approvals и handoff mode (`VID-POL-01..04`).
3. Для каждой seamless boundary найти отдельный centered seam-window; проверить указанные bounds, выбранный method, actual output URI/hash, human decision и audio playback record при `audio_required: yes` (`VID-POL-07`, `VID-POL-09`, `VID-POL-11`).
4. Разделить факт наличия документа, технические checks и perceptual claims: без фактически доступного клипа/звука визуальная/аудиальная гладкость получает статус `not verified`.
5. Каждую находку оформить путём, evidence, rule ID, consequence и приоритет; рекомендации — с ценой/риском. Видео, prompts, plans и logs не изменять.
6. Результат — только audit report в `HYAI/meta/reports/video/` и индексные строки, если их требует общий процесс (`HYAI-ART-13`).
