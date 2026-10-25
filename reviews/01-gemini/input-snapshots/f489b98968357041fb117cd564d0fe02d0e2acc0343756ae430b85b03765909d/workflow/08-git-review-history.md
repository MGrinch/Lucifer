# 08 — Two real review contributions, pushes and merges

## Current access decision — 2026-10-24

`MGrinch/Lucifer` is intentionally **public** by Misha's explicit instruction so Gemini and Grok can read it. Preserve its existing visibility; do not change it. This owner decision supersedes older workflow notes that called for private publication. Read access is public; writes still require an authorized authenticated writer. Do not upload credentials, private installation backups, account exports or unrelated personal data. Public visibility grants no new license to the personal corpus and changes neither the two-review gate nor installation permissions.

This is the publication requirement added by Misha's single-file handoff request. It supplements the content/read-coverage gate; it does not replace it. Both real reviews must remain independently attributable, their accepted changes must reach public `main`, and the final installer must verify the published revision.

## Actors and boundaries

| Responsibility | Evidence |
|---|---|
| Gemini 4 Argon critique | Actual returned report, observed runtime/effort or documented limitation, input fingerprint, complete read coverage, primary sources and findings. |
| Grok 4.7 critique | Actual returned report on Gemini-integrated input, separate initial audit, X/web sources where actually used, upstream integration pin and findings. |
| GitHub writer | Actual authenticated account/tool that saved files, committed, pushed and merged. May be Codex importing a review packet. |
| Integrator | Dispositions, exact implementation diff, rebuild/check/test evidence and preserved original reports. May share the writer role. |
| Installer | Fresh published-main verification, passing content gate and subsequent supported native changes. Cannot retroactively invent the two reviewers. |

Gemini's standard GitHub import is read-only; see [access facts](../research/cross-vendor-capabilities.md). Do not promise it can push. Prefer an actually exposed authorized writer; otherwise return the complete packet for Codex to save, commit, push and merge. The owner must not have to translate prose recommendations into patches.

## Required sequence

### A. Gemini contribution

1. Start from the verified bootstrap `main`; record the actual base commit and frozen input fingerprint.
2. Create a dedicated branch such as `review/gemini-argon-01`, using a collision-free suffix if necessary.
3. Preserve the actual complete original Gemini report and metadata. Never generate substitute content under Gemini's name.
4. Validate sources and reading coverage; disposition findings; apply accepted canonical/adapter/test/documentation changes; rebuild and run checks/tests.
5. Complete Gemini's integration record according to `tools/README.md`. A readiness gate need not pass yet because Grok is still pending.
6. Create at least one substantive commit containing this actual review contribution and accepted integration. Push the branch and verify its remote commit.
7. Merge that branch into `main`, preferably through a PR with a merge commit so the review commit remains an ancestor. Preserve the actual PR, contribution commit and merge commit references. Do not squash the two model passes into one undifferentiated change.
8. Fetch/read back `main`; verify accepted files. Record the publication receipt outside the fingerprinted candidate inventory. Freeze Grok's input from this integrated candidate; pin the exact Gemini integration record. Set `AWAITING_GROK`.

### B. Grok contribution

1. Start from Gemini-integrated `main`, not the original bootstrap branch or stale import. Record actual base commit, updated candidate fingerprint and the existing Gemini receipt.
2. Create `review/grok-4-7-02` or a collision-free equivalent.
3. Obtain and preserve the actual Grok report, initial independent audit, Gemini reconciliation, source record and observed runtime.
4. Disposition and apply accepted changes coherently. Preserve Gemini's original report and earlier decision history. If new evidence changes a previous decision, record the revision instead of rewriting the historical review.
5. Run rebuild/check/tests; complete the Grok integration record. Set `READY_FOR_INSTALL` only when the content gate is valid; run that gate on the exact resulting candidate.
6. Commit the substantive Grok contribution, push and verify its remote commit. Merge into `main` after resolving conflicts and rerunning applicable checks on the merge result.
7. Fetch/read back final `main`. Ensure both review contributions are preserved in ancestry, both merge/push events have evidence, and the content gate passes on that merged candidate. A merge conflict fix changing reviewed content must be reconciled with affected findings and evidence; no silent late redesign.

### C. Final Codex entry

The final Codex worker independently reads public remote metadata and `main` with its own supported tools. It verifies all Git completion predicates below, checks the content fingerprint and runs `tools/lucifer.py gate`. It installs only that accepted candidate. If `main` has advanced, inspect the diff; evidence-only receipts can leave the candidate unchanged, but changed reviewed content requires renewed reconciliation and checks.

