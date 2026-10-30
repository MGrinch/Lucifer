#!/usr/bin/env python3
"""Build deterministic reference artifacts and validate attested review gates."""
import argparse
from datetime import date
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath

ALGORITHM = "sha256-path-hash-json-v1"
PAYLOADS = ("native_compact", "native_extended", "project", "codex", "dot", "memory", "voice", "subagent")
EXCLUDED = (".git/", "generated/", "reviews/", "install/runs/", "runs/", "outputs/", "private/")
EXACT_EXCLUDED = {"workflow/state.json", "workflow/input-manifest.json"}
NAVIGATION = ("README.md", "start here.md", "goal.md", "persona.md")
ALLOWLIST = "workflow/review-files.json"
ROUNDS = (("01-gemini", "Gemini"), ("02-grok", "Grok"))
REQUESTED_MODELS = {"Gemini": "Gemini 4 Argon", "Grok": "Grok 4.7"}
MODEL_ALIASES = {"gemini 4 argon": "gemini-4-argon", "gemini-4-argon": "gemini-4-argon",
                 "grok 4.7": "grok-4.7", "grok-4.7": "grok-4.7"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def safe_path(root, relative):
    require(isinstance(relative, str) and relative and "\\" not in relative, "Invalid relative path")
    p = PurePosixPath(relative)
    require(not p.is_absolute() and ".." not in p.parts and p.as_posix() == relative, "Unsafe path: " + relative)
    target = root.joinpath(*p.parts)
    require(not any(x.is_symlink() for x in [target, *target.parents] if x != root.parent), "Symlink unsupported: " + relative)
    return target


def read_bytes(root, relative):
    return safe_path(root, relative).read_bytes()


def read_json(root, relative):
    value = json.loads(read_bytes(root, relative))
    require(isinstance(value, dict), "Expected JSON object: " + relative)
    return value


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def valid_hash(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def model_key(label):
    return MODEL_ALIASES.get(label.strip().casefold(), label.strip())


def fingerprint(files):
    pairs = [{"path": f["path"], "sha256": f["sha256"]} for f in sorted(files, key=lambda f: f["path"])]
    return digest(json.dumps(pairs, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def allowlist(root):
    value = read_json(root, ALLOWLIST)
    paths = value.get("files")
    require(value.get("schema") == 1 and isinstance(paths, list) and all(nonempty(p) for p in paths), "Invalid review allowlist")
    require(len(set(paths)) == len(paths), "Duplicate allowlist path")
    require(set(NAVIGATION + (ALLOWLIST, "sources/manifest.json")).issubset(paths), "Allowlist omits required inputs")
    for path in paths:
        safe_path(root, path)
        p = PurePosixPath(path)
        require(path != ".git" and path not in EXACT_EXCLUDED and not path.startswith(EXCLUDED)
                and "__pycache__" not in p.parts and p.suffix != ".pyc", "Excluded path in allowlist: " + path)
        require(not any(part.startswith(".env") or part in ("id_rsa", "id_ed25519") for part in p.parts)
                and p.suffix.lower() not in (".key", ".pem", ".p12", ".pfx", ".log"), "Private/secret/log path in allowlist: " + path)
    return sorted(paths)


def validate_sources(root, included=None):
    pins = read_json(root, "sources/manifest.json").get("files")
    require(isinstance(pins, list) and pins, "Source manifest needs pinned files")
    seen = set()
    for pin in pins:
        require(isinstance(pin, dict) and nonempty(pin.get("path")), "Invalid source pin")
        path = pin["path"]
        require(path.startswith("sources/") and path != "sources/manifest.json" and path not in seen, "Invalid/duplicate source pin")
        require(included is None or path in included, "Source omitted from review inventory: " + path)
        data = read_bytes(root, path)
        require(pin.get("sha256") == digest(data), "Source hash mismatch: " + path)
        require("bytes" not in pin or pin["bytes"] == len(data), "Source size mismatch: " + path)
        seen.add(path)


def manifest(root):
    paths, files = allowlist(root), []
    validate_sources(root, paths)
    for relative in paths:
        data = read_bytes(root, relative)
        files.append({"path": relative, "sha256": digest(data), "bytes": len(data), "lines": len(data.decode("utf-8").splitlines())})
    return {"schema": 1, "algorithm": ALGORITHM, "fingerprint": fingerprint(files), "files": files}


def validate_manifest(root, value):
    require(value.get("schema") == 1 and value.get("algorithm") == ALGORITHM, "Unknown manifest schema/algorithm")
    files = value.get("files")
    require(isinstance(files, list) and files, "Manifest needs input files")
    seen = set()
    for item in files:
        require(isinstance(item, dict), "Malformed manifest file")
        path = item.get("path")
        safe_path(root, path)
        require(path not in seen and valid_hash(item.get("sha256")), "Duplicate file or invalid hash: " + path)
        require(all(type(item.get(k)) is int and item[k] >= 0 for k in ("bytes", "lines")), "Invalid file dimensions: " + path)
        require((item["bytes"] == 0) == (item["lines"] == 0), "Inconsistent empty file: " + path)
        seen.add(path)
    require(set(NAVIGATION + (ALLOWLIST, "sources/manifest.json")).issubset(seen), "Input manifest omits required canonical inputs")
    require(value.get("fingerprint") == fingerprint(files), "Input manifest fingerprint mismatch")
    return files


def validate_snapshot(root, prefix, expected):
    snapshot_path = expected.get("snapshot_path", prefix + "input-snapshot")
    require(isinstance(snapshot_path, str) and snapshot_path.startswith(prefix), "Frozen snapshot path outside review round")
    snapshot = safe_path(root, snapshot_path)
    require(snapshot.is_dir(), "Frozen input snapshot missing")
    inventory = set()
    for path in snapshot.rglob("*"):
        require(not path.is_symlink(), "Symlink in input snapshot")
        if path.is_file():
            inventory.add(path.relative_to(snapshot).as_posix())
    require(inventory == set(allowlist(snapshot)), "Snapshot inventory differs from frozen allowlist")
    actual = manifest(snapshot)
    require(all(expected.get(k) == actual[k] for k in actual), "Frozen bytes/metadata differ from input manifest")
    return actual


def freeze(root, folder):
    require(folder in dict(ROUNDS), "Select --round 01-gemini or 02-grok")
    prefix, current = f"reviews/{folder}/", manifest(root)
    review = read_json(root, prefix + "review.json")
    manifest_path = safe_path(root, prefix + "input-manifest.json")
    pending = review.get("status") == "pending" and review.get("attestation", {}).get("actual_review") is not True
    legacy_target = safe_path(root, prefix + "input-snapshot")
    require(not legacy_target.exists() or manifest_path.exists(), "Legacy frozen snapshot has no manifest; preserve and investigate")
    old = read_json(root, prefix + "input-manifest.json") if manifest_path.exists() else None
    pristine = old == {"schema": 1, "status": "NOT_PREPARED", "fingerprint": None, "files": []}
    require(not pristine or not legacy_target.exists(),
            "Pristine input manifest cannot bypass an existing legacy snapshot; preserve and investigate")
    old_matches = isinstance(old, dict) and all(old.get(key) == current[key] for key in current)
    if old_matches:
        old_snapshot = old.get("snapshot_path", prefix + "input-snapshot")
        if safe_path(root, old_snapshot).exists():
            require(validate_snapshot(root, prefix, old) == current, "Existing frozen input is corrupt; preserve and investigate")
            return {"ok": True, "changed": False, "fingerprint": current["fingerprint"]}
    require(pending, "Cannot freeze a completed/attested review")
    if manifest_path.exists():
        require(pristine or isinstance(old, dict), "Invalid existing input manifest")
        if not pristine and (legacy_target.exists() or old.get("snapshot_path")):
            require(validate_snapshot(root, prefix, old), "Existing frozen input is invalid; preserve and investigate")
    elif legacy_target.exists():
        raise ValueError("Legacy frozen snapshot has no manifest; preserve and investigate")
    target_relative = prefix + "input-snapshots/" + current["fingerprint"]
    target = safe_path(root, target_relative)
    require(not target.exists(), "Versioned snapshot path already exists; preserve and investigate")
    target.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".freeze-", dir=target.parent) as work:
        stage = Path(work) / "input-snapshot"
        stage.mkdir()
        for item in current["files"]:
            data = read_bytes(root, item["path"])
            require(digest(data) == item["sha256"], "Candidate changed during freeze")
            destination = safe_path(stage, item["path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        require(manifest(stage) == current, "Candidate metadata changed during freeze")
        require(not target.exists(), "Snapshot appeared during freeze")
        stage.rename(target)
    frozen = {**current, "snapshot_path": target_relative}
    manifest_path.write_bytes(encoded(frozen))
    return {"ok": True, "changed": True, "fingerprint": current["fingerprint"], "snapshot_path": target_relative,
            "state": "frozen_not_read_or_reviewed"}


def fenced_block(document, kind, name, language):
    start, end = f"<!-- BEGIN {kind}:{name} -->", f"<!-- END {kind}:{name} -->"
    require(document.count(start) == document.count(end) == 1, "Missing/duplicate markers: " + name)
    require(document.index(start) < document.index(end), "Reversed markers: " + name)
    block = document.split(start, 1)[1].split(end, 1)[0].strip()
    match = re.fullmatch(r"~~~" + language + r"\n(.*?)\n~~~", block, re.S)
    require(match is not None, "Unexpected fence: " + name)
    return match.group(1)


def derived(root):
    raw = read_bytes(root, "persona.md")
    document = raw.decode("utf-8").replace("\r\n", "\n")
    source_hash, outputs, payload_info = digest(raw), {}, {}
    for side in ("BEGIN", "END"):
        markers = re.findall(r"^<!-- " + side + r" PAYLOAD:([^ ]+) -->$", document, re.M)
        require(sorted(markers) == sorted(PAYLOADS), "Expected exactly eight unique payload markers")
    for name in PAYLOADS:
        value = fenced_block(document, "PAYLOAD", name, "text")
        data, path = value.encode("utf-8"), f"generated/payloads/{name}.txt"
        chars, units = len(value), len(value.encode("utf-16-le")) // 2
        limit = {"native_compact": 1500, "native_extended": 5000}.get(name)
        require(limit is None or max(chars, units) <= limit, "Payload too long: " + name)
        outputs[path] = data
        payload_info[name] = {"path": path, "sha256": digest(data), "bytes": len(data), "characters": chars, "utf16_units": units}
    tests = fenced_block(document, "TESTS", "text_jsonl", "jsonl")
    records = [json.loads(line) for line in tests.splitlines() if line.strip()]
    require(all(isinstance(r, dict) for r in records), "Every test must be an object")
    require(len(records) == 48 and {r.get("id") for r in records} == {f"T{i:02}" for i in range(1, 49)}, "Expected unique T01..T48")
    require(all(sum(r.get("split") == s for r in records) == 24 for s in ("development", "final")), "Expected 24/24 test split")
    voice_ids = re.findall(r"^\|\s*(V\d{2})\s*\|", document, re.M)
    require(sorted(voice_ids) == [f"V{i:02}" for i in range(1, 11)], "Expected unique V01..V10")
    outputs["generated/tests/text.jsonl"] = (tests + "\n").encode("utf-8")
    lines = document.splitlines(keepends=True)
    starts = [(i, int(m.group(1))) for i, line in enumerate(lines) if (m := re.match(r"^## (\d+)\. ", line))]
    require([n for _, n in starts] == list(range(1, 22)), "Expected ordered sections 1..21")
    boundaries = [(0, 0), *starts, (len(lines), 22)]
    definitions = [(i + 1, line) for i, line in enumerate(lines) if re.match(r"^\[[^\]]+\]:\s+", line)]
    sections = []
    for (start, number), (end, _) in zip(boundaries, boundaries[1:]):
        path = "generated/sections/" + ("00-preamble.md" if number == 0 else f"{number:02}.md")
        header = f"<!-- GENERATED; DO NOT EDIT. persona.md lines {start + 1}-{end}; raw SHA256 {source_hash}. -->\n\n"
        refs = "\n\n<!-- Reference definitions copied from original lines " + ",".join(str(i) for i, _ in definitions) + ". -->\n"
        outputs[path] = (header + "".join(lines[start:end]) + refs + "".join(line for _, line in definitions)).encode("utf-8")
        sections.append({"path": path, "source_lines": [start + 1, end], "sha256": digest(outputs[path])})
    info = {"schema": 1, "canonical": {"path": "persona.md", "sha256": source_hash, "bytes": len(raw)},
            "state": "derived_only_not_reviewed_or_installed", "payloads": payload_info, "sections": sections,
            "tests": {"path": "generated/tests/text.jsonl", "sha256": digest(outputs["generated/tests/text.jsonl"]), "count": 48, "splits": {"development": 24, "final": 24}}}
    outputs["generated/manifest.json"] = encoded(info)
    return outputs


def build(root):
    outputs = derived(root)
    directory = safe_path(root, "generated")
    if directory.exists():
        for path in directory.rglob("*"):
            require(not path.is_symlink(), "Symlink in generated tree")
            if path.is_file() and path.relative_to(root).as_posix() not in outputs:
                path.unlink()
    for relative, data in outputs.items():
        target = safe_path(root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return {"ok": True, "generated_files": len(outputs), "state": "derived_only_not_reviewed_or_installed"}


def check_static(root):
    for name in NAVIGATION:
        require(safe_path(root, name).is_file(), "Missing navigation/source: " + name)
    expected = derived(root)
    for relative, data in expected.items():
        require(safe_path(root, relative).is_file(), "Missing generated file: " + relative)
        require(read_bytes(root, relative) == data, "Generated drift: " + relative)
    actual = {p.relative_to(root).as_posix() for p in safe_path(root, "generated").rglob("*") if p.is_file()}
    require(actual == set(expected), "Unexpected generated files; rebuild")
    validate_sources(root, allowlist(root))
    reviewer_intake_pins(root)


def reviewer_intake_pins(root):
    state = read_json(root, "workflow/state.json")
    intake = state.get("reviewer_intake", {})
    require(isinstance(intake, dict), "Invalid reviewer intake")
    pins = intake.get("files", [])
    require(isinstance(pins, list) and pins, "Reviewer intake must pin at least one supplement")
    normalized, seen = [], set()
    for pin in pins:
        require(isinstance(pin, dict) and nonempty(pin.get("path")), "Invalid reviewer intake pin")
        path = pin["path"]
        require(path.startswith("reviews/01-gemini/supplements/") and path not in seen,
                "Reviewer intake path outside Gemini supplements or duplicated: " + path)
        data = read_bytes(root, path)
        lines = len(data.decode("utf-8").splitlines())
        require(valid_hash(pin.get("sha256")) and pin["sha256"] == digest(data), "Reviewer intake hash mismatch: " + path)
        require(type(pin.get("bytes")) is int and pin["bytes"] == len(data), "Reviewer intake byte count mismatch: " + path)
        require(type(pin.get("lines")) is int and pin["lines"] == lines, "Reviewer intake line count mismatch: " + path)
        normalized.append({"path": path, "sha256": pin["sha256"], "bytes": len(data), "lines": lines})
        seen.add(path)
    return sorted(normalized, key=lambda item: item["path"])


def validate_file_read_coverage(files, entries, label):
    require(isinstance(entries, list) and len(entries) == len(files), "Incomplete " + label + " inventory")
    by_path = {entry.get("path"): entry for entry in entries if isinstance(entry, dict)}
    require(len(by_path) == len(entries) and set(by_path) == {item["path"] for item in files}, label + " paths mismatch")
    for item in files:
        entry = by_path[item["path"]]
        require(entry.get("sha256") == item["sha256"] and nonempty(entry.get("evidence")),
                "Unpinned/unattested " + label + " reading: " + item["path"])
        ranges = entry.get("ranges")
        require(isinstance(ranges, list), "Missing " + label + " ranges: " + item["path"])
        for span in ranges:
            require(isinstance(span, list) and len(span) == 2 and all(type(number) is int for number in span),
                    "Invalid " + label + " range: " + item["path"])
            require(1 <= span[0] <= span[1] <= item["lines"], "Out-of-bounds " + label + " range: " + item["path"])
        next_line = 1
        for start, end in sorted(ranges):
            require(start <= next_line, label + " coverage gap: " + item["path"])
            next_line = max(next_line, end + 1)
        require(next_line == item["lines"] + 1, "Partial " + label + " read: " + item["path"])


def validate_external_coverage(candidate_fingerprint, files, value, label):
    require(value.get("schema") == 1, "Unknown " + label + " schema")
    require(value.get("input_fingerprint") == candidate_fingerprint, label + " candidate fingerprint mismatch")
    external_fingerprint = fingerprint(files)
    require(value.get("external_fingerprint") == external_fingerprint, label + " input fingerprint mismatch")
    validate_file_read_coverage(files, value.get("files"), label)
    return external_fingerprint


def gemini_upstream_files(root):
    prefix = "reviews/01-gemini/"
    review = read_json(root, prefix + "review.json")
    artifacts = review.get("artifacts", {})
    require(isinstance(artifacts, dict) and set(artifacts) == {"report", "findings", "sources"}, "Invalid Gemini upstream artifacts")
    paths = [prefix + name for name in ("review.json", "input-manifest.json", "read-coverage.json", "supplementary-coverage.json", "integration.json")]
    for name in ("report", "findings", "sources"):
        item = artifacts[name]
        require(isinstance(item, dict) and isinstance(item.get("path"), str) and item["path"].startswith(prefix),
                "Invalid Gemini upstream artifact path: " + name)
        paths.append(item["path"])
    paths.extend(item["path"] for item in reviewer_intake_pins(root))
    files = []
    for path in sorted(set(paths)):
        data = read_bytes(root, path)
        files.append({"path": path, "sha256": digest(data), "bytes": len(data),
                      "lines": len(data.decode("utf-8").splitlines())})
    return files


def coverage(root, input_manifest, value):
    files = validate_manifest(root, input_manifest)
    require(value.get("input_fingerprint") == input_manifest["fingerprint"], "Coverage input mismatch")
    validate_file_read_coverage(files, value.get("files"), "read-coverage")


def validate_cross_service_substitute(root, folder, service, identity, actual):
    """Validate explicit owner-authorized Codex completion, never authenticate a vendor."""
    substitute = identity.get("accepted_substitute")
    require(folder == "02-grok" and service == "Grok" and identity.get("service_observed") == "Codex",
            "Unsupported cross-service substitution")
    require(isinstance(substitute, dict) and substitute.get("service") == "Codex"
            and nonempty(substitute.get("model")) and model_key(substitute["model"]) == model_key(actual)
            and nonempty(substitute.get("evidence")), "Cross-service substitution needs explicit service/model/evidence")
    path = substitute.get("authorization_path")
    expected_hash = substitute.get("authorization_sha256")
    require(isinstance(path, str) and path.startswith(f"reviews/{folder}/") and path.endswith(".json"),
            "Substitution authorization must be a same-round JSON record")
    raw = read_bytes(root, path)
    require(valid_hash(expected_hash) and digest(raw) == expected_hash, "Substitution authorization hash mismatch")
    authorization = json.loads(raw)
    require(isinstance(authorization, dict), "Substitution authorization must be an object")
    require(type(authorization.get("schema")) is int and authorization["schema"] == 1
            and authorization.get("kind") == "owner_authorized_review_substitution",
            "Invalid substitution authorization schema/kind")
    require(authorization.get("round") == folder
            and authorization.get("requested_service") == service
            and authorization.get("actual_service") == identity["service_observed"],
            "Substitution authorization service/round mismatch")
    for field, expected in (("requested_model", identity["model_requested"]), ("actual_model", actual)):
        require(nonempty(authorization.get(field)) and model_key(authorization[field]) == model_key(expected),
                "Substitution authorization model mismatch: " + field)
    recorded_date = authorization.get("date")
    require(isinstance(recorded_date, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", recorded_date) is not None,
            "Substitution authorization date missing/invalid")
    try:
        date.fromisoformat(recorded_date)
    except ValueError as exc:
        raise ValueError("Substitution authorization date missing/invalid") from exc
    require(authorization.get("scope") == "complete_unfinished_second_review",
            "Substitution authorization scope mismatch")
    require(nonempty(authorization.get("owner_authorization_quote")) and nonempty(authorization.get("recorded_by")),
            "Substitution authorization owner quote/recorder missing")
    require(authorization.get("original_grok_completion_attested") is False,
            "Substitution must not attest original Grok completion")


def validate_round(root, folder, service):
    prefix = f"reviews/{folder}/"
    review = read_json(root, prefix + "review.json")
    require(review.get("status") == "completed", service + " review is pending")
    identity = review.get("identity", {})
    require(isinstance(identity, dict), "Invalid reviewer identity")
    require(identity.get("service_requested") == service, "Wrong requested reviewer")
    for field in ("service_observed", "model_requested", "model_observed"):
        require(field in identity and (identity[field] is None or nonempty(identity[field])), "Missing/invalid identity field: " + field)
    runtime = identity.get("runtime_evidence")
    require(isinstance(runtime, dict) and runtime.get("basis") in ("observed_ui", "api_metadata", "user_attestation", "runtime_metadata"), "Runtime identity evidence missing")
    if runtime["basis"] == "runtime_metadata":
        require(identity.get("service_observed") == "Codex" and runtime.get("service") == "Codex"
                and runtime.get("source") == "codex_orchestration_metadata",
                "Runtime metadata must identify the observed Codex orchestration source")
    require(nonempty(runtime.get("reference")) and nonempty(runtime.get("model")), "Runtime evidence needs model and reference")
    actual = identity.get("model_observed") or runtime["model"]
    require(model_key(actual) == model_key(runtime["model"]), "Observed model contradicts runtime evidence")
    require(nonempty(identity.get("model_requested")), "Requested model missing")
    require(model_key(identity["model_requested"]) == model_key(REQUESTED_MODELS[service]), "Requested stage model was redefined")
    substitute = identity.get("accepted_substitute")
    if isinstance(substitute, dict) and substitute.get("service") is not None:
        require(identity.get("service_observed") == substitute["service"], "Substitute service contradicts observed reviewer")
    if identity.get("service_observed") not in (None, service):
        validate_cross_service_substitute(root, folder, service, identity, actual)
    if model_key(actual) != model_key(identity["model_requested"]):
        substitute = identity.get("accepted_substitute")
        require(isinstance(substitute, dict) and nonempty(substitute.get("model")) and model_key(substitute["model"]) == model_key(actual) and nonempty(substitute.get("evidence")), "Unapproved model substitution")
    input_manifest = read_json(root, prefix + "input-manifest.json")
    validate_snapshot(root, prefix, input_manifest)
    reading = read_json(root, prefix + "read-coverage.json")
    coverage(root, input_manifest, reading)
    attestation = review.get("attestation", {})
    require(isinstance(attestation, dict), "Invalid attestation")
    require(attestation.get("actual_review") is True and attestation.get("input_fingerprint") == input_manifest["fingerprint"], "No actual review attestation for this input")
    require(all(nonempty(attestation.get(k)) for k in ("recorded_by", "evidence")), "Review provenance missing")
    external_coverage_hash = None
    if service == "Gemini":
        intake = read_json(root, "workflow/state.json").get("reviewer_intake", {})
        supplements = reviewer_intake_pins(root)
        if supplements:
            require(intake.get("current_fingerprint") == input_manifest["fingerprint"], "Gemini supplements are pinned to a different candidate")
            external = read_json(root, prefix + "supplementary-coverage.json")
            external_fingerprint = validate_external_coverage(input_manifest["fingerprint"], supplements, external, "Gemini supplementary coverage")
            require(attestation.get("supplementary_fingerprint") == external_fingerprint, "Gemini attestation omits supplementary input fingerprint")
            external_coverage_hash = digest(read_bytes(root, prefix + "supplementary-coverage.json"))
    else:
        upstream_files = gemini_upstream_files(root)
        external = read_json(root, prefix + "upstream-coverage.json")
        external_fingerprint = validate_external_coverage(input_manifest["fingerprint"], upstream_files, external, "Grok upstream coverage")
        upstream = review.get("upstream", {})
        require(isinstance(upstream, dict) and upstream.get("external_fingerprint") == external_fingerprint,
                "Grok attestation omits Gemini upstream input fingerprint")
        external_coverage_hash = digest(read_bytes(root, prefix + "upstream-coverage.json"))
        require(upstream.get("coverage_sha256") == external_coverage_hash, "Grok upstream coverage hash mismatch")
    artifacts, hashes = review.get("artifacts", {}), {}
    require(isinstance(artifacts, dict) and set(artifacts) == {"report", "findings", "sources"}, "Expected three review artifacts")
    for name in ("report", "findings", "sources"):
        item = artifacts.get(name, {})
        require(isinstance(item, dict), "Invalid review artifact")
        path = item.get("path", "")
        require(isinstance(path, str) and path.startswith(prefix), "Artifact outside review round")
        data = read_bytes(root, path)
        require(data.strip() and item.get("sha256") == digest(data), "Review artifact hash/content mismatch: " + name)
        hashes[name + "_sha256"] = digest(data)
    require(len({artifacts[k]["path"] for k in artifacts}) == 3, "Review artifacts must be distinct")
    findings = read_json(root, artifacts["findings"]["path"]).get("findings")
    sources = read_json(root, artifacts["sources"]["path"]).get("sources")
    require(isinstance(findings, list) and isinstance(sources, list), "Invalid findings/sources records")
    ids = set()
    for f in findings:
        require(isinstance(f, dict) and nonempty(f.get("id")) and f["id"] not in ids, "Duplicate/invalid finding")
        require(type(f.get("blocking")) is bool and nonempty(f.get("summary")), "Finding needs blocking flag and summary")
        ids.add(f["id"])
    integration = read_json(root, prefix + "integration.json")
    require(integration.get("status") == "integrated", service + " integration is pending")
    require(integration.get("input_fingerprint") == input_manifest["fingerprint"] and valid_hash(integration.get("output_fingerprint")), "Integration fingerprint mismatch")
    for field, path in (("review_sha256", "review.json"), ("input_manifest_sha256", "input-manifest.json"), ("read_coverage_sha256", "read-coverage.json")):
        hashes[field] = digest(read_bytes(root, prefix + path))
    if external_coverage_hash is not None:
        hashes["supplementary_coverage_sha256" if service == "Gemini" else "upstream_coverage_sha256"] = external_coverage_hash
    require(integration.get("evidence") == hashes, "Integration evidence pins differ")
    if service == "Grok":
        upstream = review.get("upstream", {})
        require(isinstance(upstream, dict) and upstream.get("reading_attested") is True and nonempty(upstream.get("evidence")), "Grok upstream reading is not attested")
        require(upstream.get("gemini_integration_sha256") == digest(read_bytes(root, "reviews/01-gemini/integration.json")), "Grok upstream Gemini evidence changed")
    decisions = integration.get("dispositions")
    require(isinstance(decisions, list) and len(decisions) == len(findings), "Every finding needs one disposition")
    by_id = {d.get("finding_id"): d for d in decisions if isinstance(d, dict)}
    require(len(by_id) == len(decisions) and set(by_id) == ids, "Disposition IDs mismatch")
    for f in findings:
        d = by_id[f["id"]]
        require(nonempty(d.get("reason")), "Disposition reason missing")
        choice = d.get("decision")
        require(choice in ("accepted", "rejected", "deferred"), "Unknown disposition")
        if choice == "accepted":
            require(nonempty(d.get("verification")) and isinstance(d.get("change_refs"), list) and d["change_refs"] and all(nonempty(x) for x in d["change_refs"]), "Accepted finding lacks change/verification evidence")
        if choice == "deferred":
            require(not f["blocking"] and nonempty(d.get("next_action")), "Blocking or unexplained deferral")
    return integration


def gate(root):
    state = read_json(root, "workflow/state.json")
    require(state.get("phase") == "READY_FOR_INSTALL", "Workflow is not READY_FOR_INSTALL")
    current = manifest(root)["fingerprint"]
    require(state.get("candidate_fingerprint") == current, "State candidate is stale or missing")
    first, second = [validate_round(root, folder, service) for folder, service in ROUNDS]
    require(first["output_fingerprint"] == second["input_fingerprint"], "Grok did not review the integrated Gemini candidate")
    require(second["output_fingerprint"] == current, "Final integration is stale")
    return {"ready_for_install": True, "fingerprint": current, "evidence": "recorded attestations and hashes; not vendor authentication or installation"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check", "manifest", "freeze", "gate"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--round", dest="round_name", choices=[folder for folder, _ in ROUNDS])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        require(root.is_dir(), "Repository directory missing")
        if args.command == "build":
            result = build(root)
        elif args.command == "manifest":
            result = manifest(root)
        elif args.command == "freeze":
            result = freeze(root, args.round_name)
        else:
            check_static(root)
            if args.command == "gate":
                result = {"ok": True, **gate(root)}
            else:
                result = {"ok": True, "static_checks": "passed"}
                try:
                    result.update(gate(root))
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    result.update({"ready_for_install": False, "gate_blocker": str(exc)})
                    if read_json(root, "workflow/state.json").get("phase") == "READY_FOR_INSTALL":
                        raise ValueError("Invalid READY state: " + str(exc)) from exc
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
