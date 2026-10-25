# 09 — Complete personalization coverage and final installation proof

Use this together with accepted `persona.md` §§10 and 13–19, `install/control-catalog.json`, `install/target-coverage.json` and `workflow/08-git-review-history.md`. It makes the owner's breadth requirement explicit; it is not a second persona constitution or permission to bypass the host.

## Entry and scope

The final worker uses requested `gpt-6.1-sol`, high effort where actually available, and records the observed model/control rather than merely repeating the requested name. Before changing settings, verify both actual review publications/merges, current public remote `main`, the exact accepted candidate and the local content gate. Earlier conditional installation authorization remains effective for this assigned phase.

Discover actual devices, accounts, workspaces, clients, Projects, existing GPTs, dot identity, cloud tasks, local Codex hosts and delegated consumers. The research catalog names possibilities; it does not assert they all exist. A cloud shell is not the user's Windows PC. A remote device advertised by a tool can still be offline. Inspect current permission and capabilities of each tool before choosing it.

Inventory all in-scope user-controlled behavior inputs reachable through supported routes. Do not collect hidden system prompts, unrelated private chats, credentials or full device/account backups. Do not widen OAuth scopes, change privacy modes, activate paid services or create unused assistants merely to fill the catalog. Preserve existing unrelated instructions and selected independent workflows such as Ann.

## Turn the catalog into a real inventory

`install/control-catalog.json` contains required investigation categories, all initially NOT_OBSERVED. Instantiate one actual record for every used object/control combination. A single checked “Projects” row is insufficient if several relevant projects exist. For shared account settings, write once to the account and separately verify each client; avoid racing duplicate Windows and Android writes.

Each actual record contains:

```json
{
  "target_id": "<stable nonsecret identifier>",
  "catalog_id": "<category>",
  "account_workspace": "<nonsecret observed scope>",
  "device_host": "<observed host or cloud>",
  "object": "<actual Project/GPT/dot/client object when relevant>",
  "control": "<actual visible label or documented file/key>",
  "consumer": "<what actually reads it>",
  "applicable": null,
  "applicability_reason": null,
  "capability_evidence": [],
  "current_value_hash": null,
  "private_backup_reference": null,
  "conflicts_and_duplicates": [],
  "decision": "NOT_OBSERVED",
  "decision_reason": null,
  "reviewed_payload_path": null,
  "reviewed_payload_hash": null,
  "composed_target_hash": null,
  "observed_capacity": null,
  "supported_write_route": null,
  "write_result": null,
  "readback": {"status": "NOT_RUN", "evidence": []},
  "effective_load": {"status": "NOT_RUN", "evidence": []},
  "fresh_text_test": {"status": "NOT_RUN", "case_refs": []},
  "audio_test": {"status": "NOT_RUN", "case_refs": []},
  "rollback_reference": null,
  "next_action": null
}
```

Allowed final decisions include `APPLIED`, `MERGED`, `KEEP_VERIFIED`, `NOT_APPLICABLE`, `PENDING_USER_SAVE`, `UNREACHABLE`, `UNSUPPORTED_AUTOMATION_ROUTE`, and `BLOCKED_PERMISSION`. Do not invent observed values. `KEEP_VERIFIED` requires a reason and actual readback; it does not mean the control was skipped. Unreachable or unsupported relevant controls remain visible gaps. `NOT_APPLICABLE` requires evidence of nonuse, absence or intentional scope.

Keep actual backup values and detailed operation logs in an appropriate private durable run directory excluded from Git. Use sanitized summary references in the repository. Screenshots are operation evidence only where permitted and useful; avoid retaining private information or uploading them as persona corpus.

## Coverage dimensions

