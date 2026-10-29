---
id: decision.kit.KIT-0004
title: "Самостоятельный домен video для temporal continuity, звука и монтажа"
type: decision
status: review
authority: contract
visibility: internal
scope: kit
affects_domains: [kit]
affects:
  - "HYAI/core/domains/video/"
  - "HYAI/core/domains/video/videos/"
  - "HYAI/meta/manifest.yaml"
  - "HYAI/meta/schema/rule-ids.yaml"
  - "HYAI/meta/schema/domains/video.yaml"
  - "HYAI/meta/lint/terms/video.json"
  - "HYAI/meta/architecture/video.md"
  - "HYAI/meta/terminology/video.md"
  - "HYAI/meta/questions/video.md"
  - "HYAI/meta/decisions/video/README.md"
  - "AGENTS.md"
supersedes: null
---

# KIT-0004. Самостоятельный домен `video`

## Решение

В HYAI создаётся model-agnostic guide-only домен `video`: он описывает поведение агента, prompts/планы, gates и QA, но не добавляет renderer/API/ComfyUI integration, зависимости или автоматический вызов генерации. Предметная область имеет собственную нормативность временного состояния, handoff сегментов, audio continuity, seam processing и монтажа и потому не является профилем `picture` (`KIT-POL-05`).

Владелец project data — отдельный `<video_root>` (`HYAI/core/domains/video/videos` в самом HYAI); во внешнем проекте root задаётся вне подмодуля. В активную конфигурацию добавляются `video/producer`, `video/continuity-director`, `video/sound-designer`, `video/editor`, `video/analysis`.

Обязательные основы политики:
- sound предполагается нужным, но на каждой задаче пользователь явно отвечает yes/no; в вопросе default=yes назван явно;
- media storage/retention задаётся project policy, либо согласуется на уровне session до получения media;
- до prompts спрашивается, каким способом сегмент получает continuity context, включая last frame/tail, и подтверждается отличие статичного I2V reference от video continuation;
- каждый boundary классифицируется; бесшовная граница требует отдельного centered seam-window, video/audio обработки и human review до приёмки; простая склейка, необработанный overlap или still-reference сами по себе не устраняют шов (`VID-POL-02..12`);
- binary keyframe ownership остаётся у `picture`, а `video` хранит только ID/URI/hash reference (`P-0003`);
- одобрение человека требуется на ключевых планировочных и media gates; автоматическая оценка не гарантирует плавность.

## Почему

`picture/series` управляет связанными статичными изображениями, но не задаёт timecoded action state, segment continuation, audio seams или transition-aware video assembly. Собственный `<video_root>`, authority/access, workflows и policies удовлетворяют `KIT-POL-04..06`; декларативные схемы используют действующие generic tools без правки `HYAI/tools/*.py` (`KIT-POL-07`).

## Проверка

`check_domains.py`, `check_manifest.py`, `frontmatter.py --check`, `check_rules.py`, `check_indexes.py`, `lint_terms.py --domain video`, `run_checks.py` и матричные тесты профилей.
