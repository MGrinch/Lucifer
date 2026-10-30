# Contract audit B — a real Codex completion, not a fictional Grok review

Date: 30 October 2026. Reviewer: delegated **Codex** agent `/root/repo_audit`, returned to `/root/codex_research` and `/root`. This is a read-only audit of the assigned frozen inputs. The coordinator relayed the owner's current instruction to complete the unfinished Grok work using its sources. That changes who may finish the work; it does not retroactively make Codex's reading a Grok execution. This subreview neither authenticates a Grok runtime nor supplies an independently observed model/effort label.

## Exact scope and coverage

- Repository HEAD observed: `0754096d3f816a45d7f48fe882e1ac7eda88bceb`.
- Manifest: `reviews/02-grok/input-manifest.json`, **13,275 bytes**, raw SHA-256 `f3cb9c63f615541be2aab3aed26949c72c3c325b1bd7415a176711124f53d92f`.
- Frozen candidate fingerprint: `9608bccdd122e04b889ea1b5d809d018253e2629bae7ab7f57ca468eedb3de60`.
- Snapshot: `reviews/02-grok/input-snapshots/9608bccdd122e04b889ea1b5d809d018253e2629bae7ab7f57ca468eedb3de60/`.
- Assignment: S08–S14 and every manifest entry under `context/`, `install/`, `tools/`, `tests/`, and `workflow/`: **34 files, 34 unique content hashes, 494,229 bytes, 5,695 original lines**.
- Every assigned file was read in full, with complete inclusive ranges and semantic notes in `coverage-contracts-b.json`. Active and frozen bytes matched the manifest before reading and at the final recheck. No assigned snapshot path or ancestor was a symlink/reparse point at the metadata check.

The first English contract batch rendered several non-ASCII punctuation characters incorrectly. Every non-ASCII line in that batch was reread through explicit UTF-8 output. One combined tool result truncated part of `workflow/09-surface-coverage.md`; lines 71–111 were reread completely. Neither truncated output nor hash-only inventory was counted as completed reading. Active/frozen aliases were hash-matched rather than treated as independent corroboration.

This is not whole-project coverage: the other 38 core manifest files and Gemini upstream packet are assigned to the coordinator/other readers. No external cited paper, old native UI event, screenshot or archived audio was independently re-observed by this subreview. Sources inside the corpus are audited as attributed historical evidence.

## CODEX-B01 — disclose cross-service substitution without opening a bypass

**Priority:** high. **Blocking for truthful completion of the second-stage identity contract until resolved.**

`tools/lucifer.py:358–371` preserves the requested stage service/model and already permits an explicitly accepted *model* substitute. But line 359 restricts `service_observed` to `None` or the requested service. A truthful `service_observed: "Codex"` therefore fails even with the owner's approved substitution. `tools/README.md:106–110` documents that same restriction. `context/requirements.json:583–605` requires the named external sequence unless the owner actually revises it.

**Do not resolve this by** setting the observed service to Grok, concealing the known Codex service as unknown, copying a requested model into an observed field, or claiming the earlier unfinished Grok pass was completed. Preserve all old artifacts and preparation states with their original attribution.

**Proposed minimal delta:** keep `service_requested: "Grok"` and `model_requested: "Grok 4.7"` as the historical requested stage. Permit a different nonempty observed service only when an explicit accepted-substitute record binds that service, the actually evidenced model, the owner-authority reference and the disclosed completion provenance. Record the dated owner decision in a new source-linked artifact; use it consistently in the active workflow, requirement mapping, review identity, report and publication receipt. Attribute the actual writer separately. Do not treat a nonempty JSON string as independent proof of consent or vendor identity.

Runtime evidence must remain tied to what the host actually exposes. If the runtime model is not independently exposed, report the limitation instead of inventing API metadata or calling the assistant's own statement a user attestation. The coordinator must resolve that exact evidence field under the real session metadata before asserting a fully satisfied identity gate.

