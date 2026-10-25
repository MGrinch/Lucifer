"""Temporary synthetic fixtures exercise structure; no real vendor review occurs."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lucifer", REPO / "tools/lucifer.py")
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.put("persona.md", (REPO / "persona.md").read_bytes())
        for path in ("README.md", "start here.md", "goal.md"):
            self.put(path, b"Synthetic test fixture.\n")
        self.put("sources/corpus/history.txt", b"Historical test data.\n")
        self.write("sources/manifest.json", {"files": [{"path": "sources/corpus/history.txt", "sha256": tool.digest(b"Historical test data.\n")}], "external": []})
        self.write(tool.ALLOWLIST, {"schema": 1, "files": [*tool.NAVIGATION, tool.ALLOWLIST, "sources/manifest.json", "sources/corpus/history.txt"]})
        self.supplement_path = "reviews/01-gemini/supplements/proposal.md"
        self.put(self.supplement_path, b"Synthetic supplement.\nSecond line.\n")
        self.write("workflow/state.json", {"phase": "AWAITING_GEMINI", "candidate_fingerprint": None})
        tool.build(self.root)
        supplement = self.root / self.supplement_path
        data = supplement.read_bytes()
        self.write("workflow/state.json", {"phase": "AWAITING_GEMINI", "candidate_fingerprint": None,
            "reviewer_intake": {"current_fingerprint": tool.manifest(self.root)["fingerprint"], "files": [
                {"path": self.supplement_path, "sha256": tool.digest(data), "bytes": len(data), "lines": len(data.decode("utf-8").splitlines())}]}})

    def put(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def write(self, path, value):
        self.put(path, tool.encoded(value))

    def read(self, path):
        return json.loads((self.root / path).read_bytes())

    def external_coverage(self, candidate_fingerprint, files, label):
        return {"schema": 1, "input_fingerprint": candidate_fingerprint,
            "external_fingerprint": tool.fingerprint(files), "files": [
                {"path": item["path"], "sha256": item["sha256"], "ranges": [[1, item["lines"]]] if item["lines"] else [],
                 "evidence": "Synthetic test declaration; no actual review."} for item in files]}

    def round(self, folder, service, findings=None, dispositions=None):
        prefix = f"reviews/{folder}/"
        self.write(prefix + "review.json", {"status": "pending", "attestation": {"actual_review": False}})
        tool.freeze(self.root, folder)
        manifest = self.read(prefix + "input-manifest.json")
        self.write(prefix + "read-coverage.json", {"input_fingerprint": manifest["fingerprint"], "files": [
            {"path": f["path"], "sha256": f["sha256"], "ranges": [[1, f["lines"]]] if f["lines"] else [], "evidence": "Synthetic test declaration; no actual review."} for f in manifest["files"]]})
        external_fingerprint = None
        if service == "Gemini":
            external_files = tool.reviewer_intake_pins(self.root)
            external_fingerprint = tool.fingerprint(external_files)
            self.write(prefix + "supplementary-coverage.json", self.external_coverage(manifest["fingerprint"], external_files, "Gemini"))
        else:
            external_files = tool.gemini_upstream_files(self.root)
            external_fingerprint = tool.fingerprint(external_files)
            self.write(prefix + "upstream-coverage.json", self.external_coverage(manifest["fingerprint"], external_files, "Grok"))
        self.put(prefix + "report.md", b"Synthetic fixture only; no Gemini or Grok review was performed.\n")
        self.write(prefix + "findings.json", {"findings": findings or []})
        self.write(prefix + "sources.json", {"sources": ["Synthetic fixture"]})
        artifacts = {name: {"path": prefix + filename, "sha256": tool.digest((self.root / prefix / filename).read_bytes())}
                     for name, filename in (("report", "report.md"), ("findings", "findings.json"), ("sources", "sources.json"))}
        requested, actual = ("Gemini 4 Argon", "gemini-4-argon") if service == "Gemini" else ("Grok 4.7", "grok-4.7")
        # True below is simulated input to a validator, never an actual attestation.
        review = {"status": "completed", "identity": {"service_requested": service, "service_observed": service,
            "model_requested": requested, "model_observed": actual, "runtime_evidence": {"basis": "user_attestation", "model": actual, "reference": "Synthetic unit test"}},
            "attestation": {"actual_review": True, "input_fingerprint": manifest["fingerprint"], "recorded_by": "unittest fixture", "evidence": "Synthetic only"}, "artifacts": artifacts}
        if service == "Gemini":
            review["attestation"]["supplementary_fingerprint"] = external_fingerprint
        if service == "Grok":
            coverage_hash = tool.digest((self.root / (prefix + "upstream-coverage.json")).read_bytes())
            review["upstream"] = {"gemini_integration_sha256": tool.digest((self.root / "reviews/01-gemini/integration.json").read_bytes()),
                "reading_attested": True, "evidence": "Synthetic upstream reading", "external_fingerprint": external_fingerprint,
                "coverage_sha256": coverage_hash}
        self.write(prefix + "review.json", review)
        evidence = {name + "_sha256": item["sha256"] for name, item in artifacts.items()}
        evidence.update({field: tool.digest((self.root / prefix / name).read_bytes()) for field, name in (
            ("review_sha256", "review.json"), ("input_manifest_sha256", "input-manifest.json"), ("read_coverage_sha256", "read-coverage.json"))})
        if service == "Gemini":
            evidence["supplementary_coverage_sha256"] = tool.digest((self.root / prefix / "supplementary-coverage.json").read_bytes())
        else:
            evidence["upstream_coverage_sha256"] = tool.digest((self.root / prefix / "upstream-coverage.json").read_bytes())
        self.write(prefix + "integration.json", {"status": "integrated", "input_fingerprint": manifest["fingerprint"], "output_fingerprint": manifest["fingerprint"], "evidence": evidence, "dispositions": dispositions or []})

    def ready(self):
        for folder, service in tool.ROUNDS:
            self.round(folder, service)
        state = self.read("workflow/state.json")
        state.update(phase="READY_FOR_INSTALL", candidate_fingerprint=tool.manifest(self.root)["fingerprint"])
        self.write("workflow/state.json", state)

    def test_pending_is_static_valid_but_gate_closed(self):
        tool.check_static(self.root)
        with self.assertRaisesRegex(ValueError, "not READY"):
            tool.gate(self.root)
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(tool.main(["check", "--root", str(self.root)]), 0)
        self.assertFalse(json.loads(out.getvalue())["ready_for_install"])

    def test_positive_synthetic_chain(self):
        self.ready()
        self.assertTrue(tool.gate(self.root)["ready_for_install"])
        info = self.read("generated/manifest.json")
        self.assertEqual(len(info["sections"]), 22)
        self.assertEqual(len(info["payloads"]), 8)

    def test_public_visibility_contract_has_no_private_bootstrap_directives(self):
        public_paths = ("goal.md", "context/owner-intent.md", "context/owner-addendum-2026-10-24.md",
                        "workflow/00-repository-creation.md", "research/cross-vendor-capabilities.md",
                        "prompts/bootstrap-codex.md", "workflow/04-grok-review.md",
                        "workflow/05-final-integration.md")
        texts = {path: (REPO / path).read_text(encoding="utf-8") for path in public_paths}
        stale = ("private `MGrinch/Lucifer`", "Visibility: private", "--private", "isPrivate == true",
                 "private repository verified", "Keep the repo private", "Keep the repository private",
                 "private visibility before transferring", "Do not publish the repo to simplify access",
                 "private remote `main`", "verified private publication")
        for path, document in texts.items():
            with self.subTest(path=path):
                for phrase in stale:
                    self.assertNotIn(phrase, document)
        self.assertIn("--public", texts["workflow/00-repository-creation.md"])
        self.assertIn("do not change visibility", texts["workflow/00-repository-creation.md"].lower())
        self.assertIn("do not change visibility", texts["prompts/bootstrap-codex.md"].lower())

    def test_generated_and_state_do_not_change_candidate(self):
        before = tool.manifest(self.root)["fingerprint"]
        self.put("reviews/notes.txt", b"Evidence, not candidate.\n")
        self.put("generated/scratch.txt", b"Derived.\n")
        self.put("install/runs/receipt.json", b"{}")
        self.assertEqual(before, tool.manifest(self.root)["fingerprint"])

    def test_generated_drift(self):
        self.put("generated/payloads/codex.txt", b"Wrong adapter")
        with self.assertRaisesRegex(ValueError, "Generated drift"):
            tool.check_static(self.root)

    def test_stale_source_hash(self):
        self.put("sources/corpus/history.txt", b"Changed history")
        with self.assertRaisesRegex(ValueError, "Source hash mismatch"):
            tool.check_static(self.root)

    def test_changed_candidate_cannot_be_cured_by_state_only(self):
        self.ready()
        self.put("goal.md", b"Changed candidate.\n")
        self.write("workflow/state.json", {"phase": "READY_FOR_INSTALL", "candidate_fingerprint": tool.manifest(self.root)["fingerprint"]})
        with self.assertRaisesRegex(ValueError, "Integration evidence pins differ"):
            tool.gate(self.root)

    def test_partial_read_fails(self):
        self.ready()
        path = "reviews/01-gemini/read-coverage.json"
        value = self.read(path)
        next(f for f in value["files"] if f["path"] == "persona.md")["ranges"] = [[1, 10]]
        self.write(path, value)
        with self.assertRaisesRegex(ValueError, "Partial read"):
            tool.gate(self.root)

    def test_report_tampering_fails(self):
        self.ready()
        self.put("reviews/02-grok/report.md", b"Changed after integration")
        with self.assertRaisesRegex(ValueError, "artifact hash"):
            tool.gate(self.root)

    def test_wrong_round_chain_fails(self):
        self.ready()
        path = "reviews/01-gemini/integration.json"
        value = self.read(path)
        value["output_fingerprint"] = "0" * 64
        self.write(path, value)
        self.round("02-grok", "Grok")
        with self.assertRaisesRegex(ValueError, "Grok did not review"):
            tool.gate(self.root)

    def test_unknown_runtime_fails(self):
        self.ready()
        path = "reviews/01-gemini/review.json"
        value = self.read(path)
        value["identity"]["model_observed"] = None
        value["identity"]["runtime_evidence"] = None
        self.write(path, value)
        with self.assertRaisesRegex(ValueError, "Runtime identity"):
            tool.gate(self.root)
        value["identity"].update(model_requested="Different model", model_observed="Different model",
                                 runtime_evidence={"basis": "user_attestation", "model": "Different model", "reference": "Synthetic"})
        self.write(path, value)
        with self.assertRaisesRegex(ValueError, "stage model was redefined"):
            tool.gate(self.root)

    def test_blocking_deferral_fails(self):
        self.ready()
        self.round("01-gemini", "Gemini", [{"id": "G1", "blocking": True, "summary": "Synthetic blocker"}],
                   [{"finding_id": "G1", "decision": "deferred", "reason": "Fixture", "next_action": "Later"}])
        with self.assertRaisesRegex(ValueError, "Blocking"):
            tool.gate(self.root)

    def test_unlisted_worktree_and_private_files_are_never_read(self):
        before = tool.manifest(self.root)["fingerprint"]
        private = {".git", ".env", "ignored.key", "ignored.log"}
        for path in private:
            self.put(path, b"\xffprivate bytes")
        original = tool.read_bytes
        def guarded(root, path):
            self.assertNotIn(path, private)
            return original(root, path)
        with mock.patch.object(tool, "read_bytes", side_effect=guarded):
            self.assertEqual(before, tool.manifest(self.root)["fingerprint"])

    def test_forged_frozen_dimensions_or_inventory_fail(self):
        self.ready()
        path = "reviews/01-gemini/input-manifest.json"
        original = self.read(path)
        for operation in ("short-lines", "omit-corpus"):
            value = json.loads(json.dumps(original))
            if operation == "short-lines":
                next(f for f in value["files"] if f["path"] == "persona.md")["lines"] = 1
            else:
                value["files"] = [f for f in value["files"] if f["path"] != "sources/corpus/history.txt"]
                value["fingerprint"] = tool.fingerprint(value["files"])
            self.write(path, value)
            with self.assertRaisesRegex(ValueError, "Frozen bytes/metadata"):
                tool.gate(self.root)

    def test_allowlist_cannot_omit_pinned_corpus(self):
        value = self.read(tool.ALLOWLIST)
        value["files"].remove("sources/corpus/history.txt")
        self.write(tool.ALLOWLIST, value)
        with self.assertRaisesRegex(ValueError, "Source omitted"):
            tool.manifest(self.root)

    def test_gemini_repin_invalidates_grok(self):
        self.ready()
        prefix = "reviews/01-gemini/"
        self.put(prefix + "report.md", b"Changed synthetic report, repinned by first integrator.\n")
        review = self.read(prefix + "review.json")
        new_hash = tool.digest((self.root / prefix / "report.md").read_bytes())
        review["artifacts"]["report"]["sha256"] = new_hash
        self.write(prefix + "review.json", review)
        integration = self.read(prefix + "integration.json")
        integration["evidence"].update(report_sha256=new_hash, review_sha256=tool.digest((self.root / prefix / "review.json").read_bytes()))
        self.write(prefix + "integration.json", integration)
        with self.assertRaisesRegex(ValueError, "Grok upstream coverage input fingerprint mismatch"):
            tool.gate(self.root)

    def test_pending_refreeze_preserves_old_snapshot_and_versions_new_candidate(self):
        prefix = "reviews/01-gemini/"
        self.write(prefix + "review.json", {"status": "pending", "attestation": {"actual_review": False}})
        self.write(prefix + "input-manifest.json", {"schema": 1, "status": "NOT_PREPARED", "fingerprint": None, "files": []})
        first = tool.freeze(self.root, "01-gemini")
        self.assertTrue(first["changed"])
        old_manifest = self.read(prefix + "input-manifest.json")
        old_path = old_manifest["snapshot_path"]
        old_bytes = (self.root / old_path / "goal.md").read_bytes()
        self.assertFalse(tool.freeze(self.root, "01-gemini")["changed"])
        self.put("goal.md", b"New candidate")
        second = tool.freeze(self.root, "01-gemini")
        self.assertTrue(second["changed"])
        new_manifest = self.read(prefix + "input-manifest.json")
        self.assertNotEqual(old_path, new_manifest["snapshot_path"])
        self.assertEqual((self.root / old_path / "goal.md").read_bytes(), old_bytes)
        self.assertEqual(tool.validate_snapshot(self.root, prefix, old_manifest)["fingerprint"], old_manifest["fingerprint"])
        self.assertFalse(tool.freeze(self.root, "01-gemini")["changed"])

    def test_pristine_manifest_cannot_bypass_legacy_snapshot(self):
        prefix = "reviews/01-gemini/"
        self.write(prefix + "review.json", {"status": "pending", "attestation": {"actual_review": False}})
        self.write(prefix + "input-manifest.json", {"schema": 1, "status": "NOT_PREPARED", "fingerprint": None, "files": []})
        (self.root / (prefix + "input-snapshot")).mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "Pristine input manifest cannot bypass an existing legacy snapshot"):
            tool.freeze(self.root, "01-gemini")

    def test_completed_review_cannot_be_refrozen(self):
        prefix = "reviews/01-gemini/"
        self.write(prefix + "review.json", {"status": "pending", "attestation": {"actual_review": False}})
        tool.freeze(self.root, "01-gemini")
        self.write(prefix + "review.json", {"status": "completed", "attestation": {"actual_review": True}})
        self.put("goal.md", b"New candidate")
        with self.assertRaisesRegex(ValueError, "Cannot freeze a completed/attested review"):
            tool.freeze(self.root, "01-gemini")

    def test_gemini_supplementary_coverage_is_required(self):
        self.ready()
        path = "reviews/01-gemini/supplementary-coverage.json"
        value = self.read(path)
        value["files"] = []
        self.write(path, value)
        with self.assertRaisesRegex(ValueError, "Incomplete Gemini supplementary coverage inventory"):
            tool.gate(self.root)

    def test_changed_gemini_supplement_fails_its_pin(self):
        self.ready()
        self.put(self.supplement_path, b"Changed after pin.\n")
        with self.assertRaisesRegex(ValueError, "Reviewer intake hash mismatch"):
            tool.gate(self.root)

    def test_grok_upstream_coverage_is_required(self):
        self.ready()
        path = "reviews/02-grok/upstream-coverage.json"
        value = self.read(path)
        value["files"] = []
        self.write(path, value)
        with self.assertRaisesRegex(ValueError, "Incomplete Grok upstream coverage inventory"):
            tool.gate(self.root)


if __name__ == "__main__":
    unittest.main()
