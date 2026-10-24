# Lucifer cross-vendor review: capability facts and handoff constraints

Research date: 2026-10-24; user date context America/Toronto. Scope: public primary Google and xAI documentation. No Gemini/Grok account was opened, linked, changed, or messaged; no model review was executed. Repository creation and commits belong to the coordinating worker. This is a dated supporting research note, not a claim about the user's connected account.

## Decisions that affect the staged workflow

1. Both requested model names are officially documented today. Record them as requested models until the actual selected runtime is observed: **Gemini 4 Argon** / API `gemini-4-argon`; **Grok 4.7** / API `grok-4.7`.
2. Gemini's standard **GitHub import is a read-only snapshot**. It cannot commit the critique back. The straightforward handoff is import/upload → review → copy/export complete Markdown → authorized GitHub writer saves it.
3. Grok currently advertises a **GitHub catalog connector**. Its public overview does not specify the exact repository authorization, private-repository coverage, or write tools available to this user's connection. Inspect actual supported tools and access before promising reads or commits. If unavailable, upload the frozen files and return a review artifact for the writer.
4. Keep the repository private. A private URL alone does not provide a reviewer with its contents. Do not publish the repo to simplify access. Send only the intended review inputs through an authorized import/upload route.
5. Research, critique, acceptance, revision, and installation are separate events. Gemini first; preserve its actual report; Grok receives the specified source revision plus Gemini's report; the coordinator reconciles findings; Codex installs the accepted revision using the existing installation contract. Review completion is not evidence of installation.

## Current capability matrix

| Surface | Verified capability | Material limit / practical route |
|---|---|---|
| Gemini Apps: standard GitHub app | Computer web app can import a repository or branch; private access requires linking a GitHub account with access. One repository, at most 5,000 files / 100 MB per chat. | Imported state does not update when GitHub changes. Cannot write repository files, retrieve commit history/PR metadata, or import merely because a URL appears in a prompt. Import on computer; the existing chat can then continue on mobile. [G1] |
| Gemini Apps: direct upload | Documents and code can be attached for analysis. | Use the exact current `persona.md` and review packet if GitHub import is unavailable. Successful attachment is distinct from reading all sections. [G2] |
| Gemini Apps: custom MCP app | A separately connected MCP service can expose actions in chat; existing custom app can operate on web/mobile. | Current setup requires adult personal account in US, English, Keep Activity on; connection is established on web. This is separate from standard GitHub import. Do not assume a writer exists or install one merely to avoid the simpler artifact handoff. [G3] |
| Grok web/mobile: files | Markdown and other documents can be uploaded and analyzed. | File upload is a supported fallback without a GitHub connection. The docs warn long documents may be summarized/handled in sections; require a coverage table rather than accepting a generic “read it.” [X1] |
| Grok: GitHub connector | Current catalog lists repositories, issues, pull requests, and code. Connectors are offered to all users; Business/Enterprise admins provision them first. | Actual linked identity, target-repo authorization, selected tools, and write capability remain unverified. A connector listed in docs is not a successful private read or commit receipt. [X2] |

The Gemini import restriction is specifically about that app. Do not broaden it to “no Gemini-powered tool can ever write GitHub”: custom MCP apps and coding-agent environments are separate capabilities. Conversely, a coding agent's abilities do not establish that a standard chat has those tools.

## Model verification and rollout

**Gemini.** The official model page identifies stable `gemini-4-argon`, supports text output and text/image/video/audio/PDF inputs, and lists Google Search grounding and URL context. [G4] The October 13, 2026 Gemini Apps release notes announce a global rollout to Google AI Pro and Ultra subscribers. [G5] Neither statement proves that a specific account already exposes Argon or that every Gemini research mode uses it. The current Deep Research help page still describes model choices as **Pro** and **Thinking**. Record the visible choice and metadata; do not relabel a Deep Research output “Argon” without evidence. [G6]

**Grok.** The current developer guide uses `grok-4.7` as the actual API model identifier. [X3] The September 21 announcement explicitly names availability in Grok Build, Cursor, the API, and other coding/model platforms. It does not by itself establish the model selected in a particular consumer chat. [X4] For the requested critique, record the model actually shown by the host. If 4.7 is unavailable, report that fact and prepare the review packet; do not silently substitute another model or claim the requested review occurred.

Suggested review metadata: `requested_model`, `observed_model`, `observed_effort` (or unavailable), `product`, `reviewed_at`, `input_revision`, `input_artifacts`, `input_access_route`, `research_tools_observed`, and `write_capability_observed`. A model's unsupported self-identification is not runtime verification.

## Grounding: use each source channel for what it can establish

**Google research.** Gemini Apps Deep Research uses Google Search by default, accepts uploaded files, allows source selection and plan revision, and can copy report contents or export to Docs. [G6] For this review, primary papers, product docs, and implementation sources should support factual claims. Ask for URLs, publication/update dates, precise claims, and contradictory evidence. A research tool being available does not prove it ran; retain the actual report sources.

