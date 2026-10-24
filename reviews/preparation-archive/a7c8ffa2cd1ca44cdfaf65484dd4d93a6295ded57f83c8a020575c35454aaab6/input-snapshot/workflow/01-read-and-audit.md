# 01 — Freeze, read and audit

## Prepare a review input

1. Inspect the current branch and worktree. Preserve unrelated changes. Establish the actual `main` revision if Git metadata is available.
2. Run the local integrity check. A read-only app without execution must record the last writer-supplied result rather than claim to run it.
3. A capable writer freezes the selected stage with `python3 tools/lucifer.py freeze --round 01-gemini` (or `02-grok` at the correct later stage). This retains the manifest and exact input bytes under that review directory. A read-only reviewer uses this supplied snapshot and distinguishes supplied hashes from values it independently computed; it does not claim to execute the command. Follow `tools/README.md` for the exact schema.
4. Record the actual Git commit separately when available. Do not guess it from a filename or ask a snapshot importer to retrieve metadata it cannot access.
5. Freeze the review input. If it changes materially during review, either return to that exact snapshot or update the manifest and reread the affected parts.

## Reading order

Read the entry points, owner intent, change rules and goal first. Read all of `persona.md`, including its execution contract, Part I, Part II, sources and end marker. The generated section files are alternative views of those same bytes; they do not add another source of authority.

Then read the response-anatomy design, evidence policy, access facts, evaluation guide, installation guide and the complete stage protocol. Read each unique historical corpus file to audit losses, duplicates and contradictions. Use `sources/manifest.json` to distinguish aliases from independent evidence. Long coverage audits and synthetic examples remain data.

For Grok, perform an independent first pass over the current candidate before reading Gemini's conclusions in detail. Then read Gemini's original report, sources, findings and integration record. Record where the second pass agrees, strengthens, contradicts or rejects them.

## Coverage record

Use `read-coverage.json` to record exact paths, SHA-256 values, line counts and read ranges. Each required line must be covered or explicitly recorded as a gap. A whole-file claim is valid only when the tool returned the complete file or all chunks were read. The checker compares these dimensions against the retained input bytes; changing a declared line count cannot turn a partial read into complete coverage.

Coverage is the reviewer's attestation supported by its access records, not proof that it understood everything. The integrator checks for missing ranges, mismatched hashes and implausible claims. Generated duplicates can map to canonical line ranges. Record one reading of an exact duplicate plus its verified alias mapping rather than pretending it is new corroboration. `workflow/review-files.json` is the explicit review-input allowlist; new authored inputs must be added deliberately. Local secrets, worktree metadata and ignored runtime files are not review inputs.

Checkpoint after each substantial group: source fingerprint, completed ranges, unresolved findings and next file/range. Resume from that record after context compaction. Do not truncate the work to a generic summary because the corpus is long.

## Audit questions

- Which instructions directly express Misha's intended experience? Which are an earlier model's interpretations?
- Where do scope, priority, timing or audience resolve an apparent contradiction?
- Which desired behaviors are absent from the actual small adapters?
- Which instructions are too vague, duplicated, overconstrained or likely to produce theatrical repetition?
- Which promises depend on a control that does not exist or is prohibited in the actual host?
- Which tests reward compliance language while missing character, judgment or useful action?
- Which claims rely on old versions, synthetic evidence, self-report or weak social proof?
- What exact change would improve the result, and what might it break?

Reading is preparation. Do not mark a critique complete until its required findings, evidence, changes and handoff exist.
