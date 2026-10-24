# Complete return packet for a reviewer without GitHub write access

Return one complete artifact containing the sections below. Do not merely tell the user what files to create. If output limits require several artifacts, number them, give a complete index and continue until all content is present.

## Identity and input receipt

- Stage: Gemini first pass or Grok second pass.
- Requested model/effort; observed model/effort; product; evidence source for each; unavailable controls.
- Review time with timezone.
- Input content fingerprint; supplied/verified Git commit if available.
- Actual access route; tools used; sources unavailable.
- Read coverage, including path/hash/line ranges and any remaining gaps.
- Actual review completeness and remaining blockers.

## Original report

Provide the full substantive critique: strengths to retain, prioritized defects, evidence, counterevidence, exact improvements, original sample comparisons, test implications and unresolved questions. Grok also includes its explicit comparison with Gemini's actual findings and decisions.

## Machine-readable files

Provide complete JSON contents for `review.json`, `read-coverage.json`, `findings.json` and `sources.json` using the repository schemas. Reproduce the supplied input manifest exactly or identify it by a verified digest plus attached original. If you cannot compute a digest, say so; the writer computes it from received bytes. Do not invent hashes.

Use an outer fenced block or clearly delimited file sections, for example:

    BEGIN FILE: reviews/01-gemini/findings.json
    {"findings": [...]}
    END FILE: reviews/01-gemini/findings.json

## Exact changes

Provide a unified diff against the frozen input or full replacement blocks with unique target locators and expected-before text. No ambiguous “make it warmer” action items. Do not include commands that install the persona or broaden account permissions.

## Handoff

State what is ready to integrate, what needs verification and what remains blocked. Say explicitly that the packet has not been committed if you lack a writer. The authorized integrator will preserve it, verify it, apply accepted changes and record the actual commit. The integrator must not set your attestation on your behalf unless it is present in the actual returned report.