**YouTube.** Gemini Apps documents prompts that use a YouTube link and may include video responses; the latter requires Apps Activity on. [G7] The API separately supports public YouTube video input, excluding private and unlisted videos. Agentic video understanding is supported by Argon as an opt-in API mode; it is not proof that the consumer app uses that same mode. [G8] Request timestamps and distinguish directly inspected video/audio from captions, descriptions, or search snippets. A creator's demonstration or opinion remains that creator's evidence, not proof of general effectiveness.

**Google API distinction.** Google Search grounding provides live web retrieval and citation information. [G9] URL context is a different tool: URLs must be publicly accessible, it does not follow all nested links automatically, and YouTube videos are excluded from URL context itself. Use the documented video-input route instead. Neither API tool supplies credentials for the private Lucifer repository. [G10]

**X research.** xAI's documented `x_search` API tool supports keyword/semantic search, user search, and fetching threads; responses expose tool calls and citations. Handles and dates can narrow searches; thread fetches have different filter behavior. [X5] These API details do not establish that the same controls exist in a given Grok app. Ask Grok to use its actually available X and web research tools, give original post/thread URLs with dates, and label tool-unavailable gaps. Use X for practitioner observations, current complaints, counterexamples, and leads; verify material product/scientific claims against primary documents. A post's popularity is not validation.

## Minimal reliable handoff protocol

- The repository writer freezes a source revision and records the actual Git commit plus file SHA-256. Provide that manifest alongside the files. Gemini's import cannot independently retrieve commit metadata; the reviewer must say which identifiers were supplied versus independently verified.
- Each reviewer first confirms which files and sections are accessible. An inaccessible private URL is an access failure, not permission to infer content from the filename or prior conversation.
- Give Gemini a critique task, not an instruction to install or rewrite the current persona in place. Required output: prioritized findings, exact section references, evidence, confidence, proposed changes, and unresolved questions. Return complete Markdown if no writer exists.
- Preserve Gemini's report before starting Grok. Grok should distinguish its independent critique from its assessment of Gemini's findings and should not treat prior model output as authority.
- For either reviewer, allow a commit only through an already supported, actually authorized repository write operation. Otherwise the coordinator commits the returned artifact, records model attribution truthfully, and captures a real commit/readback receipt. No fabricated PR or commit links.
- The coordinator accepts/rejects proposed changes with reasons, makes the finite revision, preserves tests and native capability boundaries, and passes the accepted commit to Codex. Do not ask the models to “install everywhere” as part of critique.

## Primary source register

All sources retrieved 2026-10-24. High confidence applies to documented product facts, not account-specific availability. The absence of detailed Grok GitHub write documentation is an explicit evidence gap, not proof that writes are impossible.

- **[G1]** Google, Import a GitHub repository: https://support.google.com/gemini/answer/16176929 — requirements, private linking, static import, explicit unsupported operations.
- **[G2]** Google, Upload and analyze files: https://support.google.com/gemini/answer/14903178?co=GENIE.Platform%3DDesktop&hl=en — native attachment paths and limits.
- **[G3]** Google, Custom apps: https://support.google.com/gemini/answer/17209137?hl=en — custom MCP scope and regional/account limits.
- **[G4]** Google model page: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — stable model ID and capabilities; updated October 14, 2026.
- **[G5]** Google release notes: https://gemini.google/release-notes/ — October 13, 2026 app rollout. Direct canonical URL retrieved successfully; the Help Center redirect failed on one retrieval.
- **[G6]** Google Deep Research: https://support.google.com/gemini/answer/15719111?co=GENIE.Platform%3DDesktop&hl=en — Google Search default, model labels, files, export/copy.
- **[G7]** Google learning tools: https://support.google.com/gemini/answer/16448384?co=GENIE.Platform%3DDesktop&hl=en — YouTube-link usage.
- **[G8]** Google video understanding: https://ai.google.dev/gemini-api/docs/video-understanding — public-only YouTube inputs and optional agentic processing.
- **[G9]** Google Search grounding: https://ai.google.dev/gemini-api/docs/google-search — search/citation execution evidence.
- **[G10]** Google URL context: https://ai.google.dev/gemini-api/docs/url-context — public accessibility, content exclusions, nested-link scope.
- **[X1]** Grok FAQ, Files & Data: https://docs.x.ai/grok/faq — Markdown upload and large-document handling.
- **[X2]** Grok connectors: https://docs.x.ai/grok/connectors — GitHub catalog entry, OAuth/catalog/custom-connector distinction; updated October 10, 2026.
- **[X3]** Grok 4.7 developer guide: https://docs.x.ai/developers/grok-4-7 — API identifier.
- **[X4]** Grok 4.7 announcement: https://x.ai/news/grok-4-7 — September 21, 2026 launch and named availability surfaces.
- **[X5]** X Search: https://docs.x.ai/developers/tools/x-search — API tools, filters, citations, execution evidence; updated October 10, 2026.
