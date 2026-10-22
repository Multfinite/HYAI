#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Сборка проекции домена по пресету из `access.schema` (export.presets).

Документ попадает в выгрузку, только если его контур разрешён пресетом; frontmatter
снимается, служебные поля и внутренние ссылки вырезаются по настройкам пресета.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _shared as sh

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
MARKER_RE = re.compile(r"\[(?:А|И|В|Г|\?)\]")
INTERNAL_ID_RE = re.compile(
    r"\bQ-[A-Z]+-\d+\b"
    r"|\b(?:decision|report)\.[a-z0-9.]+\b"
    r"|\b[A-Z]{2,6}-(?:[A-Z]+-)*[A-Z]*\d{2,4}\b"
)
PATH_RE = re.compile(r"`[^`\n]*/[^`\n]*`")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def status_rank(model: dict, status: str) -> int:
    """Позиция статуса в `status_order` домена; неизвестный статус — последний (строже всех)."""
    order = [str(x) for x in (model.get("status_order") or [])]
    if status in order:
        return order.index(status)
    return len(order)


def collect(root: Path, man: dict, domain: str, preset_cfg: dict, model: dict,
            skipped: dict | None = None) -> list[tuple[Path, Path, dict]]:
    """Отбор документов: контур, затем порог статуса. Отброшенное считается по причинам."""
    cfg = sh.domain_configs(root, man).get(domain) or {}
    allowed = preset_cfg.get("allow_visibility") or []
    floor = str(preset_cfg.get("status_floor") or "")
    floor_rank = status_rank(model, floor) if floor else -1
    skipped = skipped if skipped is not None else {"visibility": 0, "status": 0, "no_frontmatter": 0}
    result: list[tuple[Path, Path, dict]] = []
    for base in (cfg.get("data") or {}).get("root_paths") or []:
        directory = root / str(base)
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.md")):
            meta, body = sh.split_frontmatter(path.read_text(encoding="utf-8"))
            if not meta:
                skipped["no_frontmatter"] += 1
                continue
            if allowed and meta.get("visibility") not in allowed:
                skipped["visibility"] += 1
                continue
            if floor_rank >= 0 and status_rank(model, str(meta.get("status") or "")) < floor_rank:
                skipped["status"] += 1
                continue
            result.append((path, directory, {"meta": meta, "body": body}))
    return result


def render(entry: dict, preset_cfg: dict) -> str:
    body = entry["body"].strip()
    if preset_cfg.get("strip_comments"):
        body = COMMENT_RE.sub("", body)
    if preset_cfg.get("strip_internal_links"):
        body = LINK_RE.sub(lambda m: m.group(1) if not m.group(2).startswith(("http", "#")) else m.group(0), body)
    if preset_cfg.get("strip_markers"):
        body = MARKER_RE.sub("", body)
    if preset_cfg.get("strip_repo_paths"):
        body = PATH_RE.sub("", body)
    if preset_cfg.get("strip_internal_ids"):
        body = INTERNAL_ID_RE.sub("", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    lines = []
    for line in body.splitlines():
        if not line.startswith(("    ", "\t")):
            line = re.sub(r"[ \t]{2,}", " ", line)
        lines.append(line)
    body = "\n".join(lines)
    body = re.sub(r"\s+([.,;:!?)])", r"\1", body)
    body = re.sub(r"\(\s*\)", "", body)
    return body.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Сборка выгрузки")
    parser.add_argument("--root", default=str(sh.DEFAULT_ROOT))
    parser.add_argument("--domain", required=True)
    parser.add_argument("--preset", required=True)
    parser.add_argument("--out", default=None, help="переопределить каталог выгрузки")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    man = sh.manifest(root)
    cfg = sh.domain_configs(root, man).get(args.domain) or {}
    rel = ((cfg.get("data") or {}).get("access") or {}).get("schema")
    model = sh.load_yaml(root / str(rel)) if rel else {}
    presets = (model.get("export") or {}).get("presets") or {}
    preset_cfg = presets.get(args.preset)
    if not preset_cfg:
        print(f"пресет {args.preset!r} не объявлен в домене {args.domain!r}", file=sys.stderr)
        return 2

    skipped = {"visibility": 0, "status": 0, "no_frontmatter": 0}
    entries = collect(root, man, args.domain, preset_cfg, model, skipped)
    out_dir = Path(args.out).resolve() if args.out else (root / str(preset_cfg.get("out_dir") or "Exports") / args.preset)

    if args.dry_run:
        for path, _base, _entry in entries:
            print(f"  {sh.rel_posix(root, path)}")
        print(f"\nпресет {args.preset}: к выгрузке {len(entries)}; отброшено по контуру {skipped['visibility']}, "
              f"по статусу {skipped['status']}, без frontmatter {skipped['no_frontmatter']} (dry-run)")
        return 0

    if out_dir.exists():
        shutil.rmtree(out_dir)
    for path, base, entry in entries:
        target = out_dir / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(entry, preset_cfg), encoding="utf-8")
    print(f"пресет {args.preset}: выгружено {len(entries)} документов в {out_dir}; "
          f"отброшено по контуру {skipped['visibility']}, по статусу {skipped['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
