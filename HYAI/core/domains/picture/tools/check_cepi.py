#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Validate CEPI evidence contracts, not image quality. Never calls remote APIs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"[0-9a-fA-F]{64}\Z")


def dimensions(v):
    return isinstance(v, list) and len(v) == 2 and all(type(n) is int and n > 0 for n in v)



def validate_ear_review(frame, where, size):
    """Opt-in structural evidence only. No segmentation, image or truth inference."""
    crops = frame.get("crops")
    required = isinstance(crops, list) and any(isinstance(c, dict) and c.get("anatomy_kind") == "ear" for c in crops)
    if not required and "ear_review" not in frame:
        return []
    errors = []
    prefix = where + ".ear_review"

    def need(ok, field, message):
        if not ok:
            errors.append(f"{prefix}.{field}: {message}")

    def text(v):
        return isinstance(v, str) and bool(v.strip())

    def obj(v):
        return v if isinstance(v, dict) else {}

    def evidence(value, field, keys):
        for key in keys:
            need(text(obj(value).get(key)), field + "." + key, "explicit observation or evidence reference required")

    def hashes(value, field, keys):
        for key in keys:
            need(bool(HEX.fullmatch(str(obj(value).get(key, "")))), field + "." + key, "full sha256 required")

    raw = frame.get("ear_review")
    need(isinstance(raw, dict) and bool(raw), "record", "ear_review object required for ear crop")
    e = obj(raw)
    need(e.get("schema") == "ear/1", "schema", "expected ear/1")
    roles = e.get("reference_roles")
    need(isinstance(roles, list) and bool(roles), "reference_roles", "nonempty reference roles required")
    for ref in roles if isinstance(roles, list) else []:
        evidence(ref, "reference_roles", ["uri", "scope", "evidence"])
        hashes(ref, "reference_roles", ["sha256"])
        need(obj(ref).get("role") in ("geometry", "colour", "shadow_layout", "hair", "accepted_full_frame"),
             "reference_roles", "unknown reference role")
    g = obj(e.get("geometry_lock"))
    hashes(g, "geometry_lock", ["source_sha256", "source_silhouette_sha256"])
    box = g.get("source_box")
    valid = isinstance(box, list) and len(box) == 4 and all(type(v) is int for v in box)
    if valid and dimensions(size):
        x, y, X, Y = box
        valid = 0 <= x < X <= size[0] and 0 <= y < Y <= size[1]
    need(valid, "geometry_lock.source_box", "integer xyxy source_box must fit source canvas")
    need(type(g.get("no_enlargement")) is bool, "geometry_lock.no_enlargement", "explicit boolean required")
    evidence(g, "geometry_lock", ["view_evidence", "measurement_evidence", "contour_overlay_evidence"])
    shadow = obj(e.get("shadow"))
    mode = shadow.get("mode")
    need(mode in ("unchanged", "generative", "layer-opacity"), "shadow.mode", "unknown shadow mode")
    hashes(shadow, "shadow", ["palette_source_sha256"])
    evidence(shadow, "shadow", ["footprint_evidence", "scope_evidence"])
    if mode == "layer-opacity":
        layer = obj(shadow.get("layer"))
        hashes(layer, "shadow.layer", ["base_sha256", "layer_sha256", "mask_sha256"])
        strength = layer.get("strength")
        need(type(strength) in (int, float) and 0 <= strength <= 1, "shadow.layer.strength", "numeric strength 0..1 required, not boolean")
        evidence(layer, "shadow.layer", ["authorization", "evidence"])
    evidence(e.get("mask_review"), "mask_review",
             ["ear_skin", "hair", "seam", "source_boundary_overlay", "composite_boundary_observation"])
    evidence(e.get("audit"), "audit", ["native_crop_evidence", "full_frame_evidence", "contour_evidence",
                                      "hair_evidence", "colour_evidence", "shadow_evidence", "post_style_colour_evidence"])
    approvals = e.get("approval_events")
    need(isinstance(approvals, list), "approval_events", "list required; may be empty before owner review")
    scopes = ("working_reference", "geometry", "colour_local", "shadow_layout", "shadow_strength", "hair_seam", "full_frame")
    matching = []
    output_sha = obj(frame.get("output")).get("sha256")
    for event in approvals if isinstance(approvals, list) else []:
        event = obj(event)
        need(event.get("scope") in scopes, "approval_events", "unknown approval scope")
        need(type(event.get("approved")) is bool, "approval_events", "explicit approved boolean required")
        evidence(event, "approval_events", ["quote"])
        hashes(event, "approval_events", ["artifact_sha256"])
        if event.get("scope") == "full_frame" and event.get("artifact_sha256") == output_sha:
            matching.append(event)
    if obj(frame.get("owner_approval")).get("approved") is True:
        need(bool(matching) and matching[-1].get("approved") is True, "approval_events",
             "full_frame approval must target exact output sha256; local approval or later rejection cannot promote final")
    return errors


