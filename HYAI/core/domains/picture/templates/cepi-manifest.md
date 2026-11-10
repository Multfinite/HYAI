---
id: template.picture.cepi-manifest
title: "Протокол CEPI: артефакты, стадии и доказательства"
type: template
status: review
authority: none
visibility: internal
version: "1.0"
updated: "2026-11-08"
template: true
template_kind: output
---

# Протокол crop-edit-paste-integrate

Создавать `<picture_root>/stages/<slug>/cepi-manifest.json` **до** работы по
[CEPI](../workflows/crop-edit-paste-integrate.md). Один манифест может описывать
серию, но кадры, кропы, глаза и финальные проходы адресуются раздельно.
Шаблон не является свидетельством уже выполненной генерации.

## Минимальная запись в начале работы

```json
{
  "schema": "cepi/1",
  "task_id": "local-remediation",
  "state": "planned",
  "method": "crop-edit-paste-integrate",
  "tool": {"name": "selected-image-edit", "external": false, "selection_evidence": "owner request", "cost": "unknown"},
  "delivery_mode": "add-version",
  "frames": []
}
```

До первой генерации добавить кадр и кропы; пустой план не является разрешением
генерировать без зафиксированной базы/замков/боксов. Общие состояния:
`planned`, `in_progress`, `blocked`, `complete`. Готовность кадров — отдельная.

## Поля каждого `frames[]`

| Поле | Тип / смысл |
| --- | --- |
| `id` | уникальная строка, реальный идентификатор сцены |
| `source` | `{sha256, dimensions:[W,H], uri}` — неизменяемая база |
| `content_lock` | непустой список конкретных неизменяемых признаков |
| `eyes` | список `{character, colour, evidence}`; пустой только с `eyes_not_applicable_reason` |
| `environment_objects` | список `{id, source, position, final_check}` для малых канонических объектов; пустой только с `environment_not_applicable_reason` |
| `crops` | записи локальных областей ниже |
| `composite` | `{sha256, outside_mask_changed, protected_changed, evidence}` после вставки |
| `integrate` | `{mode, calls, limit, status, authorization, prompt_ref, evidence}` |
| `audit` | `{verdict, full_frame_evidence, crop_evidence, eye_check, global_changes}` |
| `output` | `{sha256, native_dimensions, export_dimensions, resampling, pixel_exact_outside}` |
| `owner_approval` | `{approved, quote}` — отдельное от аудита решение; не выдумывать цитату |
| `delivery` | `{uploaded, verified, url, download_sha256}`; возвращённый ID не заменяет скачивание |

`composite`, `audit`, `output`, `delivery` можно не иметь до соответствующего этапа;
при `complete` они обязательны. Нельзя отметить `complete`, если есть только кропы.
`integrate.mode`: `local-integrate` / `single-full-frame-integrate`.
`integrate.status`: `pending` / `blocked` / `done`; `calls` учитывает успешные
генеративные выходы, отклонённые вызовы отдельно журналируются в `blocked_reason`.
Для full-frame `limit=1`; если выполнен, `calls=1`. Ноль — это ещё не интеграция.

## Поля каждого `crops[]`

| Поле | Тип / смысл |
| --- | --- |
| `id` | уникальный внутри кадра ключ; сторона/персонаж в человекочитаемом описании |
| `box` | целочисленный `[x0,y0,x1,y1)` внутри source dimensions |
| `defect` | наблюдаемый дефект со ссылкой на источник требования |
| `input_sha256` | SHA файла реального кропа, не контактного листа |
| `mask_sha256` | SHA маски разрешённого вклада |
| `prompt_ref` | путь к спецификации и фактическому тексту вызова |
| `prompt_provenance` | `verbatim` / `reconstructed` / `recipe`; последние два не выдавать за лог |
| `edit_sha256` | SHA генеративного выхода, когда он получен |
| `alignment` | описание опор и преобразования, либо измеренное `identity` |
| `audit_evidence` | где записан осмотр до paste, включая замки и анатомию |
| `accepted` | результат аудита кропа, не одобрение владельца |
| `style_strength` | число 0..1 для слоя композита; не «сила модели» |
| `full_strength_required` | boolean: при true внутри маски strength=1 |

Для нового complete-протокола `prompt_provenance=verbatim` обязателен.
Историческую реконструкцию хранить в ретроспективном отчёте, не легализовать
задним числом как новый полностью соответствующий CEPI запуск.

## Доказательства и размеры

`evidence` — не слово «OK», а путь/URI конкретной таблицы/кропа/сверки с хэшем,
метрикой или описанным наблюдением. Внешний URI не читается валидатором автоматически.
Пустой полный кадр или кроп не заменяются одной маленькой контактной картинкой.

Хэши — полные 64 hex; размеры — два положительных целых числа. Если native и export
различаются, `resampling` обязан описывать преобразование и отсутствие претензии на
восстановление нативной детализации. Если меняется aspect ratio — отдельный допуск
или outpaint, не скрытое растяжение.

При `single-full-frame-integrate` поле `pixel_exact_outside` должно быть false:
нулевая разница промежуточного композита не переносится на весь финальный кадр.
Семантическое сохранение глаз проверяется заново; не притворяться, что это pixel-exact.

## Проверка

```bash
python3 HYAI/core/domains/picture/tools/check_cepi.py --manifest path/to/cepi-manifest.json
python3 HYAI/core/domains/picture/tools/check_cepi.py --root . --discover
```

В проекте с подмодулем путь инструмента начинается с `HYAI/HYAI/`.
`--verify-local` дополнительно сверяет доступные локальные `{path,sha256}`-артефакты
из `artifacts[]`; относительные пути считаются от каталога манифеста. Нельзя использовать
секретные пути или передавать токены в JSON. Машинная проверка подтверждает контракт и
локальные байты, **не** качество изображения, канон, действительность чужого URI
или правдивость формально заполненного визуального свидетельства.