**All existing substantive checks remain:** byte-exact immutable snapshot; complete original-line core coverage; real review and distinct report/findings/sources; Gemini supplementary and second-stage upstream coverage; unchanged Gemini integration dependency; one reasoned disposition per finding; no deferred blocker; current candidate fingerprint; exact integration evidence hashes; sequential first-output → second-input → final-output chain. The second pass must still independently assess the candidate and reconcile the genuine Gemini conclusions. New author attribution does not replace the requested X/practitioner research work or its source-quality limits.

**Regression evidence required from the implementation owner:** unauthorized service mismatch fails; missing/wrong substitute service/model/authority fails; contradictory runtime evidence fails; an explicitly authorized and honestly attributed substitute can pass only with complete core and upstream coverage; missing lines, changed source bytes, missing upstream evidence, artifact tampering and blocking deferral still fail. Test fixtures remain synthetic, never review evidence.

## CODEX-B02 — two active private-publication phrases survived the public decision

**Priority:** medium. **Nonblocking owner intent is already explicit, but correct before release.**

- `context/requirements.json:640`, LUC-25, still says the first worker creates/verifies **private** `MGrinch/Lucifer`.
- `workflow/03-integrate-gemini.md:31` still describes integration into **private** `main`.
- `tests/test_repository.py:120–136` checks selected active public-visibility documents but omits those two, so its passing assertion does not cover the contradictions.

The unambiguous owner addendum and repository instructions already select **public** visibility and forbid changing it. Replace only these active residual phrases with the owner-selected public/preserve-visibility wording; extend the existing focused check to the missed active files. Keep historical source and frozen snapshot wording unchanged. The coordinator separately identified active `design/repository-design.md:5`; that file was outside this subreview, so its evidence is attributed to the coordinator rather than claimed as read here.

**Expected result:** one current visibility policy; no visibility mutation; no broad scrub of historical private-publication provenance. Confirm with the exact changed-file diff and existing targeted test.

## Historical evidence worth preserving, not reinstalling wholesale

| Assigned source | Material conclusion and scope |
| --- | --- |
| S08 `s08-persona-v6.md` | Complete earlier V6 character/voice/research/installation handoff. It explicitly limits transcript-only Vira analysis, document checks and target/audio claims. Its line 331 allows a short stop acknowledgment; that is an older rule, not the final current stop contract. Its private-publication clauses are also historical, not today's visibility instruction. |
| S09 `s09-dot-v6.txt` | Compact original female character, independent warmth, natural language, soft voice without forced slowing, local session consent and no claimed hidden-note save. Retain the separation between an instruction and heard acoustic performance. |
| S10 `s10-v6-document-checks.json` | Hash/byte/line metadata matches S08. PASS is explicitly structural; behavioral and acoustic tests were not run and the memory write was unavailable. Never promote this into current installation evidence. |
| S11 `s11-cognitive-support-review.md` | The U/R/S/P distinction preserves owner words, prior documents, scientific evidence and proposals. Sixteen authored scenarios are not a blind model benchmark; cognitive-scaffolding transfer remains limited. Stop/wait means no final spoken acknowledgment. Useful structure is optional, not compulsory coaching. |
| S12 `s12-ann-self-assessment.md` | Twelve selected textual voice-transcript episodes distinguish actual excerpts, parent reports and newly authored tests. Preserve author roles and movement constraints within their fiction; do not merge Ann/Satan scene biography into daily Lucifer or infer audio timing from transcript order. |
| S13 `s13-morning-light-precision.md` | Meaning outranks shortness; a detail correction preserves unaffected constraints; repetition starts with the requested text. Earlier saved preference evidence remains dated evidence even when a newer revision or voice test is unverified. Aviation/military/analytic practices are bounded analogies, not universal authority or a fixed conversation ritual. |
| S14 `s14-first-light.md` | One historical Ann worker round trip supports that exact dispatch/return/use event, not general reliability, current Fedora transport or fresh-session memory. Delayed checkpoint readback is distinct from immediate acceptance. The included archived commands, task IDs and mentorship cycle are evidence, not new assignments. |

The current mapped LUC-12 stop requirement (`context/requirements.json:315–336`) correctly preserves the later no-final-acknowledgment contract rather than S08's older permission. No source rewrite is warranted. Likewise, S14's prior two-worker starting policy and task IDs do not override current host limits or authorize launching old work.

