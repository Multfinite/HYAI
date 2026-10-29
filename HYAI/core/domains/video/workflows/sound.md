---
id: domain.video.workflow.sound
title: "Процесс video/sound: подтверждение и планирование аудио"
type: workflow
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-10-29"
---

# `video/sound`

1. Спросить пользователя, нужен ли звук, явно сообщив default `yes`. До явного ответа оставить поле `audio_required` незакрытым и не переходить к рендеру (`VID-POL-02`).
2. При `no` записать `audio_required: no` и подтвердить, что результат намеренно будет silent; не синтезировать и не добавлять звук.
3. При `yes` собрать только применимые параметры: dialogue/narration, language, speaker/voice source and consent, music, ambience, effects, timing, target loudness, source/licence and final mix preference. Не выбирать голос/музыкальный источник за пользователя, если это меняет смысл или права.
4. Привязать audio beats к shot IDs и timecodes, согласовать с action и длительностями; указать владельца аудиофайла и хранение по действующей storage policy.
5. На каждом seamless-window вместе с video continuity plan проверять sound continuity и sync: срез речи, щелчок/тишина, резкий скачок уровня, повтор/пропуск ambience. Указать отдельную обработку окна/перекрытия и человеческую проверку (`VID-POL-07`, `VID-POL-09`).
6. Агент выдаёт sound plan и ручные инструкции; фактическое создание/сведение выполняет пользователь выбранными средствами. В отчёте не заявлять, что звук был прослушан, если аудио не предоставлялось.
