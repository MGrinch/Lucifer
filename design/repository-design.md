# Repository design and decisions

## Intended result

A portable handoff in the owner-selected public repository that a new worker can read without this chat, improve through two attributed critiques, and then use to install and verify the accepted persona. Private target settings and rollback copies remain private. The repository must distinguish review completion, content acceptance, settings application and actual behavior.

## Architecture

The current `persona.md` remains the sole normative specification. An immutable R1 copy and recovered originals preserve provenance. Small generated sections make complete reading tractable; payloads and evaluation cases are derived mechanically. Ordered workflow documents guide reviewers, the integrator and the installer. A machine-readable stage record and a fail-closed readiness check prevent accidental installation before the two real critiques.

## Approaches considered

1. **A single giant prompt only:** portable, but difficult to audit, easy to partially read, and weak at preserving review sequence or exact application status.
2. **Many independently editable persona files:** easier to browse, but risks duplicate authority and contradictory adapters.
3. **One canonical file plus generated views and explicit review records:** selected design. It preserves the requested one-file handoff while adding navigable context and verifiable transitions.

These are engineering choices made for the user's explicit repository request, not a claim that he selected a menu of architectures.

## Boundaries

- A private GitHub URL is not an access credential. Review input can arrive through an authorized connector or file import.
- Reviewer training background is not evidence that it searched Google, YouTube or X. Actual retrieved sources are recorded.
- Content fingerprints can identify the reviewed bytes even when an import cannot see Git commit metadata. Supplied versus independently verified commit IDs remain distinct.
- The readiness tool checks records and integrity. It cannot authenticate model identity, prove a human heard audio, judge all prose quality, enforce GitHub branch protection, or prevent a user from editing the checker. Do not overstate it.
- This repository's scripts do not call an LLM, change native settings, access credentials or install software.

## Dependency order

Original corpus → current candidate → Gemini input snapshot → Gemini report → accepted Gemini changes → Grok input snapshot → Grok report → reconciliation → accepted `main` revision → Codex inventory/application → native behavioral and voice evidence.

The second pass may reject a Gemini proposal with evidence; it may not erase the first report. Final integration may change the candidate to resolve Grok findings, but those changes must be recorded, validated and covered by the final integration receipt. Unrelated post-review edits invalidate readiness.

## Initial publication scope

Create files, derive payloads, verify navigation and integrity, and publish privately. Do not run either future critique, link the user's Gemini/Grok accounts, or install the persona during repository preparation.
