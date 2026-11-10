---
id: domain.picture.tools.readme
title: "Инструменты домена picture: CEPI"
type: meta
status: review
authority: none
visibility: internal
---

# Структурная проверка CEPI

- [check_cepi.py](check_cepi.py) — проверка протокола без генерации и сети.
- Формат: [cepi-manifest.md](../templates/cepi-manifest.md).
- Процесс: [crop-edit-paste-integrate.md](../workflows/crop-edit-paste-integrate.md).

Команда: `python3 HYAI/core/domains/picture/tools/check_cepi.py --discover`.
Явный файл: `--manifest /path/cepi-manifest.json`; `--verify-local` сверяет доступные
локальные artifacts[].sha256. Протокол не доказывает качество картинок, истинность
канона и чужие URI. Исторические снимки не становятся новыми complete-запусками.