def validate(data):
    errors = []

    def need(ok, where, message):
        if not ok:
            errors.append(f"{where}: {message}")

    def text(v):
        return isinstance(v, str) and bool(v.strip())

    def obj(v):
        return v if isinstance(v, dict) else {}

    if not isinstance(data, dict):
        return ["pic.cepi-contract: root must be an object"]
    need(data.get("schema") == "cepi/1", "schema", "expected cepi/1")
    need(data.get("method") == "crop-edit-paste-integrate", "method", "expected CEPI")
    need(text(data.get("task_id")), "task_id", "required")
    need(data.get("state") in ("planned", "in_progress", "blocked", "complete"), "state", "unknown state")
    complete = data.get("state") == "complete"
    tool = obj(data.get("tool"))
    need(text(tool.get("name")) and text(tool.get("selection_evidence")), "tool", "name and selection evidence required")
    need(type(tool.get("external")) is bool, "tool.external", "must be boolean")
    need(text(tool.get("cost")), "tool.cost", "record actual cost or unknown, never invent zero")
    need(data.get("delivery_mode") in ("add-version", "replace-final"), "delivery_mode", "explicit mode required")
    frames = data.get("frames")
    if not isinstance(frames, list):
        return errors + ["frames: expected list"]
    need(not complete or bool(frames), "frames", "complete run cannot be empty")
    seen = set()
    for index, raw in enumerate(frames):
        where = f"frames[{index}]"
        f = obj(raw)
        fid = f.get("id")
        valid_id = text(fid)
        need(valid_id, where, "nonempty id required")
        if valid_id:
            need(fid not in seen, where, "duplicate frame id")
            seen.add(fid)
        source = obj(f.get("source"))
        need(bool(HEX.fullmatch(str(source.get("sha256", "")))), where + ".source", "full sha256 required")
        size = source.get("dimensions")
        need(dimensions(size), where + ".source", "positive integer dimensions required")
        need(text(source.get("uri")), where + ".source.uri", "required")
        locks = f.get("content_lock")
        need(isinstance(locks, list) and bool(locks) and all(text(v) for v in locks), where + ".content_lock", "nonempty locks required")
        eyes = f.get("eyes")
        need(isinstance(eyes, list), where + ".eyes", "list required")
        if not eyes:
            need(text(f.get("eyes_not_applicable_reason")), where + ".eyes", "no eyes needs reason")
        elif isinstance(eyes, list):
            names = set()
            for e in eyes:
                e = obj(e)
                name = e.get("character")
                need(text(name) and text(e.get("colour")) and text(e.get("evidence")), where + ".eyes", "character, source colour, evidence required")
                if text(name):
                    need(name not in names, where + ".eyes", "duplicate character")
                    names.add(name)
        environment = f.get("environment_objects")
        need(isinstance(environment, list), where + ".environment_objects", "object inventory required")
        if not environment:
            need(text(f.get("environment_not_applicable_reason")), where + ".environment_objects", "empty inventory needs reason")
        elif isinstance(environment, list):
            for item in environment:
                item = obj(item)
                need(all(text(item.get(k)) for k in ["id", "source", "position"]), where + ".environment_objects", "object id, canon source and position required")
                if complete:
                    need(text(item.get("final_check")), where + ".environment_objects", "post-integrate object check required")
        crops = f.get("crops")
        need(isinstance(crops, list) and bool(crops), where + ".crops", "real crops required")
        crop_ids = set()
        for ci, raw_crop in enumerate(crops if isinstance(crops, list) else []):
            c = obj(raw_crop)
            cw = f"{where}.crops[{ci}]"
            cid = c.get("id")
            need(text(cid), cw, "id required")
            if text(cid):
                need(cid not in crop_ids, cw, "duplicate crop id")
                crop_ids.add(cid)
            box = c.get("box")
            good_box = isinstance(box, list) and len(box) == 4 and all(type(v) is int for v in box)
            if good_box and dimensions(size):
                x, y, X, Y = box
                good_box = 0 <= x < X <= size[0] and 0 <= y < Y <= size[1]
            need(good_box, cw + ".box", "integer xyxy box must be inside source")
            need(text(c.get("defect")) and text(c.get("prompt_ref")), cw, "defect and saved prompt reference required")
            need(c.get("prompt_provenance") in ("verbatim", "reconstructed", "recipe"), cw, "explicit prompt provenance required")
            need(bool(HEX.fullmatch(str(c.get("input_sha256", "")))), cw, "input crop sha256 required")
            if complete or c.get("accepted") is True:
                for k in ["mask_sha256", "edit_sha256"]:
                    need(bool(HEX.fullmatch(str(c.get(k, "")))), cw + "." + k, "full sha256 required")
                need(c.get("accepted") is True, cw, "complete run needs accepted crop")
                need(text(c.get("alignment")) and text(c.get("audit_evidence")), cw, "alignment and pre-paste audit evidence required")
                need(c.get("prompt_provenance") == "verbatim", cw, "new accepted run needs verbatim prompt; historical reconstruction belongs in report")
                strength = c.get("style_strength")
                need(type(strength) in (int, float) and 0 <= strength <= 1, cw, "style strength must be numeric 0..1")
                need(type(c.get("full_strength_required")) is bool, cw, "full_strength_required must be explicit boolean")
                if c.get("full_strength_required") is True:
                    need(strength == 1, cw, "required full strength cannot be weakened")
        errors.extend(validate_ear_review(f, where, size))
        comp = obj(f.get("composite"))
        if complete or comp:
            need(bool(HEX.fullmatch(str(comp.get("sha256", "")))), where + ".composite", "sha256 required")
            need(type(comp.get("outside_mask_changed")) is int and comp.get("outside_mask_changed") == 0, where + ".composite", "lossless outside-mask diff must be zero")
            need(type(comp.get("protected_changed")) is int and comp.get("protected_changed") == 0, where + ".composite", "protected diff must be zero")
            need(text(comp.get("evidence")), where + ".composite", "numeric evidence required")
        integ = obj(f.get("integrate"))
        if complete or integ:
            mode = integ.get("mode")
            need(mode in ("local-integrate", "single-full-frame-integrate"), where + ".integrate", "explicit mode required")
            calls, limit = integ.get("calls"), integ.get("limit")
            counts = type(calls) is int and type(limit) is int and 0 <= calls <= limit and limit > 0
            need(counts, where + ".integrate", "invalid iteration budget")
            need(integ.get("status") in ("pending", "blocked", "done"), where + ".integrate", "status required")
            if mode == "single-full-frame-integrate":
                need(text(integ.get("authorization")), where + ".integrate", "full-frame permission required")
                need(type(limit) is int and limit == 1, where + ".integrate", "single means limit 1")
            if complete or integ.get("status") == "done":
                need(integ.get("status") == "done" and type(calls) is int and calls > 0, where + ".integrate", "integration not executed")
                need(text(integ.get("prompt_ref")) and text(integ.get("evidence")), where + ".integrate", "saved prompt and result evidence required")
        audit = obj(f.get("audit"))
        output = obj(f.get("output"))
        if complete or output:
            need(bool(HEX.fullmatch(str(output.get("sha256", "")))), where + ".output", "sha256 required")
            native, exported = output.get("native_dimensions"), output.get("export_dimensions")
            need(dimensions(native) and dimensions(exported), where + ".output", "native and export dimensions required")
            need(text(output.get("resampling")), where + ".output", "resampling or explicit none required")
            if dimensions(native) and dimensions(exported):
                changed_ratio = abs(native[0] * exported[1] - native[1] * exported[0]) > max(native + exported)
                if changed_ratio:
                    need(text(output.get("aspect_ratio_authorization")), where + ".output", "aspect-ratio change needs explicit permission or outpaint record")
                if native != exported:
                    need(output.get("resampling") not in ("none", "identity"), where + ".output", "dimension change cannot claim no resampling")
            if integ.get("mode") == "single-full-frame-integrate":
                need(output.get("pixel_exact_outside") is False, where + ".output", "full-frame cannot inherit local pixel-exact claim")
        if complete or audit:
            need(audit.get("verdict") == "accepted", where + ".audit", "accepted audit required")
            for k in ["full_frame_evidence", "crop_evidence", "eye_check", "global_changes"]:
                need(text(audit.get(k)), where + ".audit." + k, "explicit observation required")
        owner = obj(f.get("owner_approval"))
        if owner.get("approved") is True:
            need(text(owner.get("quote")), where + ".owner_approval", "owner approval requires actual quote")
        delivery = obj(f.get("delivery"))
        if complete or delivery:
            uploaded, verified = delivery.get("uploaded"), delivery.get("verified")
            need(type(uploaded) is bool and type(verified) is bool, where + ".delivery", "explicit booleans required")
            if verified is True or complete:
                need(uploaded is True and verified is True, where + ".delivery", "not uploaded/download-verified")
                need(text(delivery.get("url")), where + ".delivery", "direct file URL required")
                need(bool(HEX.fullmatch(str(delivery.get("download_sha256", "")))) and delivery.get("download_sha256") == output.get("sha256"), where + ".delivery", "download sha256 differs from output")
    return errors


