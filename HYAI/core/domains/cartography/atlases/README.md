---
id: domain.cartography.atlases.readme
title: "Корень данных планетарных атласов"
type: meta
status: review
authority: source-record
visibility: internal
version: "1.0"
updated: "2026-11-01"
---

# Данные атласов

Стандартный корень `HYAI/core/domains/cartography/atlases/` можно переопределить в проектной конфигурации. Это каталог данных, а не место для инструментального кода. Канонические записи должны ссылаться на stable IDs и решения `P-0005`.

| Подкаталог | Назначение |
| --- | --- |
| [`systems/`](systems/README.md) | звёздные системы и параметры звёзд |
| [`bodies/`](bodies/README.md) | планеты/спутники, датум, CRS и вращение |
| [`layers/`](layers/README.md) | физические, климатические, политические и иные spatial layers |
| [`maps/`](maps/README.md) | map specs, проекции и ссылки на векторные exports |
| [`exports/`](exports/README.md) | принятые SVG/другие векторные выдачи и sidecars |

Не складывай сюда raster screenshots, изображения-подложки или растровые карты. Экран интерактивного preview — временное отображение, а не экспортируемый файл.
