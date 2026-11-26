---
id: report.software.2026-11-25-animationcore-integration
title: "AnimationCore: интеграция срезов S0–S7"
type: report
report_kind: task
domain: software
profile: software/code
status: review
authority: none
visibility: internal
date: "2026-11-25"
workflow: task
decisions: []
---

# AnimationCore: интеграция срезов S0–S7

## Задача

Собрать `AnimationCore` как единственный контроллер анимации игрока и рендера содержимого рук
на базе плана `2026-11-25-animationcore-architecture-and-migration.md` v0.7.2 [А], решений
`SW-0030` (публикация/пин NeoForge `21.1.265`) и `SW-0031` (канон хвата, `Firearm_*`-якорь) [А].
Не менять механику боя, маршрутизацию ввода, bind-позы и существующие арматуры [А].
Проверка — compile/test по каждому standalone-репозиторию, behavior-diff, гейты плана,
вердикты Reviewer/QA/Bug Fixer на моделях, отличных от моделей исполнителей.

## Что сделано

Все правки интегрированы в четыре standalone-репозитория под `mods/`:
`riftfall-animationcore-stage` (AC), `riftfall-core-stage` (Core), `epicfight` (EF), `tacz`.

| Срез | Интегрированные коммиты | Суть |
| --- | --- | --- |
| S0 | root `6042f17`, core `03f7e71`, architect `70d86a1` | артефакты, D4-grep, SHA jar; HSM под `SW-0031`, `Firearm_*` в техспеке |
| S1 | AC `ad5c5ec`, `b4ba615` | `ArmRow`/`ArmsStateSnapshot`, `PoseContext.arms()`, contribution/grip/render контракты |
| S2 | core `f4a4787`, `e42f5e9`, `2426737`; AC `fd3db3c`, `10dd1e7`, `adaba7a`; EF `4acb211`, `4c73f45`, `2e5b1bf` | `acbridge` (кадр §7.3, dual-run 9 контрактов), `FrameDispatcher`, `Firearm_*` append-only id 20/21 |
| S3 | EF `5b3f1fc`, `f2c8998`; tacz `455e1e8`; core `b4094c3`, `1392d64`; AC `cebb813` | слотовые default-методы хуков, `SlotProjectionBridge`, compileOnly AC Path fix |
| S4 | core `7bbaf47`, `f705299`; AC `c26c64d`, `ac18ded`, `bdff120`; EF `b5e7634`, `f2c8998` | `SlotOwnershipGate`, `RenderCallCounter`, `OffhandSlotResolver`, `FpFrameStack`, OFF под флагом `false` |
| S5 | core `4bd5a0d`, `4fdbf8b`; tacz `03be513`; AC `eb41f89`, `6d503e2`, `ac18ded` | подавление TaCЗ, `RenderSuppression` с чистым generic-ядром, REQ-25 сохранён |
| S6 | AC `f3931a2`, `cca77a0` | IK (`FootIk`, `SupportArmIk`, `HeadLookIk`, `TwoBoneIk`) и sway (`BreathSource`, `ShakeSource`, `TremorSource`, `DeterministicNoise`, `SwayChain`), pure-JVM |
| S7 | core `180bce0`, `3816edd` | уборка мёртвых веток, `CALIB_LOG` под флагом (дефолт выкл), `stage=modelBox`, проверка `tools/calib` |

`cross_scope` — правки вне зоны `software/code` не делались; все файлы — код и тесты в домене `software`.

### Существенные исправления интеграции

- `1392d64` — `compileOnly` в core-stage указывал на устаревший каталог `../Riftfall-AnimationCore`
  (пустой jar внутри основного репо); исправлено на реальный standalone-репозиторий
  `../riftfall-animationcore-stage/build/libs` [В].
- `2d555b5` → `4fdbf8b` — ошибочная смена `ownsGunRender(gunStack, true)` на `false` в
  `TaczHandProvider.renderSupportArm` откачена: единственный callsite `LeftHandRender:30` — FP-only,
  поэтому `true` корректен [В]. Вердикт подтверждён Reviewer/QA/Bug Fixer.
