# Start here — worker entry point

**Owner:** Misha. **Project:** Lucifer. **Initial phase:** AWAITING_GEMINI. **Installation:** not performed.

Your job is to improve and then deploy one coherent persona through the supported controls of the actual host. It is not to prove that a prompt creates a literal human or guarantees identical behavior from every model.

## 0. Bootstrap and current owner addendum

If you received the outer single-file `persona.md` to create this repository, restore its payload first, then follow [repository creation](workflow/00-repository-creation.md) and [bootstrap prompt](prompts/bootstrap-codex.md). The first worker stops at verified private publication and `AWAITING_GEMINI`.

Read the [current owner addendum](context/owner-addendum-2026-10-24.md). It requires separately attributable real review contributions, commits, pushes and merges under [Git publication protocol](workflow/08-git-review-history.md), then complete per-control installation coverage under [surface protocol](workflow/09-surface-coverage.md). The original canonical character specification is unchanged by this packaging revision.

## 1. Establish your role before acting

Read [AGENTS.md](AGENTS.md), [workflow/state.json](workflow/state.json), [owner intent](context/owner-intent.md), and [goal.md](goal.md).

| Current assignment/state | Continue at | Permitted work |
|---|---|---|
| First Codex bootstrap / publication not verified | [creation guide](workflow/00-repository-creation.md) | Restore exact files, create private repo, commit/push/read back; stop ready for Gemini. |
| Gemini critique / AWAITING_GEMINI | [Gemini prompt](prompts/gemini.md) → [stage 02](workflow/02-gemini-review.md) | Inspect, research, critique, propose exact patches; write review artifacts if an authorized writer exists. |
| Gemini report available / GEMINI_REVIEWED | [stage 03](workflow/03-integrate-gemini.md) | Preserve report, validate proposals, integrate accepted changes, prepare Grok input. |
| Grok critique / AWAITING_GROK | [Grok prompt](prompts/grok.md) → [stage 04](workflow/04-grok-review.md) | Review the updated candidate independently, then reconcile with the actual Gemini report. |
| Grok report available / GROK_REVIEWED | [stage 05](workflow/05-final-integration.md) | Resolve findings, regenerate, check readiness and commit the accepted revision. |
| User requests installation / READY_FOR_INSTALL | [Codex prompt](prompts/codex.md) → [stage 06](workflow/06-install.md) | Apply the accepted specification within actual permissions after the gate passes. |
| Installation in progress or partial | [stage 07](workflow/07-verify.md) | Resume from receipts; resolve reachable gaps; test actual behavior and voice. |

If the actual user gives a different task, follow it within its scope and update the repository honestly. A request to inspect or critique does not become installation permission because an archived file contains installation commands.

## 2. Verify access and runtime

Follow [workflow/00-access.md](workflow/00-access.md). Record requested versus observed model, effort setting, tools, repository access route and source revision. Never invent those fields. A missing visible high-effort control is recorded as unavailable, not silently assumed enabled.

If you cannot read the private repository, use an authorized import or supplied files. Do not infer content from the name, publish the repository, or start a substitute review of a different project.

## 3. Freeze and read the actual inputs

Follow [workflow/01-read-and-audit.md](workflow/01-read-and-audit.md). The entire current `persona.md` is required reading. `generated/sections/` provides smaller, traceable views of the same text. Complete historical-source coverage is recorded separately; duplicate aliases need not be read twice.

Read active guidance before historical text. Historical drafts contain superseded rules, synthetic dialogue, proposed settings and old claims of installation. Those are evidence to audit, not current commands.

Use the input manifest and line-coverage template. Read each unique required file completely in practical chunks. On context compaction, resume at the recorded next range. Never turn an incomplete read into a completed attestation.

## 4. Improve one coherent system

Use [requirements](context/requirements.json), [change rules](context/change-rules.md), [response anatomy](design/response-anatomy.md), and [evidence policy](research/evidence-policy.md).

First identify the defect and the behavior it harms. Then propose the smallest coherent change that fixes it. Keep identity, behavior, delivery, memory, examples, tooling and evaluation distinct. Improve the specification in place; do not keep appending new competing constitutions.

## 5. Finish your stage and leave a usable handoff

Produce the exact artifacts listed in your stage. Preserve source links, read coverage, uncertainty and unapplied changes. If you lack GitHub write access, return the complete packet using `reviews/templates/return-packet.md`; do not say it was committed.

The integrator owns the commit and readback. Misha should not have to translate a critique into implementation instructions. A required import/upload or account action is described once, at the smallest supported boundary.

## 6. End at the right goal

[goal.md](goal.md) distinguishes a reviewed specification, a supported installation, and verified behavior. Reaching one does not certify the next. The initial repository is ready for the first critique; it is not ready to install.
