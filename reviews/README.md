# Review records

There are exactly two required external passes in this release cycle:

1. `01-gemini`: actual Gemini 4 Argon critique, requested high effort.
2. `02-grok`: actual Grok 4.7 critique of the Gemini-integrated candidate, requested high effort.

Initial files are explicitly **pending placeholders**, not reviews. Do not fill them with simulated reviewer speech, this repository author's analysis or a guessed outcome.

## Files per pass

| File | Meaning |
|---|---|
| `input-manifest.json` | Frozen input paths, hashes, line counts and content fingerprint. |
| `input-snapshot/` | Exact frozen input bytes for independent dimension/inventory checks; evidence only. |
| `read-coverage.json` | Actual reviewer attestation of complete ranges with access evidence. |
| `review.json` | Runtime/access metadata, actual-review attestation and artifact digests. |
| `report.md` | Original complete external review; preserve verbatim after receipt. |
| `findings.json` | Structured findings, importance, evidence, precise changes and tests. |
| `sources.json` | Retrieved evidence with dates, modality, claims and limits. |
| `integration.json` | Writer's decisions, implemented changes, verifications and input/output chain. |
| `proposed.patch` or replacement blocks | Exact suggested edits when the reviewer provides them. Optional if the report contains unambiguous complete replacements. |

Use `tools/README.md` for machine-checked schema fields. Extra documented fields are allowed. A writer can normalize an external Markdown response into the schema while preserving the original and marking missing fields. It cannot invent a read attestation, runtime evidence or executed test.

## Finding record

Each finding should include a stable ID (`GEM-001` or `GRK-001`), exact file/section/line or quoted locator, defect, affected requirement IDs, expected consequence, proposed change, supporting source IDs, counterevidence/uncertainty, verification method and whether it blocks installation readiness.

A reasoned proposal can be rejected. A nonblocking item can be deferred with a concrete next action. Every accepted change must exist and have a verification reference before integration is complete.

## Completeness is not aesthetic agreement

The reviewer can prefer different prose. The integrator judges whether its changes serve Misha's character. Preserve disagreements visibly. Strong engineering evidence does not automatically choose a subjective taste; a style preference does not establish a product capability.

## Hashes and scope

Candidate fingerprints exclude review records to avoid self-reference. Integration receipts therefore pin the exact review, source, finding, input-manifest and coverage bytes separately. Grok additionally pins the Gemini integration record it read; that binds it to the preserved first report and decisions. The readiness check validates that chain against retained input snapshots. It cannot prove the reviewer's honesty or replace source inspection.

GitHub branch protection is not configured by this repository. The checker is a transparent procedural guard, not an access-control boundary. Do not describe it as stronger enforcement than it provides.

## Actual Git publication

Each review directory also has `publication.json`, initially NOT_STARTED. Follow `workflow/08-git-review-history.md`; actual reviewer, authenticated writer, contribution commit, push and merge evidence are separate. These receipts are not auto-validated by the content gate and must be checked against the actual remote before installation.

## Dated owner-authorized reviewer substitution — 30 October 2026

The earlier two-vendor assignment above is preserved as history. The owner subsequently authorized Codex to finish the unfinished second-stage review using recovered Grok sources. The exact scope and exposed runtime are recorded in `02-grok/codex-completion-20261030/provenance.json`. Current second-stage metadata must say actual Codex, not Grok; requested Grok/Grok4.7 stays visible. The completed Codex supplement, actual full83-input reading and independent source reconciliation do not retroactively complete the missing Grok archive. No source/coverage/disposition/integrity/publication/native gate is removed.
