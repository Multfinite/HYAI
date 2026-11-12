# SPDX-License-Identifier: GPL-3.0-only
"""Ear evidence contracts; offline, no image-quality or owner-authenticity claim."""
import copy
import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).with_name("test_picture_cepi.py")
spec = importlib.util.spec_from_file_location("base_cepi_tests", P)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
cepi = base.cepi
H = base.H


def ear_fixture():
    d = base.fixture()
    f = d["frames"][0]
    f["crops"][0]["anatomy_kind"] = "ear"
    f["ear_review"] = {
        "schema": "ear/1",
        "reference_roles": [{"uri": "original.webp", "sha256": H, "role": "geometry",
                             "scope": "accepted silhouette of this view only", "evidence": "owner geometry quote"}],
        "geometry_lock": {"source_sha256": H, "source_box": [5, 5, 80, 80],
                          "source_silhouette_sha256": H, "no_enlargement": True,
                          "view_evidence": "three-quarter view", "measurement_evidence": "native tip/base positions retained",
                          "contour_overlay_evidence": "original vs composite contour overlay"},
        "shadow": {"mode": "unchanged", "palette_source_sha256": H,
                   "footprint_evidence": "same upper plane", "scope_evidence": "layout only approved, strength not approved"},
        "mask_review": {k: "observed source and composite" for k in
                        ["ear_skin", "hair", "seam", "source_boundary_overlay", "composite_boundary_observation"]},
        "audit": {k: "observed final and source" for k in
                  ["native_crop_evidence", "full_frame_evidence", "contour_evidence", "hair_evidence",
                   "colour_evidence", "shadow_evidence", "post_style_colour_evidence"]},
        "approval_events": [{"scope": "geometry", "approved": True, "quote": "keep this shape", "artifact_sha256": H}]
    }
    return d


class EarReviewTests(unittest.TestCase):
    def setUp(self):
        self.d = ear_fixture()
        self.f = self.d["frames"][0]
        self.e = self.f["ear_review"]

    def bad(self, text):
        errors = cepi.validate(self.d)
        self.assertTrue(any(text in e for e in errors), errors)

    def test_valid_ear(self):
        self.assertEqual(cepi.validate(self.d), [])

    def test_old_manifest_still_valid(self):
        self.assertEqual(cepi.validate(base.fixture()), [])

    def test_new_ear_requires_review_even_when_planned(self):
        self.d["state"] = "planned"
        del self.f["ear_review"]
        self.bad("ear_review")

    def test_opt_in_review_is_checked_without_crop_marker(self):
        del self.f["crops"][0]["anatomy_kind"]
        self.e["schema"] = "unknown"
        self.bad("ear/1")

    def test_missing_roles(self):
        self.e["reference_roles"] = []
        self.bad("reference_roles")

    def test_bad_role(self):
        self.e["reference_roles"][0]["role"] = "all_for_every_species"
        self.bad("reference role")

    def test_missing_reference_hash(self):
        self.e["reference_roles"][0]["sha256"] = "short"
        self.bad("sha256")

    def test_explicit_reference_scope(self):
        del self.e["reference_roles"][0]["scope"]
        self.bad("scope")

    def test_source_contour_hash_required(self):
        del self.e["geometry_lock"]["source_silhouette_sha256"]
        self.bad("source_silhouette_sha256")

    def test_bool_not_source_coordinate(self):
        self.e["geometry_lock"]["source_box"][0] = True
        self.bad("source_box")

    def test_source_box_inside_canvas(self):
        self.e["geometry_lock"]["source_box"] = [0, 0, 101, 80]
        self.bad("source_box")

    def test_enlargement_lock_explicit_boolean(self):
        self.e["geometry_lock"]["no_enlargement"] = 1
        self.bad("no_enlargement")

    def test_zero_outside_diff_not_boundary_review(self):
        del self.e["mask_review"]["composite_boundary_observation"]
        self.bad("composite_boundary_observation")

    def test_style_requires_colour_recheck(self):
        del self.e["audit"]["post_style_colour_evidence"]
        self.bad("post_style_colour_evidence")

    def test_full_frame_and_native_both_required(self):
        for key in ["full_frame_evidence", "native_crop_evidence"]:
            d = copy.deepcopy(self.d)
            del d["frames"][0]["ear_review"]["audit"][key]
            self.assertTrue(any(key in e for e in cepi.validate(d)))

    def layer(self):
        self.e["shadow"]["mode"] = "layer-opacity"
        self.e["shadow"]["layer"] = {"base_sha256": H, "layer_sha256": H,
                                     "mask_sha256": H, "strength": .55,
                                     "authorization": "reduce existing dark overlay only",
                                     "evidence": "same layer and footprint, source palette retained"}

    def test_valid_opacity_not_new_style(self):
        self.layer()
        self.assertEqual(cepi.validate(self.d), [])

    def test_opacity_provenance_required(self):
        self.layer()
        del self.e["shadow"]["layer"]["base_sha256"]
        self.bad("base_sha256")

    def test_opacity_needs_permission(self):
        self.layer()
        self.e["shadow"]["layer"]["authorization"] = " "
        self.bad("authorization")

    def test_opacity_number_not_bool_or_out_of_range(self):
        self.layer()
        for v in [True, False, -1, 1.1, "0.55", float("nan"), float("inf")]:
            self.e["shadow"]["layer"]["strength"] = v
            self.bad("strength")

    def test_shadow_mode_closed_enum(self):
        self.e["shadow"]["mode"] = "change_all_skin_hues"
        self.bad("shadow mode")

    def test_local_approval_cannot_promote_final(self):
        self.f["owner_approval"] = {"approved": True, "quote": "local colour good"}
        self.bad("full_frame")

    def test_final_quote_must_target_exact_output(self):
        self.f["owner_approval"] = {"approved": True, "quote": "fine"}
        self.e["approval_events"].append({"scope": "full_frame", "approved": True, "quote": "fine", "artifact_sha256": "b" * 64})
        self.bad("full_frame")

    def test_valid_full_frame_approval(self):
        self.f["owner_approval"] = {"approved": True, "quote": "fine"}
        self.e["approval_events"].append({"scope": "full_frame", "approved": True, "quote": "fine", "artifact_sha256": H})
        self.assertEqual(cepi.validate(self.d), [])

    def test_rejected_final_does_not_approve(self):
        self.f["owner_approval"] = {"approved": True, "quote": "fine"}
        self.e["approval_events"].append({"scope": "full_frame", "approved": False, "quote": "no", "artifact_sha256": H})
        self.bad("full_frame")

    def test_approval_scope_and_quote_required(self):
        self.e["approval_events"][0] = {"scope": "everything", "approved": True, "artifact_sha256": H}
        self.bad("approval_events")

    def test_bad_types_do_not_crash(self):
        for key in ["reference_roles", "geometry_lock", "shadow", "mask_review", "audit", "approval_events"]:
            for value in [None, True, "bad", 1, [False]]:
                d = copy.deepcopy(self.d)
                d["frames"][0]["ear_review"][key] = value
                self.assertTrue(cepi.validate(d), (key, value))
        for value in [None, [], True, "bad"]:
            self.f["ear_review"] = value
            self.bad("ear_review")


if __name__ == "__main__":
    unittest.main()
