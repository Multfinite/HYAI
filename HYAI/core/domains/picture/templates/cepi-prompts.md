---
id: template.picture.cepi-prompts
title: "Промпты CEPI: edit, full-strength style, integrate"
type: template
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-11-08"
template: true
template_kind: output
---

# Раздельные промпты CEPI

Это **каркасы**, не готовые промпты для любого кадра. Заполняются внутри
[prompt-spec](prompt-spec.md), включая 5+3, безопасность, окружение,
динамический negative и журнал. Сохранить окончательный текст **до** вызова,
после — связать с результатом и хэшем. Для API без отдельного negative его блок
включается в единый текст; выдумывать поддержку seed/силы диффузии нельзя.

Плейсхолдеры заполняются по источнику. Неизвестный цвет глаз не угадывается.
Если задача — убрать прожилки, не оставлять в subject старое описание сосудистой сети.
Если референс показывает другую личность, сказать: геометрия детали, не замена лица.

## A. Содержательная правка реального кропа

**Входы:** контекстный crop + разрешённый эталон отдельным файлом при необходимости.

```text
Edit this exact real scene crop, not a new composition.
Task: replace only [observed defect] with [source-backed target].
Keep [character identity, gender, age, expression], [hair], [ear geometry],
[exact hand pose, finger count and object contact], [clothes and occlusion].
Eye colour lock by character: [character A: original hue; character B: hue].
Preserve current skin hue and original light direction and softness.
Reference role: [approved part geometry only; not its face, background or framing].
Keep the crop framing and all non-target scene content.
Do not add [scene-specific prohibited marks, veins, stains, cracks or anatomy errors].
```

**Проверка до paste:** заменён ли именно дефект; не другая ли женщина/кисть;
совпадают ли опоры; не сменились ли глаза, пол, возраст, скрывающий лицо шарф.
Текст `preserve` — намерение, не доказательство сохранности.

## B. Полноценный стиль изменённого участка

Применять после содержательной приёмки, не для маскировки анатомического брака.
Подставить **свой** материал изображения; oil illustration — пример, не общий стиль.

```text
Apply a full-strength [target painting technique] style transfer to this exact crop.
Repaint the smooth edited surfaces into [broad controlled directional brush planes,
matte pigment and simplified tonal masses] matching the surrounding existing paint.
This is a visible stylistic conversion, not subtle smoothing or a grain overlay.
Preserve [all individual identity and anatomy locks], [original iris hues and brightness],
[skin and hair hues], [clothes, objects, occlusion and crop framing].
Preserve original light direction and shadow softness; no bleaching or new hard shadows.
Clean even skin: no veins, cracks, dirty mottling, scratch lines or glossy plastic finish.
Brush shapes model form, not skin blemishes. No content redesign.
```

**Проверка:** сравнить с окружающей живописью, а не только с гладким предыдущим лицом.
Широкие штрихи на щеке не должны читаться как прожилки или шрамы. Вставлять на полной
силе, когда она потребована; маска должна защищать материал, а не ослаблять стиль.

## C. Локальная интеграция шва

```text
Harmonize only the visible compositing transition in this exact context crop:
[hairline / jaw / cuff / scarf / eye-area transition]. Continue the existing paint
and soft lighting through the boundary without a cutout edge or colour step.
Keep the strong painted surface treatment and all original content locks:
[list identities, iris hues, anatomy, objects, light]. Do not smooth back to CGI skin.
Do not introduce marks, hard shadows, extra fingers or new objects.
```

В paste берётся только разрешённая полоса шва; не переносить весь новый кроп ради
удобства. Ещё раз проверить, не расширилась ли область изменения без записи.

## D. Единственный full-frame integrate (только согласованный режим)

**Вход:** именно композит после всех локальных вставок, не оригинал и не лист сравнения.

```text
FINAL SINGLE SEAM-HARMONIZATION PASS on this assembled full illustration.
Edited painted patches have been inserted into the scene. Remove visible pasted
edges, abrupt texture/value boundaries and artificial preserved-eye strips at
[specific observed transitions]. Continue coherent brushwork through the boundaries.
KEEP the strong broad painted planes; do not revert to smooth photo or CGI skin.
Content lock: [each character identity, gender, age, expression, hair, pointed-ear
geometry, exact hands/finger counts, object contacts, clothing, occlusion, composition].
Eye colour lock by character: [explicit original hues and permitted brightness].
Preserve original lighting direction and soft shadows. No bleaching, no new hard
shadow band, no veins, cracks, dirty mottling, scratches or glossy highlights.
One coherent [target technique] illustration, same full composition and all contents.
```

Это запрос, **не гарантия**, что генератор изменит только швы. После него нужна
проверка всего кадра и отдельная запись глобальных отличий (`PIC-QA-12`). Если
результат плох, не делать второй «single» проход молча: остановиться и согласовать
дальнейшее. Не возвращать широкую полосу старых глаз поверх финала.

## Анти-промпты и диагностика провала

| Плохая формулировка | Почему не хватает | Замена |
| --- | --- | --- |
| «Сделай красивее / masterpiece» | нет дефекта и проверяемого результата | точный материал, плоскости, границы и замки |
| «Стиль чуть сильнее ещё раз» | цикл без критерия, теряется содержание | видимый full-strength crop style, затем одна интеграция |
| «Сохрани всё» | не выделены слабые инварианты | поимённые радужки, пол/возраст, руки, предметы, свет |
| «Чистая кожа» без материала | может стать CGI-пластиком | чистота + требуемая живописная моделировка |
| «Штрихи/текстура на коже» | может добавить трещины и грязь | мазок как форма, запрет дефектных отметин |
| «Исправь женщину» | в сцене несколько женщин | точная позиция и признаки нужного персонажа |
| «Убери стыки» в новой генерации с нуля | нет собранной опоры | передать финальный композит как image-edit input |

## Провенанс промптов

`verbatim` — сохранённый фактический вызов; `reconstructed` — восстановление по
журналу/чату с явной оговоркой; `recipe` — переиспользуемый новый каркас. Не выдавать
последние два за точные исторические строки. Наличие хорошего шаблона не доказывает,
что агент использовал его в уже выполненной серии.
