# Stage prompts

Use one prompt with the correctly imported/current public repository. Model names and effort controls must be verified in the actual app.

- [Gemini first critique](gemini.md)
- [Grok second critique](grok.md)
- [Review-packet integrator](integrator.md)
- [Codex installation after both critiques](codex.md)

These prompts route work; they do not make unavailable connectors or model settings appear. A standard Gemini GitHub import is read-only and does not refresh itself. See [access](../workflow/00-access.md).

## Initial repository creator

`bootstrap-codex.md` routes the worker receiving the self-contained outer file. Its historical task was private repository publication; current visibility is public by explicit owner instruction, then stop ready for Gemini. Later reviewers and the final installer use their own prompts and actual phase.
