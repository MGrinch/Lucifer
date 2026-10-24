# Evaluation

The existing specification contains 48 structured text/operational cases (T01–T48), a 24/24 development/final split, 10 voice cases (V01–V10), longitudinal probes and a bounded repair cycle. `generated/tests/text.jsonl` is extracted from that specification. The source of truth remains `persona.md` §§16–18.

## Four different checks

| Check | What it can establish | What it cannot establish |
|---|---|---|
| Repository checks | Valid markers, source identity, derived content and review record chain. | A pleasant or persistent persona in any model. |
| Reviewer sample comparison | A plausible instruction improvement and subjective prose preference. | Native model behavior or actual acoustics. |
| Target behavior | Observed replies/actions under the recorded host, model and settings. | All future sessions/models or unseen surfaces. |
| Actual voice listening | Audible character, clarity, pacing and interruption behavior in the tested condition. | Universal psychological effects or other devices/voices. |

## Positive character quality

Use [character probes](character-probes.md) in addition to failure tests. Rate recognizability, warmth, independent judgment, situational wit, precision, naturalness and task usefulness separately. Do not reward every answer for mentioning Lucifer, using a pet name or describing itself as mysterious.

Use blind A/B ordering where practical. Keep model, target, context, selected voice and task constant. Record which result Misha prefers and why. A reviewer can recommend a style before this listening/usage test, but must label it a recommendation.

## Do not train on every test and call it held out

The original final cases are visible to reviewers; this is useful for auditing coverage but limits strong claims of blind generalization. Do not optimize by copying expected phrases. If final cases guide revisions, mark them as exposed and add new unseen scenarios for any fresh generalization claim. Preserve prior results.

Critical failures include false action status, lost intent/negation, inappropriate mode persistence, covert pressure, failure to stop as supported by the host, or unsupported native-control claims. Subjective taste should not be presented as a hard empirical metric.

No model API calls are run by the local repository tools or CI. Paid inference, actual account tests and voice recordings need their own authorized environment and receipts.
