# Lucifer

## Current access decision — 2026-10-24

`MGrinch/Lucifer` is intentionally **public** by Misha's explicit instruction so Gemini and Grok can read it. Preserve its existing visibility; do not change it. This owner decision supersedes older workflow notes that called for private publication. Read access is public; writes still require an authorized authenticated writer. Do not upload credentials, private installation backups, account exports or unrelated personal data. Public visibility grants no new license to the personal corpus and changes neither the two-review gate nor installation permissions.

**A public, evidence-led path from a developed character to a tested persona installation.**

[Start here](start%20here.md) · [Desired end state](goal.md) · [Current specification](persona.md) · [Stage status](workflow/state.json)

Lucifer is Misha's original adult female assistant character: warm, composed, darkly elegant, quick-witted and independently useful. This repository preserves the work already done, then gives two different reviewers room to improve it before a Codex worker applies the accepted result.

## The sequence

| Stage | Worker | Result |
|---|---|---|
| 1 | Gemini 4 Argon, requested high reasoning | A complete audit, Google/YouTube evidence, precise improvements and a traceable review packet. |
| 2 | Authorized GitHub writer | Integrate Gemini's accepted changes into `main`; preserve the original report and unresolved questions. |
| 3 | Grok 4.7, requested high reasoning | Independent critique of the updated candidate, X/practitioner research, and explicit review of Gemini's conclusions. |
| 4 | Authorized integrator | Reconcile the two passes, regenerate adapters, validate the exact candidate, and mark it ready for installation. |
| 5 | Codex gpt-6.1-sol, requested high effort | Inventory the actual account/devices, apply supported changes, verify each surface, and report precise coverage. |

These are requested runtimes. Each run must record the model and effort actually exposed by its host. The two external critiques and installation have **not** happened in the initial repository.

## Give an agent one starting instruction

> Open https://github.com/MGrinch/Lucifer on `main`. Read `start here.md`. Follow the route for your assigned stage, read the required inputs completely, and leave the required artifacts. Preserve Lucifer's character while improving the evidence, instructions and attainable behavior. Do not skip the two-review gate or claim installation during review.

Ready-to-use stage prompts are in [prompts/](prompts/README.md).

## Important access detail

Gemini's standard GitHub import is a snapshot and does not write changes back. The repository and raw files are publicly readable without GitHub authentication. An app may still require an explicit supported import; opening a URL does not prove it loaded every file. A supported writer can then commit the returned review packet. Grok's actual repository access and write tools must be checked in its connected session. The [access guide](workflow/00-access.md) gives both direct-write and report-return routes.

## Where truth lives

| Path | Purpose |
|---|---|
| `persona.md` | The one current editable specification: personality, adapters, installation procedure, tests and research. |
| `context/` | Owner intent, protected preferences and requirement traceability. |
| `design/` | How the parts fit together and how to critique response construction. |
| `workflow/` | Ordered steps and honest stage status. |
| `reviews/` | The two actual reviews, source evidence, read coverage and integration decisions. |
| `sources/` | Exact original research handoff and recovered historical corpus, with hashes and aliases. |
| `generated/` | Smaller reading sections, deployment payloads and evaluation cases extracted from the current specification. |
| `evals/` | Character quality, regression and real voice acceptance. |
| `install/` | Target coverage, supported installation route and rollback requirements. |
| `tools/` | Local standard-library build, integrity and readiness checks. |

This is a publicly readable working repository. No open-source license is granted to the personal corpus. Referenced public projects retain their own licenses. No third-party runtime is required for the initial native-first route.

## Single-file delivery and strengthened handoff

Misha's [latest delivery instruction](context/owner-addendum-2026-10-24.md) is implemented in the [bootstrap guide](workflow/00-repository-creation.md), [review Git protocol](workflow/08-git-review-history.md), and [complete control coverage guide](workflow/09-surface-coverage.md). The packaged source preserves the previous preparation snapshot and the unchanged R1 character specification. Review publications and installation still have pending receipts.
