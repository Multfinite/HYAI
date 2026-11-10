#!/usr/bin/env python3
"""Сборщик страницы переноса «промпт + картинка» (PIC-POL-10, PIC-WF-03).

Читает JSON-манифест пар «изображение + промпт» и из шаблона handoff-page.html
собирает три артефакта в каталоге выдачи:

    <slug>-handoff.html   автономная страница, изображения в data: URI
    <slug>-handoff.txt    все пары одним текстом
    <slug>-handoff.zip    изображения, промпты по одному, HTML, TXT, README

Стандартная библиотека только; сеть, CDN, секреты и генерация изображений не
используются. Прогон промптов выполняет пользователь в другом чате.

    python3 build_handoff_page.py --manifest handoff.json --out-dir DIR

Формат манифеста — в templates/handoff-page.md.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import sys
import zipfile
from pathlib import Path

MIMES = {
    ".png": "image/png",
    ".webp": "image/webp",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
}
MAX_EMBED = 10 * 1024 * 1024  # artifacts.no_binaries_over_mb, HYAI-ART-19


def fail(message: str) -> None:
    print("ОШИБКА: " + message, file=sys.stderr)
    raise SystemExit(2)


def tags(text: str) -> str:
    """Внедряемый JSON не должен закрывать <script>."""
    return text.replace("</", "<\\/")


def read_manifest(path: Path) -> dict:
    if not path.is_file():
        fail(f"манифест не найден: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"манифест не читается: {exc}")
    for field in ("slug", "title", "caption", "note", "frames"):
        if not data.get(field):
            fail(f"в манифесте нет поля {field!r}")
    if not isinstance(data["frames"], list) or not data["frames"]:
        fail("frames должен быть непустым списком")
    return data


def resolve(raw: str, base: Path) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (base / path)


def embed(path: Path) -> tuple[str, str]:
    if not path.is_file():
        fail(f"изображение не найдено: {path}")
    ext = path.suffix.lower()
    if ext not in MIMES:
        fail(f"неподдерживаемый формат {ext}: {path}")
    size = path.stat().st_size
    if size > MAX_EMBED:
        fail(f"{path}: {size} байт > {MAX_EMBED} (HYAI-ART-19); вынесите во внешнее хранилище")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{MIMES[ext]};base64,{encoded}", ext


def card(index: int, frame: dict, image_path: Path, ext: str) -> str:
    ident = html.escape(str(frame["id"]))
    caption = html.escape(str(frame.get("caption") or ""))
    name = html.escape(image_path.stem)
    badge = f'<div class="badge">{html.escape(str(frame["badge"]))}</div>' if frame.get("badge") else ""
    return f"""<section class="card" data-i="{index}">