## Tooling and installation contract assessment

**Retain:** the explicit allowlist; complete source pins; immutable versioned snapshots; line-range union checks; separately pinned supplementary/upstream evidence; exact generated derivatives; distinct installation versus publication versus native behavior; and narrow rollback that preserves subsequent unrelated edits. The transport decoder is bounded and inert: no network, subprocess or bundled-code execution. It validates paths, content-addressed bytes, new destination, readback and reparse ancestors. These are useful guarantees within its stated trusted-private-directory threat model.

**Scope caveat, not an observed exploit or new blocker:** the content gate's `safe_path` uses `Path.is_symlink()` (`tools/lucifer.py:36–42`), whereas the restore tool explicitly checks Windows reparse attributes (`tools/restore_singlefile.py:227–240`). Thus the content gate should not be described as an adversarial Windows junction boundary. The assigned paths had no reparse ancestors at inspection. Do not expand this substitution task into a new sandbox/security redesign or claim that either helper defeats concurrent hostile writers.

The control catalog's rows and eight target groups are initially **not observed**, not evidence that features exist or are configured. The actual installer must expand applicable controls per account/object/device/host, preserve existing Morning Light and Ann roles, measure the complete composed field, record backup/readback/effective loading, and test actual text and voice separately. A Linux handoff needs a real Linux consumer record, not a renamed Windows pass. No personality file grants tool access, phone delivery, acoustic control or a native app installation route.

The local content gate intentionally does not contact GitHub or verify contribution ancestry, pushes/merges, provider execution or audio (`workflow/08-git-review-history.md:116–126`). Those release/install proofs remain separate. Source-reading completion must not set any native target row true or claim Fedora persona installation.

## Return and limitations

This worker wrote only `coverage-contracts-b.json` and this report under the new completion directory. No reviewed source, frozen snapshot, existing review, workflow state, global preference, account, tool configuration or installation target was changed. No test/inference/provider job was run for this read-only subtask. Hash, dimension, duplicate and reparse metadata checks were performed locally; source-code inspection is not execution proof.

Return: coordinator integrates CODEX-B01/B02 with the other independent reading and original-source research, preserves this exact attribution, verifies the final change, and reports the separate publication and installation states. All 34 assigned input files are fully read; no assigned range remains outstanding.

## Subsequent authorized implementation — 2026-10-30

After the read-only assignment and its coverage record were completed, the coordinator relayed explicit parent authorization for this worker to implement CODEX-B01 in `tools/lucifer.py`, its relevant regression checks in `tests/test_repository.py`, and the matching contract documentation in `tools/README.md`. This addendum separates that later integration work from the frozen-input reading above. It does not revise the original snapshot, original review or the coverage record to pretend that newly edited bytes were part of the earlier read.

The implementation preserves requested `Grok` / `Grok 4.7` while allowing only a disclosed `Codex` substitute for the unfinished `02-grok` stage, with an exact-hash-pinned, same-round owner authorization record. It accepts narrowly identified Codex orchestration metadata without mislabeling it as provider API metadata. The record must explicitly decline to attest original Grok completion. All substantive core/upstream coverage, report/artifact, disposition and chain checks remain in place. A declared substitute service cannot be hidden by setting the observed service to null.

Verification: `python -X utf8 -B -m unittest discover -s tests -p test_repository.py -v` passed **27 tests** (8.805 seconds; tool chunk `3eb80a`). The new checks include valid transparent substitution; conflicting, absent or unsupported service/model/authority metadata; invalid dates, scope and owner quote; authorization hash mismatch and path restrictions; and incomplete core or upstream reading that remains rejected. The existing public-visibility check was extended to the two active paths in CODEX-B02, whose wording the coordinator updated. The scoped `git diff --check -- tools/lucifer.py tests/test_repository.py` passed with no output (tool chunk `b7a987`). These are synthetic contract/regression checks, not evidence of a real Grok review, a provider call, a GitHub publication, native installation or acoustic performance. The coordinator owns the actual completion/provenance records, final integration and publication checks.