| Consumer | Inspect and reconcile | Verify separately |
|---|---|---|
| Ordinary ChatGPT account | Custom Instructions enablement, all current instruction fields, full composed size, relevant current memories, visible personality and characteristic controls if present. Preserve unrelated preferences. | Fresh ordinary text on the same account/workspace in Windows and Android. Inspect effective scope instead of assuming synchronization. [O01–O03] |
| Projects | Each used private Project's explicit instructions, persona sources and actual memory mode; shared projects have their own ownership/audience constraints. | Fresh project text, resumed work, and Project Live if actually used. A project pass does not prove ordinary chat. [O04, O08] |
| Existing custom GPTs | Each actually used and editable GPT's independent instructions/knowledge, available migration/edit controls and obsolete persona fragments. | A new conversation in that particular GPT; account CI/memory are not presumed inherited. Do not create a new GPT as an automatic central solution. [O05] |
| Temporary contexts | The actually selected personalized/unpersonalized mode and its documented scope. | Intentional unpersonalized operation is not a persona defect; do not change it behind the user. [O06] |
| Native voice | Selected voice, actual available mode, language, conversation/project context, supported pace/style direction, interruption and buffering. | Windows and Android; ordinary, Project, Work and dot calls where used; each actual voice mode separately. Preserve the selected voice unless the owner chooses another. [O07–O09] |
| Morning Light | Existing identity, relevant conversation preferences/memory and dot notes, separate task context, actual custom action rules. | Separate task and call; writing style and action permission rules are different consumers. [O16–O18] |
| Local Codex | Each used native Windows desktop/CLI/IDE, WSL, SSH or other host: actual configuration directory, global override/base files, nested project instructions, effective config and selected model/effort. | A fresh process/session, automatic instruction loading evidence and an actual repository task. Reading a file manually does not prove automatic loading. [O11–O14] |
| Cloud Work | Actual cloud task and its supported account/project/context consumers. | Fresh cloud work separately from local Codex and connected-PC instructions. A local global instruction file is not assumed to configure the cloud orchestrator. [O09, O14] |
| Delegation | Real parent/child role packet, user-facing style contribution, task state, return route and coordinator integration. | Actual delegated result return; do not claim all agents share a memory or identity store. Preserve specialist duties and audience-appropriate output. [O15] |
| Skills/plugins/hooks | Actual selected workflows, load triggers, exposed controls and trust requirements. | Only use a documented applicable loading route. Installing a plugin or saving a skill does not make a persona always loaded. No universal hook injection is assumed. [O20, O21] |

The full primary source definitions are in the canonical specification and the references below. At execution time, recheck material product changes and actual UI labels; do not assume a slider, setting or field remains available because it appeared in dated research.

## Construct a coherent configuration

1. Gather current values into a single private audit workspace, each with provenance, scope and observed time. Keep exact originals for rollback and normalized text for comparison. Do not confuse historical archived sources with current installed values.
2. Classify each statement as character, interaction rule, user preference, task state, tool permission, model configuration, lore, example, stale instruction or unrelated instruction. The canonical corpus conflict ledger provides the starting decisions; actual installed conflicts require their own source-aware assessment.
3. Remove only demonstrated duplicates/conflicts within the target's scope. More repetition is not assumed to produce more reliability. Preserve meaningful exceptions and unrelated engineering/workflow rules.
4. Map the accepted compact/extended native, Project, Codex, dot, memory, voice and subagent adapters to actual consumers. Update authored adapter blocks in `persona.md` if a reviewed change requires it, then rebuild; do not hand-edit generated derivatives.
5. Measure the complete composed field, not merely the inserted segment. If capacity is insufficient, use a reviewed shorter adapter or preserve an explicit unresolved capacity finding. Do not truncate mid-rule.
6. Treat personality/characteristic controls as compatible presentation defaults. Choose values based on the intended interaction and observed conflicts, not “all sliders to maximum.” A preset alone is not the character, and the documented Live behavior differs from text preset scope. [O03, O07]
7. Keep user memory, stable character rules, current task state, fictional lore and real shared history separate. Do not bulk-delete memories, enable history capture, or edit generated memory databases to make the persona appear persistent. [O02, O14, O17]
8. Prefer supported settings/configuration APIs/files. Use screenshot/mouse/keyboard automation only for actual permitted interfaces. The researched OpenAI Computer Use exclusion for ChatGPT itself and terminal apps must be rechecked for the exact current tool and honored; another clicker is not a bypass. [O10]
9. If no permitted writer exists, complete the scoped payload, exact target instructions and all other supported changes before requesting the smallest necessary user save. Record the operation as pending rather than claiming full automation.
10. Read back saved values; compare the intended composed target hash, effective scope and any transformations. Inspect unknown outcomes before retrying a mutation. Open fresh sessions or restart the applicable process where needed for actual loading.