def check_file(path, verify_local=False):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{path}: cannot read manifest: {exc}"]
    errors = validate(data)
    if verify_local and isinstance(data, dict):
        artifacts = data.get("artifacts", [])
        if not isinstance(artifacts, list):
            return errors + ["artifacts: expected list"]
        for a in artifacts:
            if not isinstance(a, dict) or not isinstance(a.get("path"), str) or not HEX.fullmatch(str(a.get("sha256", ""))):
                errors.append("artifacts: path and full sha256 required")
                continue
            f = path.parent / a["path"]
            try:
                digest = hashlib.sha256(f.read_bytes()).hexdigest()
                if digest != a["sha256"].lower():
                    errors.append(f"{f}: sha256 mismatch")
            except OSError as exc:
                errors.append(f"{f}: unavailable: {exc}")
    return errors


def discover(root):
    # Reuse the framework resolver: do not hardcode a consumer project's layout.
    sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools"))
    import _shared as sh
    cfg = sh.domain_configs(root, sh.manifest(root)).get("picture") or {}
    result = set()
    for rel in (cfg.get("data") or {}).get("root_paths") or []:
        directory = root / str(rel) / "stages"
        if directory.is_dir():
            result.update(directory.rglob("cepi-manifest.json"))
    return sorted(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, action="append", default=[])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--verify-local", action="store_true")
    args = parser.parse_args()
    paths = list(args.manifest)
    if args.discover:
        paths.extend(discover(args.root.resolve()))
    if not paths and not args.discover:
        parser.error("provide --manifest or --discover")
    errors = []
    for path in sorted(set(paths)):
        errors.extend(f"{path}: {error}" for error in check_file(path, args.verify_local))
    print(f"CEPI manifests: {len(set(paths))}; errors: {len(errors)}" + ("; not applicable (no manifests)" if not paths else ""))
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
