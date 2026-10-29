---
id: domain.video.workflow.production
title: "Процесс video/production: brief, план и ворота запуска"
type: workflow
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/production`

## Этапы

1. **Project rules.** Прочитать project-level rules по хранению, приватности, правам и формату. В отсутствие правила хранения применить `video/storage-policy.md` на уровне сессии. До согласования хранения не импортировать, не рендерить и не переносить медиа (`VID-POL-03`).
2. **Intake.** Зафиксировать цель, audience, длительность, aspect ratio, FPS/resolution (если известны), каналы поставки, число shots, допустимое число попыток и критерии приёмки. Не угадывать обязательные творческие решения.
3. **Явный вопрос о звуке (`VID-POL-02`).** Спросить: «Нужен ли звук? По умолчанию предполагается, что да; подтвердите или укажите “без звука”.» До ответа не считать аудиоплан закрытым. При `yes` перейти к [`sound.md`](sound.md); спросить типы дорожек, язык, источник/права и синхронизацию.
4. **Handoff-вопрос (`VID-POL-04`).** До сегментных prompts запросить выбранный пользователем способ передачи контекста: последний кадр, хвост нескольких кадров/предыдущий клип, другой reference/keyframe или независимые сегменты. Уточнить возможности выбранного им генератора и отличить static image reference от реального video continuation. Записать ответ в brief/shot-plan.
5. **Story/timeline.** Создать continuity bible и shot-plan: shot IDs, цель, action beats, camera, `start_state`, `end_state`, duration, refs, audio need и тип обеих границ. Чётко отделить continuity между монтажными shots от продолжения одного непрерывного действия.
6. **Предпросмотр и approval.** Сформировать storyboard/contact sheet через соответствующий workflow `picture`, если нужны изображения. Человек утверждает shot order, references, переходы и sound/storage plans до видеорендера (`VID-POL-11`).
7. **Preflight.** Сверить все prompts/refs/timing и задать attempt limit до первого платного/долгого вызова пользователя. Убедиться, что у каждого seamless boundary есть готовая запись seam-window с точным временным диапазоном и plan обработки (`VID-POL-07`). Если требуемого метода renderer не поддерживает, остановить запуск и спросить выбор fallback.

## Остановить процесс, если

- нет явного ответа нужен ли звук;
- storage policy не определена проектом или пользователем на сессию;
- пользователь не выбрал/не подтвердил continuity handoff mode;
- обязательные references не приняты или их ownership неясен;
- seamless-window отсутствует, его обработка не определена либо после проверки виден дефект;
- человеческое approval gate не пройдено.
