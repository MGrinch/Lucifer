# 03 — Integrate Gemini and prepare Grok

## Preserve and verify

Save Gemini's original report and attachments exactly as returned. A formatting-normalized structured record is allowed, but the original remains available. Attribute the review truthfully; a writer that imports it is not its author.

Check the input fingerprint, reading coverage, runtime metadata and cited evidence. Open material sources before relying on them. Separate unavailable evidence from a negative finding. Reject fabricated source URLs, guessed timestamps and unsupported “tested” claims.

## Resolve every finding

For each finding record one disposition: accepted and implemented, rejected with reason, deferred with scope/next action, or blocking. Preserve the reviewer's proposal even when rejected. Map accepted edits to requirement IDs, canonical sections and test effects.

Apply coherent accepted changes to `persona.md` and relevant authored guides. Keep originals immutable. Do not change Misha's taste under the label of optimization. Preserve meaningful existing examples and add variety where the actual audit shows a gap.

## Verify and merge

Regenerate derived content. Run integrity checks and repository tests. Inspect the actual diff for lost requirements, stale citations, prompt expansion and contradictions. Static success is not a target-model persona pass.

Record Gemini's input fingerprint, the integrated output fingerprint, the original report/source/findings digests and every decision in `integration.json`. Use the schema in `tools/README.md`. If a blocking issue remains, leave the stage blocked and state the precise missing evidence or owner decision.

Commit the accepted changes and review artifacts through the actual supported writer. Prefer a dedicated branch and merge into `main`; verify the resulting files/commit. Do not claim a merge before it occurred. No second permission ritual is needed for ordinary in-scope edits already requested by Misha.

## Prepare the second pass

Freeze Grok's input from the Gemini-integrated candidate using the documented command. Include the preserved Gemini review packet separately. Grok's record must pin the actual Gemini integration digest and attest that it read the report and decisions; that digest transitively pins the first review's artifacts. Set the stage to `AWAITING_GROK`. A stale Gemini app import does not update itself after this merge.

Next: [04 — Grok critique](04-grok-review.md).