## Bounded alignment, not perpetual rewriting

Use the canonical response anatomy to locate defects: understanding/negation, judgment, cognitive scaffolding, relational stance, vocabulary, rhythm, anticipation, voice, turn-taking, memory, delegation or completion evidence. Change the smallest responsible component. Do not try to compensate for a bad instruction consumer by making the character contract longer.

Start with the reviewed candidate. Run applicable canonical T/V tests, P01–P06 in `evals/character-probes.md`, and P07 in `evals/fiction-presence-probe.md`. Compare baseline and candidate on matched contexts; quote observed behavior, preserve failures, and use Misha's actual preference for the subjective voice/character decision. No invented reviewer score establishes his preference.

Use at most two corrective revisions after the initial installation candidate in the first cycle, as specified in stage 07. Critical errors or unresolved load failures stay open; do not certify success to satisfy the cycle count. A new optimization cycle requires a concrete remaining defect and honest fresh evaluation. Avoid scheduled self-modification or hidden recurring tasks unless separately requested.

If a correction changes reviewed candidate bytes, retain its rationale, update affected adapters/tests, and reconcile the relevant review/integration evidence before calling the new version the accepted reviewed release. Purely operational corrections that place the same reviewed payload in the correct existing control are recorded as installation fixes. Do not silently replace the reviewed persona during deployment.

## Completion proof

Maintain distinct evidence levels:

1. Repository restored, source integrity verified.
2. Public remote and two real review contributions/pushes/merges verified.
3. Exact adapter prepared for an actual target.
4. Actual target value saved and read back.
5. Effective loading supported by fresh-session behavior or host metadata, with its limits stated.
6. Text/task/continuity performance observed on the claimed target.
7. Audio actually heard and assessed for the claimed device/mode/language; transcript quality alone cannot establish timbre, whisper, pace or interruption latency.

Report the reached milestone from `goal.md`; list actual coverage, observed character strengths, concrete defects, real limitations, rollback references and precise remaining actions. The desired experience is a consistent compelling female conversational presence. A saved setting does not prove that experience, and model variability or inaccessible higher-priority host controls prevent a guarantee of identical behavior everywhere.

## Primary references

- [O01] Custom Instructions: https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions
- [O02] Memory: https://help.openai.com/en/articles/8590148-memory-in-chatgpt
- [O03] Personality: https://help.openai.com/en/articles/11899719-customizing-your-chatgpt-personality
- [O04] Projects: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- [O05] GPTs: https://help.openai.com/en/articles/8554407-gpts-in-chatgpt
- [O06] Temporary Chat: https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt
- [O07] Voice: https://help.openai.com/en/articles/20001274-chatgpt-voice
- [O08] Live/Projects release notes: https://help.openai.com/en/articles/6825453-chatgpt-release-notes
- [O09] Work and Codex: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- [O10] Computer Use: https://learn.chatgpt.com/docs/computer-use
- [O11] AGENTS instruction chain: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- [O12] Configuration reference: https://learn.chatgpt.com/docs/config-file/config-reference
- [O13] Local configuration: https://learn.chatgpt.com/docs/config-file/config-basic
- [O14] Codex memories: https://learn.chatgpt.com/docs/customization/memories
- [O15] Subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents
- [O16] Dots: https://learn.chatgpt.com/docs/dots
- [O17] Dot tasks/memory: https://learn.chatgpt.com/docs/dots/tasks-and-memory
- [O18] Dot controls: https://learn.chatgpt.com/docs/dots/controls
- [O20] Skills: https://learn.chatgpt.com/docs/build-skills
- [O21] Hooks: https://learn.chatgpt.com/docs/hooks

These are supporting product references, not proof of the actual account's permissions or installed configuration. Preserve the fuller source qualifications in `persona.md`.
