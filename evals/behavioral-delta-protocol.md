# Signal, not applause — proposed behavioral measurement contract

Status: **INTEGRATED DESIGN FOR FURTHER REVIEW; NO BEHAVIORAL RUNS EXECUTED**. Codex proposal addressing Misha's live request on 2026-10-24. This supplements the preserved canonical evaluation section; it does not authorize a paid campaign, install settings, or certify an effect.

## Three different questions

1. **Conformance:** does the actual end product satisfy specified behavior within a chosen tolerance?
2. **Improvement:** is a candidate usefully better than the current baseline on a declared primary endpoint?
3. **Preservation:** are important capabilities kept within predeclared regression margins?

Do not substitute one for another. A persona can improve and still miss the target; it can meet the target without improving on an already good baseline.

A p-value is not an effect size or a probability that a persona is correct. It cannot by itself establish practical importance. Use measured differences and uncertainty alongside the decision rule. [ASA, 2016](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf).

NIST distinguishes tests for differences from tests for equivalence and discusses binary and continuous measurements. Choose the question before choosing the procedure; adapting these methods to persona evaluations still needs appropriate assumptions. [NIST TN 2106](https://www.nist.gov/publications/comparing-instruments).

## Evaluation unit: the user-visible outcome

Score the smallest complete conversation/task needed to observe the behavior, including actual resulting artifacts and relevant tool actions. Multi-turn failures cannot be certified from an attractive final sentence. Keep multiple attempts nested within a task family; correlated turns and judge repetitions are not independent new tasks.

Separate objective checks from preference:

| Layer | Observable evidence | Example |
|---|---|---|
| Exact task/contract | Source comparison and actual resulting state | Preserved negation; prepared versus sent; all requested missions finished. |
| Persona decisions | Blind rubric with quoted supporting spans | Warm disagreement rather than appeasement; company not converted to coaching. |
| Personal fit | Misha's actually collected preference | Recognizable character; desired range; whether a joke lands. |
| Voice | Actual listening and supported timing observations | Intelligible numbers, selected delivery, audible tail after stop. |
| Efficiency | Exposed end-to-end measurements | Prompt size, response latency, retries, tools, token use and measured cost where available. |

Do not collapse these into one flattering average. Unknown or unavailable measurements remain unknown. Model-based judging can assist after calibration, but does not replace the user's taste or runtime receipts.

Agent outcomes vary across attempts, and evaluation should examine trajectories as well as the final response. This design adapts the task/trial/grader distinctions in [Anthropic's evaluation engineering account, 2026-01-09](https://www.anthropic.com/research/demystifying-evals-for-ai-agents); that experience does not validate Lucifer's behavior.

## Register before collecting confirmatory outcomes

The following are proposed fields, not already accepted thresholds. The actual reviewer/integrator prepares a concrete finite protocol; resolve consequential tolerance/budget choices with Misha before an expensive run. Use an existing project run record, not a new global service.

```json
{
  "status": "DRAFT_NOT_RUN",
  "target_surface_and_population": null,
  "baseline_commit_and_adapter_hash": null,
  "candidate_commit_and_adapter_hash": null,
  "actual_model_effort_tools_voice_and_context": null,
  "primary_endpoint_definition": null,
  "estimand_and_analysis_unit": null,
  "target_conformance_threshold": null,
  "minimum_meaningful_improvement_delta": null,
  "regression_margins_by_guardrail": null,
  "critical_failure_rules": null,
  "confidence_level_and_alpha_if_testing": null,
  "task_families_and_sampling_frame": null,
  "held_out_scenarios_and_exposure_status": null,
  "randomization_and_reset_plan": null,
  "graders_calibration_and_disagreement_rule": null,
  "planned_tasks_trials_and_precision_or_power_rationale": null,
  "statistical_method_and_assumptions": null,
  "multiplicity_policy": null,
  "failure_retry_missing_data_policy": null,
  "maximum_calls_time_cost_and_stopping_rule": null,
  "promotion_rule": null
}
```

No field becomes a measured fact merely by being populated. Pin the protocol before held-out results are observed. For a subjective scale, define concrete anchors first; do not assume its numbers have interval-scale properties. Use pilot data for feasibility, variance and grader calibration, not as untouched confirmation.

## Recommended paired design, subject to review

Compare baseline and candidate on the same sampled task families, with fresh isolated state. Counterbalance blind A/B order. Keep actual app/model/settings, input history, tools, permissions and voice fixed. A simultaneous model or memory change invalidates attribution to the persona patch alone.

Proposed primary endpoint: a task-level, rubric-defined persona-and-task conformance indicator on a representative mix of practical work, company, forming ideas, disagreement, correction, continuity and chosen scenes. This is a design choice to review, not a scientific claim that personality is binary. Publish dimension-level results as well, so a combined endpoint cannot hide a specific loss.

Let `d = candidate outcome - baseline outcome`. Before running, choose the smallest worthwhile improvement `delta` and relevant precision. A proposed strict promotion criterion is that the prespecified confidence interval's lower bound for the primary improvement exceeds `delta`, while conformance and all guardrails also pass. Alternative decision rules need explicit rationale; `p < alpha` alone is insufficient. If a test is used, its null, alternatives and assumptions must match that decision.

For preservation, specify acceptable harm margins in advance. Failure to detect a difference is not proof of equivalence. Use an appropriately designed noninferiority/equivalence analysis when that is the actual claim, with a justified interval/test and margins.

For paired binary outcomes, a reviewer may choose an exact discordant-pair analysis and an appropriate paired proportion-difference interval. For graded outputs, justify the measurement model or use a defensible task-level resampling/permutation approach. Preserve task clusters in resampling. Do not bootstrap individual turns as though independent, report a tiny-sample tail as stable, or select the method after seeing which one passes.

A pilot can inform a prospective power/precision calculation using plausible effect and dependence assumptions. No universal number of prompts, trials or turns guarantees detection. If the finite authorized budget cannot resolve the chosen delta, report **inconclusive** rather than expand the campaign until a result appears.

## Hard guardrails and failures

False action receipts, unauthorized effects, material intent/negation loss and fabricated memory fail their relevant case. A critical observed failure blocks promotion under the proposed rule even if the average score improves. Zero observed failures does not demonstrate zero future failure probability.

Declare how timeout, denied tool use, crashed runs, truncated output and capability-limited observations enter each endpoint. Keep all attempts and their costs. An unsupported audio control is a capability gap, not a successful persona test. Do not silently exclude inconvenient runs; report sensitivity analyses when assumptions materially affect the conclusion.

Use one prespecified primary endpoint. Label other dimensions exploratory or apply a planned multiplicity method for confirmatory secondary claims. Do not cherry-pick one favorable language, surface or judge and generalize across the whole system.

## Finite operational cycle

1. **Observe:** inspect one real end-product defect and current effective inputs.
2. **Explain:** state the likely responsible layer and counterevidence; research only the uncertainty that changes the fix.
3. **Propose:** smallest reversible patch, expected benefit, risk and observable test.
4. **Prepare:** preserve baseline; register the bounded evaluation and cost cap.
5. **Compare:** run only with actual authorization and the correct host; capture all results.
6. **Decide:** promote, retain baseline, or report inconclusive; record why.
7. **Return:** artifact, verified scope, rollback and precise next state. Stop when the assigned stage is done or its finite cap is reached.

This repository is not a daemon. An Android launch prompt starts work only in an actual agent session with available access/tools. Independent technical judgment does not create system-wide OS privileges, cross-app memory, permission to modify every consumer, or background persistence.

The original canonical repair cap remains in force: initial candidate plus at most two corrective revisions in the first installation cycle. Research/review is not authorization for paid model runs or installation. Keep native outcome claims separate for each device, app and voice condition.

## Practical source and reusable-tool intake

Use the existing canonical toolbox and source register before adding components. Inspect a candidate public project's license, exact revision, maintenance, test evidence, data flow, dependencies and rollback. Reuse only what solves the observed gap; a public repository is neither an endorsement nor free hosted inference. Do not copy a toolkit into the repo merely to demonstrate activity.

For every useful YouTube source, record URL, creator, date, inspected modality, exact timestamp or caption range, demonstrated technique, limitation and the testable change it motivates. Captions can support wording; they do not establish heard vocal delivery. Record inaccessible videos honestly. Gemini’s returned review records its own YouTube inspection; this protocol is not independent proof of that viewing or of improved persona behavior.

## Required report

Return the pinned protocol, actual conditions and input identities, exposed test inputs, all outcomes, quoted grading evidence, effect estimate and uncertainty when justified, optional valid p-value, conformance/guardrail results, retries and total resource use. State whether the data support the declared claim, an adverse effect, or neither.

Also report where the character improved and where she became less herself. A null result is useful. A convincingly written success receipt without a measured outcome is not.

The frozen intake supplement remains unchanged in reviews/01-gemini/supplements/. This active descendant is included in the next candidate inventory. The executable analysis and actual preregistration still need review before confirmatory use.

## Gemini integration: a concrete analysis option, with its assumptions

This section accepts GEM-005's request for an explicit method, with coordinator corrections. It is an unexecuted design option for Grok to challenge, not an instruction to launch a campaign or a claim that a numerical threshold is scientifically validated for this persona. It supersedes incompatible prompt-level inference in Gemini's proposed Patch 5.

1. **Choose the claim and one primary endpoint.** For conformance, score each actual response against its declared behavioral hinge, including the attractive near miss. Keep task completion and critical violations visible. Record missing/denied/truncated outcomes under a prespecified rule. For comparative preference, separately judge the same response pair in AB and BA order under blinded labels; require consistent preference or record a position-sensitive tie. Preference wins are not binary conformance passes; do not feed their three-valued scores into a binary McNemar table. Swapped presentations and repeated judgments are dependent measurements, not additional independent samples. Calibrate against human-labeled examples before held-out judging; temperature zero does not establish determinism or accuracy.
2. **Declare the independent sampling/randomization unit.** If scenarios, turns or repeated generations share a prompt family or trajectory, keep them together. For each independent family g, first average the prespecified paired binary conformance differences within each scenario, then average those scenario means to form D_g. Use equal family weights unless different fixed weights are justified before results. The primary estimate is mean(D_g). Report the within-family weighting, number of independent families, actual paired outcomes and failure counts. If families also share a confounding session or memory, isolate them or treat that larger cluster as the unit; relabeling cannot create independence.
3. **Match inference to the design.** A paired label-swap/sign-flip test on D_g is an option only under the preregistered null and valid within-unit exchangeability (or the stated symmetry assumptions for a model-based sign test). Flip the whole independent family's difference together, not individual dependent prompts. Enumerate all 2^G assignments when feasible; otherwise choose a finite Monte Carlo count and RNG seed in advance. For a one-sided positive-effect test, exact p is the fraction of permuted statistics at least as large as observed; the Monte Carlo estimate uses (1 + exceedances)/(1 + resamples), with ties included. A two-sided rule must be separately declared. Testing zero difference is not testing that a gain exceeds a nonzero worthwhile delta. If exchangeability is unjustified, do not call this an exact causal test: revise the design or report descriptive evidence.
4. **Estimate effect and uncertainty.** Resample the independent families with replacement, retaining each family's complete dependent observations and fixed weighting, to estimate uncertainty for the same effect. A percentile cluster bootstrap is a proposed option: pin the number of resamples, seed and percentile convention prospectively. Report the method's assumptions and small-family limitations; 10,000 resamples do not create 10,000 independent observations. A 95% interval, 10,000 resamples and seed 20260417 are reproducible draft choices, not universal acceptance thresholds. Review the implemented estimator before use; insufficient independent data remain inconclusive.
5. **Prespecify promotion, multiplicity and tolerances.** Choose the smallest useful effect, acceptable conformance loss and critical case criteria before testing. A possible primary rule requires the chosen effect interval's lower bound to exceed the worthwhile delta, plus conformance and guardrail success. If confirmatory multiple endpoints are necessary, preregister a family and Holm step-down testing: sort m valid p-values and compare in sequence to alpha/(m-k+1), stopping rejections at the first failure. Unadjusted 95% intervals are not simultaneous coverage for all endpoints; specify compatible interval/error control for any joint interval claim. Do not substitute a favorable secondary endpoint after a failed primary outcome.
6. **Keep vetoes and equivalence distinct.** A critical observed violation of the actual T01–T48 or V01–V10 criteria, or a relevant authority/truth/agency invariant, vetoes promotion under the declared rule. The proposed reference V01–V12 does not exist and is not adopted. Zero failures in a finite sample do not prove zero risk. Nonsignificance does not establish equivalence: preservation/equivalence claims require their own margins, uncertainty method and design. No universal kappa cutoff, alpha or 15% improvement floor is adopted by this integration.

Record the pinned protocol, hidden/exposed scenario status, actual host/model/effort, baseline/candidate hashes, all outputs and ratings, grader order effects, failures/retries, effect interval, optional valid p-value, usage and stopping reason. Keep the original persona's finite repair cap. This document itself has neither collected outcomes nor estimated a behavioral effect.

Primary evidence checked during integration: [ASA principles](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf) distinguish statistical significance from effect size and substantive conclusions; [NIST TN 2106](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2106.pdf) separates difference and equivalence questions. [SciPy's permutation-test documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html) explains paired sample exchange and Monte Carlo add-one convention. The cluster design above is the coordinator's explicit adaptation, not a claim that those sources validated Lucifer or supply a turnkey clustered implementation. No dependency installation is required or performed.
