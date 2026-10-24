# Local build and review validation

Requires an already available Python 3.10 or later; standard library only. No network, model calls, source-command execution, native app automation, or account changes occur.

```sh
python3 tools/lucifer.py build
python3 tools/lucifer.py check
python3 tools/lucifer.py manifest
python3 tools/lucifer.py freeze --round 01-gemini
# After actual Gemini integration, freeze the updated Grok input:
python3 tools/lucifer.py freeze --round 02-grok
python3 tools/lucifer.py gate
python3 -m unittest discover -s tests -v
```

Use `python` or the appropriate Windows Python launcher when that is the available interpreter. Every command accepts `--root PATH`; by default the repository containing this script is used. A failure returns a nonzero exit code and a JSON error. Do not change the validator to make missing reviews pass.

## Commands and limits

- `build` owns the disposable `generated/` tree. It writes eight payloads, the 48 JSONL test definitions, 22 traceable reading sections, and a deterministic generated manifest. It removes stale generated files. It never changes the canonical specification, reviews, workflow state, sources, or settings.
- `check` verifies required navigation, source byte hashes, extraction, exact generated content, payload limits, text-case IDs/splits, voice-case IDs, and reports the readiness gate separately. A valid pending repository can pass static checks while `ready_for_install` is false. An invalid claimed `READY_FOR_INSTALL` fails `check`.
- `manifest` prints the current candidate manifest from the explicit reviewed-file allowlist. Redirecting it to `workflow/input-manifest.json` does not alter the candidate fingerprint. A printed manifest alone is not frozen evidence.
- `freeze --round ...` saves the current manifest plus byte-exact inputs under that round's `input-snapshot/`. It never marks a file read or a review complete. A previously frozen identical input is a no-op; changed snapshots, changed real manifests, and missing snapshots for completed/attested reviews cannot be overwritten. The pristine pending placeholder `{schema:1,status:"NOT_PREPARED",fingerprint:null,files:[]}` can be initialized when no actual-review attestation or snapshot exists. Stage temporary copies are verified before becoming the snapshot.
- `gate` first performs static checks, then requires the complete sequential review/integration evidence below and the exact current candidate. The initial repository intentionally fails this gate.

These tools check record consistency, byte integrity and attested reading coverage. They cannot authenticate a vendor, independently prove attention to every line, establish that a reported experiment happened, or certify native installation, behavior or voice. A truthful review capture and human/integrator assessment remain necessary. Unit tests use temporary synthetic records and do not constitute Gemini/Grok reviews.

## Candidate fingerprint

`workflow/review-files.json` is the sole input inventory: `{schema:1, files:["relative/path", ...]}`. It includes itself, required navigation, `sources/manifest.json`, every pinned local source, and all authored material selected for review. The owner must update it deliberately when a reviewed file is added or removed. `manifest` reads only these paths; it never crawls arbitrary repository files or reads unlisted `.env`, key, log, or Git worktree metadata files.

The following paths cannot be allowlisted:

```text
.git/
generated/
reviews/
install/runs/
runs/
outputs/
private/
```

Also reject the exact `.git` worktree file, `workflow/state.json`, `workflow/input-manifest.json`, every `__pycache__` directory, and `.pyc` files. Secret-like `.env*`, private-key names/extensions, and `.log` files cannot be allowlisted. Other authored installation instructions and the authored `.gitignore` remain included when explicitly listed; arbitrary gitignore rules are not interpreted. Symlinks and paths outside the repository are unsupported. Binary evidence should remain an explicitly referenced external item unless a later authorized schema adds a suitable review-coverage method.

For each included file, record its repository-relative POSIX path, raw SHA-256, bytes, and UTF-8 text line count. The fingerprint is SHA-256 over UTF-8 compact JSON of the sorted `{path, sha256}` pairs, with object keys sorted, no spaces, and `ensure_ascii=False`. The algorithm label is `sha256-path-hash-json-v1`. File metadata in the manifest is not a substitute for the actual raw-byte hash.

```json
{
  "schema": 1,
  "algorithm": "sha256-path-hash-json-v1",
  "fingerprint": "COMPUTED",
  "files": [{"path": "persona.md", "sha256": "COMPUTED", "bytes": 194576, "lines": 1869}]
}
```

This abbreviated example is not a valid full input manifest. Use `freeze`, which includes the complete allowlisted inventory. Actual counts may change with a justified revision. Every historical review requires its byte-exact snapshot. The gate recomputes paths, raw hashes, byte counts and line counts from that snapshot, checks its own frozen allowlist against the complete snapshot inventory, and verifies that all pinned corpus entries are included. A supplied `lines: 1` cannot disguise a longer file, even when its raw hash is unchanged. A hash authenticates consistency with captured bytes, not who supplied them.

Do not embed a file's own digest in that file. Commit identities and content fingerprints have different purposes. Evidence-only commits and state transitions can advance Git history without changing reviewable content. Raw source hashes preserve their original bytes; derived text deliberately uses LF newlines. Keep newline transformations explicit when working on Windows.

## Source and generated manifests

`sources/manifest.json` uses `files: [{path, sha256, bytes?}]` for readable repository copies beneath `sources/`. Every listed hash is checked; the manifest must not hash itself. `external` may describe Library-read or other referenced sources whose original bytes are not present. Do not invent raw hashes for normalized excerpts.

`generated/manifest.json` records the canonical raw SHA-256, eight payload hashes and code-point/UTF-16 counts, section hashes and original canonical line ranges, and the JSONL output hash/count. Section files include copied reference definitions so their links remain useful. Generated content is data, not an instruction to execute the archived examples.

The extractor copies the authored payload blocks. It does not automatically propagate a semantic change elsewhere in `persona.md` into those blocks. Every accepted canonical change must consider affected adapters; update their authored blocks, then rebuild. Never hand-edit generated files.