- `f705299` — восстановлен `RiftfallGunGate.OFFHAND_FIRST_CLASS = false`, потерянный агентом S4
  при ребейзе; Bug Fixer подтвердил побайтовое совпадение всех 11 файлов `1fd08b4` [В].
- `6d503e2` — `RenderSuppression` разделён на generic pure-ядро и Minecraft-адаптер: прямой
  `Bootstrap.bootStrap()` требует NeoForge `LoadingModList`, недоступный в unit-тестах [В].
- `bdff120` — `FpFrameStack.currentFrame()` возвращает defensive copy (P1 S4) [В].

## Проверка

| Проверка | Команда | Результат |
| --- | --- | --- |
| AC tests | `gradlew test --offline --no-daemon` в `mods/riftfall-animationcore-stage` | `262/0` после S6 |
| Core tests | `gradlew test --offline --no-daemon` в `mods/riftfall-core-stage` | `240/2` — ровно baseline `HandButtonRouterTest` |
| EF build | `gradlew build -x test --offline` в `mods/epicfight` | успех после возврата AC-jar в `libs/` (ignore защищает git) |
| TaCZ build | `gradlew build --offline` в `mods/tacz` | успех |
| S1 review | Reviewer | PASS, P0/P1 нет |
| S2 review | Reviewer / QA / Bug Fixer | PASS; P1-гигиена закрыта `2426737`, `2e5b1bf` |
| S3+S5 review | Reviewer / QA / Bug Fixer | PASS; special ask по `ownsGunRender(...,true)` — оправдан |
| S4 review | QA / Bug Fixer / Reviewer | PASS, P0 нет; 3×P1, P1-3 закрыт `bdff120` |
| S7 review | QA / Bug Fixer | PASS, P0 нет; 2×P1 (doc/стенд) |
| S6 review | Reviewer / QA / Bug Fixer | PASS у всех; `HYAI-PERM-N01` нарушений нет; P1 `BreathSource` закрыт `cca77a0` |
| run_checks | `python HYAI/HYAI/tools/run_checks.py --json` | измерено `18` проверок / `7` падений; все вне кода S1–S7 (assembly drift, frontmatter untracked-файлов, битые ссылки в чужих mods-доках, `affects` у untracked-копий `SW-0030/31`, индексы, `PIC-ERA-01`/`TZ-AC-*`, trailing whitespace в `mods/epicfight/bin`). Плановый baseline указан 4 — расхождение зафиксировано |

## Открытые вопросы

- `Q-S6-01` — 7 численных тестов IK/sway исправлены `f3931a2`; проверяющим предъявлен вопрос,
  не ослаблена ли правка `SwayFrameTest` (изменены ожидания и tolerance) — `HYAI-PERM-N01`.
- `Q-S7-01` — измерено 7 падений `run_checks` вместо 4 по плану; ни одно не вызвано кодом S1–S7.
  Требуется решение владельца: обновить baseline в плане или починить предсуществующие
  frontmatter/links/whitespace/`PIC-ERA-01`/`affects`. `PYTHONIOENCODING=utf-8` решает только
  `UnicodeDecodeError` самого раннера, не эти проверки.
- `Q-S4-P1a` — окно `RenderCallCounter` включает identity `PoseStack`: межвызовные дубли не
  ловит, только re-entrancy; защита от двойного рендера — suppression gates, не счётчик.
- `Q-S4-P1b` — pos-инвариант `tuned−joint=gripShift` тавтологичен (~0 по построению); TP с
  `USE_MODEL_ANCHOR` будет писать `DRIFT`. Только TRACE, не гейт.
- `Q-SW-107`, `Q-AC-05`, `Q-SW-105`, `Q-TZ-02` — остаются открытыми по плану, не блокируют срезы.