<div class="thumb"><img data-img="{index}" alt="{name}{ext}"></div>
<div class="body">
{badge}
<div class="head"><span class="num">{ident}</span><h2>{caption}</h2></div>
<div class="file">файл: <code>{name}{ext}</code> · в буфер копируется PNG</div>
<textarea class="prompt" readonly spellcheck="false"></textarea>
<div class="buttons">
<button class="btn primary" data-act="prompt">Копировать промпт</button>
<button class="btn" data-act="image">Копировать картинку</button>
<button class="btn" data-act="png">Скачать PNG</button>
<button class="btn" data-act="src">Скачать исходник</button>
</div>
<div class="status" aria-live="polite"></div>
</div>
</section>"""


def build_html(template: str, data: dict, frames: list[dict], base: Path) -> tuple[str, list[tuple[Path, str]]]:
    block = str(data.get("style_filter_block") or "").strip()
    require = bool(data.get("require_style_filter"))
    if require and not block:
        fail("require_style_filter: true требует непустое поле style_filter_block")
    images: list[str] = []
    names: list[str] = []
    exts: list[str] = []
    files: list[tuple[Path, str]] = []
    cards: list[str] = []
    a: list[str] = []
    b: list[str] = []
    sha_checked = 0
    for index, frame in enumerate(frames):
        for field in ("id", "caption", "image", "prompt_a"):
            if not frame.get(field):
                fail(f"кадр {index + 1}: нет поля {field!r}")
        image_path = resolve(str(frame["image"]), base)
        uri, ext = embed(image_path)
        expected_sha = str(frame.get("image_sha256") or "").strip().lower()
        if expected_sha:
            if not re.fullmatch(r"[0-9a-f]{8,64}", expected_sha):
                fail(f"кадр {index + 1}: image_sha256 — hex, 8..64 символа (полный хэш или префикс), "
                     f"факт: {expected_sha!r}")
            actual_sha = hashlib.sha256(image_path.read_bytes()).hexdigest()
            if not actual_sha.startswith(expected_sha):
                fail(f"кадр {index + 1}: sha256 изображения {actual_sha} не совпадает с image_sha256 "
                     f"{expected_sha} (PIC-QA-07): в карточку положено не принятый финал кадра")
            sha_checked += 1
        images.append(uri)
        names.append(image_path.stem)
        exts.append(ext)
        files.append((image_path, "images/" + image_path.name))
        if require:
            for key in ("prompt_a", "prompt_b"):
                value = str(frame.get(key) or "")
                if not value:
                    continue
                pos = value.find(block)
                if not value.lstrip().startswith("STYLE FILTER") or pos < 0 or pos > 200:
                    fail(f"кадр {index + 1}: {key} не начинается с блока STYLE FILTER "
                         f"(PIC-POL-08, PIC-QA-07); стиль-фильтр обязан быть в начале промпта")
        a.append(str(frame["prompt_a"]))
        b.append(str(frame.get("prompt_b") or ""))
        cards.append(card(index, frame, image_path, ext))
    has_b = any(b)
    payload = (
        "const A = " + tags(json.dumps(a, ensure_ascii=False))
        + ", B = " + tags(json.dumps(b, ensure_ascii=False))
        + ", IMG = " + tags(json.dumps(images, ensure_ascii=False))
        + ", IMG_NAMES = " + tags(json.dumps(names, ensure_ascii=False))
        + ", IMG_EXTS = " + tags(json.dumps(exts, ensure_ascii=False))
        + ", HAS_B = " + ("true" if has_b else "false") + ";"
    )
    note = str(data["note"])
    if require:
        note = (f'<div class="badge">СТИЛЬ-ФИЛЬТР: включён в {len(frames)}/{len(frames)} промптов, '
                f'блок стоит первым</div>' + note)
    rendered = (template
                .replace("__HANDOFF_TITLE__", html.escape(str(data["title"])))
                .replace("__HANDOFF_CAPTION__", html.escape(str(data["caption"])))
                .replace("__HANDOFF_NOTE__", note)
                .replace("__HANDOFF_CARDS__", "\n".join(cards))
                .replace("__HANDOFF_DATA__", payload))
    left = sorted(set(re.findall(r"__HANDOFF_[A-Z_]+__", rendered)))
    if left:
        fail("незаполненные плейсхолдеры: " + ", ".join(left))
    return rendered, files, sha_checked


def build_txt(data: dict, frames: list[dict], base: Path) -> str:
    lines = [
        str(data["title"]),
        "=" * 64,
        "Для каждого кадра приложите указанный файл изображения к сообщению",
        "и вставьте промпт текстом. Прогон выполняет пользователь.",
        "=" * 64,
        "",
    ]
    for frame in frames:
        p = resolve(str(frame["image"]), base)
        lines += [
            f"----- {frame['id']} · {frame.get('caption') or ''} -----",
            f"КАРТИНКА (приложить): {p.name}",
            "ПРОМПТ (вставить текстом):",
            "",
            str(frame["prompt_a"]),
            "",
        ]
    if any(f.get("prompt_b") for f in frames):
        lines += ["", "=" * 64, "Вариант B: одиночный проход с нуля (картинка не нужна)", "=" * 64, ""]
        for frame in frames:
            if frame.get("prompt_b"):
                lines += [f"----- {frame['id']} · {frame.get('caption') or ''} -----", str(frame["prompt_b"]), ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--template", type=Path, default=Path(__file__).with_name("handoff-page.html"))
    ap.add_argument("--slug", default="")
    args = ap.parse_args()

    manifest_path = args.manifest.resolve()
    base = manifest_path.parent
    data = read_manifest(manifest_path)
    slug = args.slug or str(data["slug"])
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        fail(f"slug {slug!r}: только латиница, цифры и дефис")
    if not args.template.is_file():
        fail(f"шаблон не найден: {args.template}")
    template = args.template.read_text(encoding="utf-8")
    page, image_files, sha_checked = build_html(template, data, data["frames"], base)
    text = build_txt(data, data["frames"], base)

    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    stem = slug + "-handoff"
    html_path = out / (stem + ".html")
    txt_path = out / (stem + ".txt")
    zip_path = out / (stem + ".zip")
    html_path.write_text(page, encoding="utf-8")
    txt_path.write_text(text, encoding="utf-8")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path, arcname in image_files:
            z.write(path, arcname)
        for frame in data["frames"]:
            z.writestr(f"prompts/{frame['id']}-A-image-to-image.txt", str(frame["prompt_a"]))
            if frame.get("prompt_b"):
                z.writestr(f"prompts/{frame['id']}-B-single-pass.txt", str(frame["prompt_b"]))
        z.writestr(txt_path.name, text)
        z.writestr(html_path.name, page)
        z.writestr("README.txt",
                   f"{data['title']}\n\n"
                   "images/ — базовые изображения; prompts/ — по одному промпту на кадр;\n"
                   f"{html_path.name} — страница с кнопками копирования; {txt_path.name} — все пары текстом.\n"
                   "Прогон промптов выполняет пользователь в другом чате.\n")

    external = len(re.findall(r'(?:src|href)="https?://', page))
    enforced = bool(data.get("require_style_filter") and data.get("style_filter_block"))
    print(f"кадров: {len(data['frames'])}; data-URI: {page.count('data:image/')}")
    print(f"sha256-сверка (image_sha256): {sha_checked}/{len(data['frames'])} кадров")
    print("стиль-фильтр: " + ("обязателен, блок первым в каждом промпте" if enforced else "не задан"))
    print(f"внешних http-ресурсов: {external}; вариант B: {'да' if any(f.get('prompt_b') for f in data['frames']) else 'нет'}")
    for path in (html_path, txt_path, zip_path):
        print(f"создан: {path}")
    if external:
        fail("в странице есть внешние ресурсы — нарушение PIC-POL-11")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