## Concrete Git route

These are operation forms, not an unchecked script; use the observed branch names and review state:

```sh
git fetch origin
git switch main
git merge --ff-only origin/main
git switch -c review/gemini-argon-01
# Save the actual Gemini artifacts and accepted edits; build/check/test first.
git add --all
git diff --cached --check -- tools tests workflow install prompts
git diff --cached --stat
git commit -F /actual/private/path/gemini-commit-message.txt
git push -u origin review/gemini-argon-01
# Create/merge the PR through the supported writer; inspect the actual result.
```

Prepare multiline commit messages and PR descriptions as actual UTF-8 files or structured tool arguments. Do not interpolate model text into shell commands. Use a real supported PR/merge tool; discover its schema instead of guessing. If normal branch protection requires a genuine approval, prepare all content and report that actual boundary rather than weakening protections. Ordinary in-scope merge authorization already comes from the owner's task.

Example commit message **template**, with placeholders replaced by observed values:

```text
Integrate Gemini 4 Argon review of Lucifer persona

Preserve the actual review, resolve its findings, and implement the accepted
changes while retaining the owner's character and deployment requirements.

Review-Service: Gemini
Review-Model-Observed: <actual observed model>
Review-Effort-Observed: <actual value or not-exposed>
Review-Input-Fingerprint: <actual fingerprint>
Review-Report-SHA256: <actual original-report hash>
Review-Writer: <actual authenticated writer>
```

For Grok, use its actual service/model/report values. These trailers describe attribution; they do not impersonate a Git author or prove execution on their own. Additional commits for preparation, fixes, receipts or merges are normal. Two real review contributions are required; two total Git commits are not a ceiling.

## Publication receipt

Use `reviews/01-gemini/publication.json` and `reviews/02-grok/publication.json`. Templates begin pending. Fill only observed values:

```json
{
  "schema": 1,
  "status": "PUBLISHED_AND_MERGED",
  "repository": "MGrinch/Lucifer",
  "private_observed": false,
  "review_service": "Gemini",
  "review_model_observed": "<observed>",
  "writer_identity_observed": "<observed>",
  "write_route": "<actual supported tool or CLI>",
  "base_commit": "<actual>",
  "branch": "<actual>",
  "contribution_commit": "<actual>",
  "push": {"observed": true, "remote_commit": "<actual>", "evidence": "<readback>", "observed_at": "<actual UTC>"},
  "merge": {"observed": true, "commit": "<actual>", "pull_request_url": null, "evidence": "<actual result/readback>"},
  "main_head_verified": "<actual>",
  "contribution_is_ancestor_of_main": true,
  "candidate_fingerprint": "<integrated output>",
  "report_sha256": "<actual>",
  "integration_sha256": "<actual>",
  "verification": {"checked_at": "<actual UTC>", "by": "<actual worker>", "evidence": ["<actual references>"]}
}
```

Receipt files are evidence outside `workflow/review-files.json`; never insert a commit's own hash into that same commit. A subsequent metadata commit can record an earlier content or merge commit. Keep original reports and content integration receipts immutable once pinned by the later stage unless a documented correction updates the dependency chain.

## Git completion predicates — mandatory in addition to the content gate

- The actual repository is public and belongs to MGrinch; expected repo metadata is freshly observed.
- Each contribution exists remotely and the actual pushed commit is recorded. An attempted command or local SHA alone does not establish this.
- Each contribution is reachable from final `main`. With a Git checkout, fetch first and use `git merge-base --is-ancestor <contribution_sha> origin/main`; inspect its exit status for **each** review. Never pass angle-bracket placeholders literally.
- The recorded merge and branch history matches the actual Git graph. Use a merge commit or fast-forward integration that preserves each original contribution commit as an ancestor of main. Do not squash or rebase these published review contributions under this protocol. If an actual mandatory repository policy prevents a preserving merge, finish all unaffected work and record the precise policy boundary; any alternative history protocol requires an explicit owner decision and revised receipts before installation.
- Grok's base/candidate comes after the actual Gemini integration. Its evidence pins the exact Gemini integration packet.
- Current merged content matches the final integration fingerprint and passes `python3 tools/lucifer.py gate` plus the repository checks/tests.
- Review authorship, Git author, committer and writer are described separately and truthfully.

**The existing Python content gate does not contact GitHub or verify pushes, PRs, merges, vendor execution or audio.** The installer must perform and record the remote checks above; a green local gate alone is not the full installation entry condition.