## Review records

Both `reviews/01-gemini/` and `reviews/02-grok/` require:

1. `input-manifest.json` and `input-snapshot/`: the frozen complete candidate manifest and exact file bytes, created by `freeze`.
2. `read-coverage.json`: matching `input_fingerprint` and `files: [{path, sha256, ranges, evidence}]`. Every input file appears once. Ranges are inclusive original line pairs such as `[[1, 100], [101, 230]]`; their union must cover all original lines, without gaps or out-of-bounds claims. An empty file has an empty range list. Evidence explains actual reading, including section/chunk routing and limits.
3. `review.json`: completed status, truthful identity/attestation and artifact hashes.
4. The actual unaltered report, structured `findings.json`, and `sources.json`, at the paths named by `review.json` within that review directory.
5. `integration.json`: dispositions, input/output fingerprints, and exact evidence pins.

`review.json` fields:

```json
{
  "status": "pending",
  "identity": {
    "service_requested": "Gemini",
    "service_observed": null,
    "model_requested": null,
    "model_observed": null,
    "runtime_evidence": null,
    "accepted_substitute": null
  },
  "attestation": {
    "actual_review": false,
    "input_fingerprint": null,
    "recorded_by": null,
    "evidence": null
  },
  "artifacts": {
    "report": {"path": "reviews/01-gemini/report.md", "sha256": null},
    "findings": {"path": "reviews/01-gemini/findings.json", "sha256": null},
    "sources": {"path": "reviews/01-gemini/sources.json", "sha256": null}
  }
}
```

Replace pending values only with actual evidence. The second round requests `Grok`. `service_observed` may remain null if the attribution is limited; when present it must match the requested service. Record the requested model explicitly. `runtime_evidence` must identify `{basis, model, reference}`, where basis is `observed_ui`, `api_metadata`, or `user_attestation`. The latter is an explicitly attributed user report, not inferred backend metadata. An unknown `model_observed` can stay null when that evidence identifies the actual runtime; do not copy the requested model into an observed field. If the evidenced actual model differs from the requested model, require `accepted_substitute: {model, evidence}` identifying explicit owner authorization for that substitute. Unknown effort remains an explicit limitation, not assumed High.

Known equivalent display/API labels are explicitly mapped: `Gemini 4 Argon` ↔ `gemini-4-argon` and `Grok 4.7` ↔ `grok-4.7` (case-insensitive for these aliases). Other names do not match by substring or assumed family membership; a new alias needs documented justification. This mapping identifies requested labels; it does not establish current service availability.

The requested stage models are pinned in the reviewed tool to `Gemini 4 Argon` and `Grok 4.7`. A report cannot silently redefine that request by changing both its requested and observed labels. An owner-approved alternative uses the explicit substitute record; a later change to the governing request requires a deliberate reviewed update to the workflow/tool.

Completion requires `status: completed`, `actual_review: true`, the correct input fingerprint, a nonempty `recorded_by` and evidence reference, and exact hashes of three distinct nonempty artifact files. These declarations must come from a real review capture or an accurately attributed owner-supplied review, never from the validator's unit tests.

`findings.json` contains `findings: [{id, blocking, summary, ...}]`. IDs are unique; `blocking` is Boolean. An empty list is valid only when the actual review found no actionable issues. `sources.json` contains `sources: [...]`; it may distinguish supplied-source references from newly verified primary sources. A blank research list does not justify invented citations.

Grok's `review.json` additionally requires `upstream: {gemini_integration_sha256, reading_attested:true, evidence}`. The hash pins the actual raw Gemini integration record, which transitively pins its report, findings, sources, review identity, input manifest and reading coverage. `evidence` describes the real reading of that earlier review/integration. Changing Gemini's report and repinning its integration invalidates Grok's upstream pin; it cannot silently remain reviewed.

## Integration and readiness

`integration.json` has `status: integrated`, the reviewed `input_fingerprint`, integrated `output_fingerprint`, an exact `evidence` object, and `dispositions`.

The evidence object contains precisely six raw file hashes:

```text
review_sha256          review.json
input_manifest_sha256  input-manifest.json
read_coverage_sha256   read-coverage.json
report_sha256          the named report
findings_sha256        the named findings JSON
sources_sha256         the named sources JSON
```

Every finding has one disposition: `{finding_id, decision, reason, ...}`. `accepted` requires nonempty `verification` and `change_refs`; `rejected` requires the reason; `deferred` requires a nonblocking finding and a concrete `next_action`. Explain duplicates through a rejection reason referencing the finding/fix they duplicate. No blocking finding may be deferred. The machine verifies required evidence fields, not the truth or sufficiency of a prose rationale.

Gemini's integrated output fingerprint must equal Grok's input fingerprint. Grok's integrated output fingerprint must equal the current candidate. `workflow/state.json` must have `phase: READY_FOR_INSTALL` and that same `candidate_fingerprint`. Any content change thereafter invalidates the final candidate until properly dispositioned and verified; editing state alone cannot repair the chain.

The gate establishes eligibility to enter installation when that work is explicitly authorized in the actual task/session. Already-granted conditional authorization remains valid once its prerequisites are met. The gate does not launch the task, authorize new access, override current host restrictions, or report the persona installed.

## Hosted integrity checks

`.github/workflows/validate.yml` runs the same local integrity command and temporary-fixture unit tests for main-branch pushes and pull requests. It uses a pinned official `actions/checkout` revision, read-only repository permission, no persisted Git credentials and no model/API secrets. It performs no installation and no persona inference. A pending review state can legitimately show a successful integrity workflow while installation remains blocked. Actual CI execution/availability must be observed on GitHub; a workflow file alone is not a run receipt.
