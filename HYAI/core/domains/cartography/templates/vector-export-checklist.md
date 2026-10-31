---
id: domain.cartography.template.vector-export-checklist
title: "QA векторной картографической выдачи"
type: template
status: review
authority: contract
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Проверка векторной выдачи

- [ ] Формат указан и является векторным; сохранённый результат не является screenshot или raster export.
- [ ] SVG открывается в целевой версии Inkscape (если выбран SVG); другой формат проверен целевым приложением.
- [ ] Файл не содержит внедрённых raster images/подложек; все географические объекты сохранены как vector paths/features.
- [ ] Sidecar содержит map/body/layer IDs, CRS/datum/эллипсоид, projection, coordinate units, epoch/time, source IDs, method, uncertainty и версии инструментов.
- [ ] Экстент, проекция, масштаб, легенда, подписи, символы и unit conversions проверены.
- [ ] Ссылки на body/CRS/layers разрешаются; нет потерянных или дублирующихся IDs.
- [ ] Производные слои содержат модель, версию, входы и ограничения; визуализатор не записан как источник расчёта.
- [ ] Köppen–Geiger слой указывает схему/версию, период, temperature/precipitation inputs и адаптацию (если применялась).
- [ ] Интерактивный viewer (если используется) проверен отдельно: отображает тот же vector source, выбранное тело/ось/время; viewport не сохранён как map output.
- [ ] Уровень доступа и публичная публикация согласованы; hash экспортированного файла записан.

## Результат

- Статус: `draft | review | approved | rejected`
- Проверил(а):
- Дата:
- Найденные ограничения/дефекты:
- Решение владельца:
