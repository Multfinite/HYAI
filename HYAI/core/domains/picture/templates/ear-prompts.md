---
id: template.picture.ear-prompts
title: "Промпты исправления ушей по независимым задачам"
type: template
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-11-08"
template: true
template_kind: output
---


# Промпт-каркасы для ушей

Расширяют [cepi-prompts](cepi-prompts.md) и [prompt-spec](prompt-spec.md).
Это **recipes**, не verbatim исторических вызовов. Для реальной задачи заполнить
5+3, модель/безопасность/negative, роли входов и сохранить точный скомпилированный
текст до вызова. Канон, углы, skin hue и style не выдумывать из примера.
Не объединять эти задания в неопределённое «make the ear better».

## A. Только форма (до её приёмки)

```text
Edit only the ear geometry in this real head crop to match [approved view-specific
construction]. Reference [A] defines the projected contour and tip; reference [B]
defines the species geometry, not its face, colour or background. Preserve this
character, ear root and concha, original hair, skin palette, lighting and crop.
Show [source-backed surface orientation and stand-off] without a painted crease.
No straight spike, enlarged base, arbitrary curl or forced tip occlusion.
```

Проверка: исходная сетка, контур, кончик, основание, проекция/объём; не объявлять
измеренными 3D-углы по рисованному mockup.

## B. Только исходный цвет (форма уже принята)

```text
Keep the exact accepted ear silhouette, dimensions, position, tip and inner anatomy
from image [A]. Match only the original muted flesh palette from image [B], not
[B]'s ear shape. Preserve inherited matte painted material and scene illumination.
No orange, pink, grey-green drift, bleaching, pores, veins or plastic shine.
Do not recolour surrounding hair, face or neck. Same crop and camera.
```

## C. Только область тени

```text
Preserve the accepted ear contour, scale, flesh palette and anatomy. The shadow
layout reference defines ONLY [named surface] and its full footprint, NOT its
black value, material or altered geometry. Shade [whole returning segment across
both edges / specific named area] according to this scene's light. Do not substitute
a narrow rim, a dark concha or a new fold for the requested shaded plane.
```

## D. Только ослабление существующего затемнения

При доступных слоях и разрешённом opacity-композитинге **не вызывать генератор**
ради формального расхода лимита: фиксируются хэши/сила/поручение и проверка стыков.
Это не отменяет обязательной генерации для нового содержания.
Если требуется согласованный image-edit:

```text
Reduce only the strength of the existing darkening in [exact accepted footprint].
Keep the original skin colours underneath, the same shadow boundary and the exact
accepted ear shape. Do not repaint the ear into another palette, relocate the
shadow, brighten unrelated lit surfaces or add a highlight stripe. No new anatomy,
hair changes, pores or glossy material. Same crop and original painted texture.
```

## E. Только волосы/стык

```text
Repair only [observed malformed hair clump / cutout fringe / lobe speck]. Replace
the false braided mass with [original source-backed hair flow and tie], not a new
hairstyle. Keep the ear tip, silhouette, size, concha, skin hue and shadow unchanged.
No hair crossing the ear, extra curls, ropes, lobes, dark halo or bright outline.
Keep face, eyes, neck, crown and background unchanged.
```

В paste берётся только hair/seam зона, не новый портрет. Проверить исключение уха
из hair-mask: ошибочно сохранённая как кожа старая прядь даёт зубчатую кромку.

## F. Заключительный локальный style/integrate

```text
One final local style integration on the repaired content. Harmonize only [named
junction] into the existing [source-backed technique], keeping the exact accepted
ear geometry, original flesh palette and current shadow footprint and strength.
No skin redesign, photographic pores, grain layer, waxy smoothing, new hair or
anatomy. Keep all non-target content, face, eyes and scene unchanged.
```

После него повторить colour/shadow/contour/hair-check. При дрейфе не называть
промпт успешным лишь потому, что в нём есть `preserve`; отдельно документировать
отклонение и разрешённую адресную коррекцию.
