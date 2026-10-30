---
id: domain.video.workflows.readme
title: "Домен video: процессы"
type: meta
status: review
authority: contract
visibility: internal
version: "1.1"
updated: "2026-10-30"
---

# Процессы `video`

| Процесс | Когда |
| --- | --- |
| [`production.md`](production.md) | Intake, project rules, brief, timeline и storyboard |
| [`continuity.md`](continuity.md) | Handoff контекста, reference contract и обработка окна шва |
| [`sound.md`](sound.md) | Явное решение о звуке и план звуковых слоёв |
| [`assembly.md`](assembly.md) | Ручная сборка, проверка границ, аудио и выдачи |
| [`audit.md`](audit.md) | Read-only аудит video-пакета по общему `kernel/audit` workflow |
| [`frame-repair.md`](frame-repair.md) | Покадровая правка окна дефекта: скан → окно → разбор → правка → сборка → приёмка |

Все workflow — инструкции агенту и пользователю; автоматический вызов внешнего renderer не предусмотрен.
