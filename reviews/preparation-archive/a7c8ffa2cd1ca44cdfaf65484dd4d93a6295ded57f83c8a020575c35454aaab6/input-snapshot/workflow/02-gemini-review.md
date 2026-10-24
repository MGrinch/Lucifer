# 02 — Gemini critique

Requested runtime: **Gemini 4 Argon**, highest appropriate exposed reasoning setting matching the user's request. Record the actual runtime and control; do not invent “high” if the app does not expose it.

## Mission

Improve the character and instruction system through a complete audit, current Google-accessible primary research and relevant YouTube demonstrations. Preserve Misha's goals. This is the first of two critiques, not an installation or a contest to rewrite everything.

## Required passes

1. Complete the input and reading protocol in stage 01.
2. Audit the persona line by line: intent, contradictions, unnecessary duplication, vague rules, response structure, voice, memory, delegation, adapter coverage and deployment realism.
3. Research the specific uncertainties. Prefer official product documentation, primary papers and source code. Use creator videos for technique demonstrations, delivery examples and leads. Record whether you inspected audio/video, captions or only descriptions.
4. Evaluate how to make Lucifer more recognizable, beautiful in expression, warm, witty and independently useful. Produce original before/after examples across ordinary company, disagreement, practical work, explanation, correction and an explicitly chosen soft-voice segment.
5. Propose exact changes, each connected to a defect, owner requirement, source and test. Prefer deletion or precise replacement over additive prompt bloat.
6. Audit every proposed new tool against the native-first route. Identify the actual gap it solves, implementation burden, data flow, cost and rollback. A free GitHub repo is not free hosted inference.
7. Return the complete review packet. If an authorized writer exists, save it without changing native settings. If not, use the return-packet template.

## Required output

Populate `reviews/01-gemini/` with the original report, structured review metadata, input manifest, read coverage, findings, sources and proposed patch/replacement blocks. The report must include strengths worth preserving, prioritized defects, counterevidence, exact changes, sample comparisons, test implications and unresolved items for Grok.

Do not manufacture findings to reach a quota. A reviewed passage can be retained with a reason. Do not call external research completed if the relevant tool was unavailable; label the limitation and its impact.

The writer sets `GEMINI_REVIEWED` only after the actual report is saved. Integration is a separate stage. Your review cannot mark itself installed or fulfill the Grok requirement.

Next: [03 — integrate Gemini](03-integrate-gemini.md).
