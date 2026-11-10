# SPDX-License-Identifier: GPL-3.0-only
"""Contract tests only: no image model, network, tokens or paid calls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

P = Path(__file__).resolve().parents[2] / "core/domains/picture/tools/check_cepi.py"
spec = importlib.util.spec_from_file_location("picture_cepi", P)
cepi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cepi)
H = "a" * 64


def fixture():
    return {
        "schema": "cepi/1", "task_id": "test", "state": "complete",
        "method": "crop-edit-paste-integrate", "delivery_mode": "add-version",
        "tool": {"name": "embedded-image-edit", "external": False, "selection_evidence": "owner", "cost": "unknown"},
        "frames": [{
            "id": "frame1", "source": {"sha256": H, "dimensions": [100, 150], "uri": "source.webp"},
            "content_lock": ["identity, fingers, objects, light"],
            "eyes": [{"character": "left", "colour": "blue", "evidence": "source eye crop"}],
            "environment_objects": [{"id": "symbol", "source": "canon", "position": "top right", "final_check": "retained"}],
            "crops": [{"id": "face", "box": [5, 5, 80, 80], "defect": "wrong painted surface, owner request",
                       "input_sha256": H, "mask_sha256": H, "edit_sha256": H,
                       "prompt_ref": "prompt.md", "prompt_provenance": "verbatim",
                       "alignment": "eye and jaw anchors", "audit_evidence": "crop audit",
                       "accepted": True, "style_strength": 1, "full_strength_required": True}],
            "composite": {"sha256": H, "outside_mask_changed": 0, "protected_changed": 0, "evidence": "numeric mask test"},
            "integrate": {"mode": "single-full-frame-integrate", "calls": 1, "limit": 1, "status": "done",
                          "authorization": "owner explicitly requested one pass", "prompt_ref": "integrate.md", "evidence": "native result"},
            "audit": {"verdict": "accepted", "full_frame_evidence": "full review", "crop_evidence": "eye and seam review",
                      "eye_check": "blue retained", "global_changes": "paint detail changed, no content loss observed"},
            "output": {"sha256": H, "native_dimensions": [100, 150], "export_dimensions": [100, 150], "resampling": "none", "pixel_exact_outside": False},
            "owner_approval": {"approved": False},
            "delivery": {"uploaded": True, "verified": True, "url": "https://example.org/file/real-record", "download_sha256": H}
        }]
    }


class CepiTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.frame = self.data["frames"][0]

    def bad(self, word):
        errors = cepi.validate(self.data)
        self.assertTrue(any(word in e for e in errors), errors)

    def test_valid_full_frame(self):
        self.assertEqual(cepi.validate(self.data), [])

    def test_empty_plan_allowed_not_complete(self):
        self.data["frames"] = []
        self.bad("complete run")
        self.data["state"] = "planned"
        self.assertEqual(cepi.validate(self.data), [])

    def test_invalid_box_and_boolean_coordinate(self):
        for box in [[0, 0, 101, 10], [20, 5, 10, 15], [True, 2, 9, 10], [-1, 0, 5, 6]]:
            self.frame["crops"][0]["box"] = box
            self.bad("box")

    def test_environment_inventory_required(self):
        del self.frame["environment_objects"]
        self.bad("object inventory")

    def test_environment_final_check_required(self):
        del self.frame["environment_objects"][0]["final_check"]
        self.bad("post-integrate")

    def test_no_crop(self):
        self.frame["crops"] = []
        self.bad("real crops")

    def test_full_strength_cannot_be_weakened(self):
        self.frame["crops"][0]["style_strength"] = .8
        self.bad("full strength")

    def test_historical_reconstruction_not_verbatim(self):
        self.frame["crops"][0]["prompt_provenance"] = "reconstructed"
        self.bad("verbatim")

    def test_missing_crop_audit(self):
        self.frame["crops"][0]["audit_evidence"] = ""
        self.bad("pre-paste")

    def test_changed_outside_mask(self):
        self.frame["composite"]["outside_mask_changed"] = 1
        self.bad("outside-mask")

    def test_changed_protected_area(self):
        self.frame["composite"]["protected_changed"] = 1
        self.bad("protected diff")

    def test_second_full_frame_pass(self):
        self.frame["integrate"].update(calls=2, limit=2)
        self.bad("limit 1")

    def test_blocked_is_not_done(self):
        self.frame["integrate"].update(status="blocked", calls=0)
        self.bad("not executed")

    def test_full_frame_permission(self):
        self.frame["integrate"]["authorization"] = ""
        self.bad("permission")

    def test_full_frame_not_pixel_exact(self):
        self.frame["output"]["pixel_exact_outside"] = True
        self.bad("pixel-exact")

    def test_native_dimensions_required(self):
        del self.frame["output"]["native_dimensions"]
        self.bad("dimensions")

    def test_no_fake_native_detail(self):
        self.frame["output"]["export_dimensions"] = [200, 300]
        self.bad("no resampling")
        self.frame["output"]["resampling"] = "Lanczos, not native detail"
        self.assertEqual(cepi.validate(self.data), [])

    def test_aspect_ratio_change_requires_record(self):
        self.frame["output"].update(export_dimensions=[300, 300], resampling="resize")
        self.bad("aspect-ratio")

    def test_owner_quote_required(self):
        self.frame["owner_approval"] = {"approved": True}
        self.bad("actual quote")

    def test_no_owner_approval_needed_for_candidate_audit(self):
        self.assertEqual(cepi.validate(self.data), [])

    def test_id_not_download_proof(self):
        self.frame["delivery"]["download_sha256"] = "b" * 64
        self.bad("download sha256")

    def test_not_uploaded(self):
        self.frame["delivery"]["uploaded"] = False
        self.bad("not uploaded")

    def test_no_eyes_requires_reason(self):
        self.frame["eyes"] = []
        self.bad("no eyes")
        self.frame["eyes_not_applicable_reason"] = "object still life"
        self.assertEqual(cepi.validate(self.data), [])

    def test_duplicate_identifiers(self):
        self.data["frames"].append(copy.deepcopy(self.frame))
        self.bad("duplicate frame")

    def test_type_errors_are_findings_not_crashes(self):
        for key in ["state", "delivery_mode", "tool", "frames"]:
            d = copy.deepcopy(self.data)
            d[key] = ["invalid"]
            self.assertTrue(cepi.validate(d))
        for value in [None, [], "bad", 1, True]:
            self.assertTrue(cepi.validate(value))

    def test_bool_not_numeric_budget(self):
        self.frame["integrate"]["calls"] = True
        self.bad("iteration budget")

    def test_local_artifact_sha(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            payload = b"local evidence"
            (d / "artifact.bin").write_bytes(payload)
            self.data["artifacts"] = [{"path": "artifact.bin", "sha256": hashlib.sha256(payload).hexdigest()}]
            p = d / "cepi-manifest.json"
            p.write_text(json.dumps(self.data))
            self.assertEqual(cepi.check_file(p, True), [])
            (d / "artifact.bin").write_bytes(b"changed")
            self.assertTrue(any("mismatch" in e for e in cepi.check_file(p, True)))

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "bad.json"
            p.write_text("{")
            self.assertTrue(cepi.check_file(p))

    def test_discovery_consumer_project_root(self):
        # The existing resolver reads active domain root_paths rather than assuming HYAI data.
        import sys
        sys.path.insert(0, str(P.parents[4] / "tools"))
        import _shared as sh
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "consumer/pictures/stages/scene/cepi-manifest.json"
            real.parent.mkdir(parents=True)
            real.write_text("{}")
            cfg = {"picture": {"data": {"root_paths": ["consumer/pictures"]}}}
            with patch.object(sh, "manifest", return_value={}), patch.object(sh, "domain_configs", return_value=cfg):
                self.assertEqual(cepi.discover(root), [real])


if __name__ == "__main__":
    unittest.main()
