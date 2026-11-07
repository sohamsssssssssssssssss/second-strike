# Second Strike

One reviewer's correction becomes a human-approved rule for agents sharing a Switch room.

**P1 PASSED — 5 Nov 2026:** the fallback quant-desk room is deployed on Mattermost. Both workers returned the two fixture trades and traded_value=20000. Saved Console settings show worker-a Codex gpt-6.1-sol and worker-b Codex gpt-6-luna, both on This computer. This is same vendor, different models. R1 was approved in room chat and activated as a Second Strike custom record; it is also in the room Instructions. The fee checker ran live through gate. P4 has one treatment and one control attempt, but the control room is public and its reported model does not match; there is no valid pair yet. Historical blocked attempts below are retained as history.

**Latest P1 attempt — 4 Nov 2026:** terminal OpenCode v2.2.5 successfully answered a minimal prompt when explicitly routed to OpenAI model `openai/gpt-5.6-terra` (response: `P1-terminal-ok`; OpenCode session `ses_e583b95e1ffeB4a10iaO0ngffX`). Its configured default was instead `opencode/crouton-alpha-free`, which failed with sanitized `provider.free-limit` / HTTP 429. No Gemini-backed OpenCode worker was verified. Switch deployment and room messaging could not be performed from the non-interactive terminal harness, so no agent was created, assigned to This computer, or sent the fixture. P1 remains blocked. This is not cross-vendor evidence: the only verified terminal route uses OpenAI.

## Reproduce the room setup

Use Switch Console, Codex, OpenCode with a Gemini backend, and a local Switch server with Mattermost. Credentials belong in provider settings, never in this repository. Python 3.11+ is required for later phases; no Python dependencies are required by this skeleton.

1. Download or clone this project and read the six documents in `docs/`. A published Git remote has not been configured here.
2. Open Console → Settings → Agent providers. Confirm Codex is signed in and OpenCode says Backend connected. Configure Gemini using OpenCode's documented provider setup; VERIFY quota and actual supported model ID before running.
3. Select the local Switch server and Start. This installation runs switch-core without Docker; bundled Mattermost runs beside it in Docker. Wait for Mattermost to be available and your messaging account linked. Do not reset an existing server.
4. Select Templates → Import template → Choose file, and choose `templates/quant-desk.template.yaml`. Select Import, name it Quant desk, choose Private, and Save. This import succeeded on Console 0.40.1 / switch-core 0.31.0 on 4 Nov 2026.
5. Select Use template. Select Mattermost, enter the actual Codex and Gemini model IDs for `worker_a_model` and `worker_b_model`, and review Advanced → location. All four agents need an online machine with their provider installed and configured. VERIFY worker-b's machine: the inspected preview did not select one.
6. Review the preview: worker-a=Codex, worker-b=OpenCode/Gemini, scribe=Codex, gate=Codex; private room quant-desk; reviewer included via `{$creator}`; separate agent directories. Select Create all only after resolving prerequisites. Creation and worker replies are VERIFY, not completed.
7. Open quant-desk. Send the identical fixture below separately to worker-a and worker-b, changing only the addressed name. Require JSON trade rows, not an acknowledgement. Do not coach either worker about fees. Record the actual returned messages and thread IDs.
8. Record room/thread references, actual provider/model IDs, and returned ledgers in the tracker. Keep keys out of logs and screenshots. These smoke tests are not the unseen P4 benchmark.

The agent directories are separate from this repository. P1 tasks are delivered in chat; agents do not automatically have these six documents. Supply the necessary schema text in the task. A shared repository/checker handoff must be resolved in P2 before claiming the gate works.

## Fallback

If OpenCode/Gemini fails, record the exact sanitized failure and import `templates/quant-desk-fallback.template.yaml` as Quant desk fallback using the same steps. Select two available, **different** Codex model IDs. The form requires nonempty IDs; the operator must verify that they differ and are supported. This is **same vendor, different models**. Fallback deployment is VERIFY.

Both variants use the same agent and room names. Deploy only one. If names already exist, inspect them and resolve the collision explicitly; do not delete existing work or silently reuse agents.

## Roles and current limits

Workers produce synthetic ledgers. The scribe drafts; only the human approves. The gate is a separate agent and will run offline deterministic scripts in P2. During P1 it reports “not implemented”; it cannot issue a real pass/fail. Codex gate differs from the Gemini worker where available, but does not differ from worker-a's provider. Deterministic checking remains the intended primary gate.

Both templates keep automatic tool approval off. The kickoff addresses all four agents and asks only for introductions, avoiding an agent-to-agent message loop.

Switch currently provides the imported team/room setup. Source inspection confirms room Instructions, agent-readable documents, conversation History, and session approval records; a distinct native Rules/Decisions rule-lifecycle feature was not found. Live use in quant-desk remains VERIFY. See the evidence below before implementing P3. A local file can store rule text; no cross-vendor rule propagation has yet been demonstrated. Do not describe an imported template as a running room.

## Files and their purpose

| Files | Purpose |
| --- | --- |
| `docs/Second Strike *.md` (six files) | Original requirements, technical design, flow, schema, tracker, and guardrails; relocated without rewriting the source text, except progress appended to the tracker. |
| `templates/quant-desk.template.yaml` | Primary Codex/OpenCode team setup. |
| `templates/quant-desk-fallback.template.yaml` | Two Codex worker models if Gemini is unavailable. |
| `templates/life-room.template.yaml` | Purpose-only P6 placeholder; do not import. |
| `checkers/check_fees.py` | Purpose-only fee checker placeholder for P2. |
| `checkers/check_lookahead.py` | Purpose-only lookahead checker placeholder for P5. |
| `harness/paired_test.py` | Freezes two JSON first submissions by SHA-256 and reports their R1 checker verdicts; it does not run agents or claim an evaluation. |
| `harness/eval.py` | Purpose-only evaluation runner placeholder for P5. |
| `tasks/seeded/.gitkeep` | Keeps the future task prompt directory. |
| `eval/ledgers/.gitkeep` | Keeps the future evaluation ledger directory. |
| `rules/R1.json` | Active custom rule record, including the chat approval reference and lifecycle fields. |
| `eval/results.md` | Records P4 live first replies, checker outcomes, hash evidence, and limits. |
| `DEMO.md` | Purpose-only P7 script placeholder. |
| `.gitignore` | Excludes local credentials and Python artifacts. |
| `README.md` | P1 setup, recovery steps, file purposes, and limits. |

No CLI currently executes a demo: running the placeholder Python files does nothing. Do not treat their zero exit status as a passing test.

## Verification and sources

Codex authored the templates, skeleton, walkthrough, and tracker update. Automated local checks parsed both YAML documents and checked agent membership, required setup fields, and template differences with already-installed PyYAML; no dependency was added. Console accepted the primary template and displayed its deployment preview. These checks do not establish live responses, Gemini availability, or rule enforcement. The continuation investigation below records the current blockers. Soham's personal review is still pending.

Sources read on 4 Nov 2026: [official triage-pair template](https://github.com/sandbox-quantum/switch/blob/main/examples/agent-templates/triage-pair.template.yaml), [template language](https://github.com/sandbox-quantum/switch/blob/main/docs/TEMPLATES.md), [Console template steps](https://docs.switchagents.ai/switch-rooms/administer/room-templates), and [quickstart](https://docs.switchagents.ai/switch-rooms/getting-started). Source branch: main; immutable commit revision is VERIFY. Terminal fetching failed due to DNS restrictions; sources were read through the web tool. No Switch API client was invented or added.


## P1 continuation: observed deployment state

Inspected 4 Nov 2026. Console **0.40.1**, local switch-core **0.31.0**. Console reports the local server Running at `http://localhost:50139`; this is a local development address, not a public demo. Codex **0.166.0** is Installed / Signed in. OpenCode **2.2.5** is Installed / Sign-in could not be checked. No credentials were printed or copied into the project.

| Item | Observed result |
| --- | --- |
| Primary template | Imported privately as Quant desk; not deployed. |
| OpenCode/Gemini authentication | OpenCode auth store contains only an `opencode` provider entry, no Google entry. Global config has only its schema setting, no model/provider configuration. Shell has neither `GEMINI_API_KEY` nor `GOOGLE_API_KEY`. Console could not verify authentication. This is not proof that a Gemini key elsewhere is invalid. |
| Gemini model and quota | **VERIFY:** no authenticated Google backend or quota dashboard was available. No Gemini request was made; no quota estimate invented. |
| Primary worker-b machine | Deployment preview: **Machine Not set by the template**. No actual worker-b assignment exists. Other agents preview This computer. |
| Fallback | Existing fallback selected as recovery path: **same vendor, different models**. Import attempted but not completed; not deployed. |
| Fallback model candidates | Codex model cache fetched `2026-11-04T17:28:54.830834Z` lists `gpt-6.1-sol` and `gpt-6-luna` with visibility `list` and `supported_in_api=true`. These are verified catalog entries, **not runtime-verified worker models**. |
| Actual worker provider/model IDs | No deployed workers; IDs are unassigned. Proposed fallback: worker-a `codex` / `gpt-6.1-sol`, worker-b `codex` / `gpt-6-luna`. |
| Actual worker machines | No assignments. Intended fallback: all four agents on This computer. |
| Ledger response evidence | **None**: no worker task was posted because no quant-desk deployment completed. |

### Terminal OpenCode verification — 4 Nov 2026

The terminal binary is `~/.opencode/bin/opencode`, version `2.2.5`; its background service answered `/api/info`. Credential values were not read, printed, or stored. `opencode auth list` showed stored OpenAI and OpenCode Console integrations.

| Check | Exact observed result |
| --- | --- |
| Configured default model | Provider `opencode`; model `crouton-alpha-free` (`opencode/crouton-alpha-free`) |
| Default small prompt | Failed before an answer: `provider.free-limit`, HTTP `429`, “Free usage limit reached.” |
| Explicit small prompt | `opencode run --model openai/gpt-5.6-terra --format json 'Reply with exactly: P1-terminal-ok'` returned `P1-terminal-ok` |
| Explicit route | Provider `openai`; model `gpt-5.6-terra` (`openai/gpt-5.6-terra`) |
| Evidence | Session `ses_e583b95e1ffeB4a10iaO0ngffX`; response text `P1-terminal-ok` |

The successful explicit route is OpenAI, not Gemini. It therefore cannot justify describing a Codex/OpenCode deployment as cross-vendor unless deployed worker routing later proves different model vendors. The primary template is still unmodified and has not been deployed; all four “This computer” assignments, the room/thread/message IDs, and both ledger acceptance checks remain **VERIFY**.

The terminal harness has no interactive Switch Console/browser-control capability. Consequently it could not invoke the documented Console template flow or obtain a new Switch integration error. The only exact current failure is the terminal default-route quota error above; the earlier Console import/UI failures remain recorded below. Do not substitute a terminal response for a deployed worker ledger.

The automation blocker is specific: selecting the fallback YAML in Console's file picker left **Open disabled**; double-click and keyboard selection did not open it. Pasting and setting the import editor did not persist content, leaving Import disabled. Resetting the computer-control session did not resolve this. Browser access returned **The browser access host is unavailable**. A later native observation returned `cgWindowNotFound`. Direct local HTTP checks were inconclusive: one health check returned ok, subsequent attempts failed to connect or returned Operation not permitted. No authentication was bypassed and no server data was reset.

### Exact user action to unblock deployment

In Switch Console, select the local server → Templates → Import template, open `templates/quant-desk-fallback.template.yaml`, and save privately as **Quant desk fallback**. If the file picker cannot open it, paste its contents manually into the import editor. Select Use template, Mattermost, and the two distinct Codex model IDs above **if the provider offers them**. Confirm all four previews select **This computer**, then Create all. If it fails, retain the sanitized error and do not delete existing agents automatically. Tell Codex when the room is created so it can perform the two ledger checks. Import and preview alone do not pass P1.

To restore the primary path instead, configure Google authentication in OpenCode on this computer using its documented `/connect` flow, select an offered Gemini model using `/models`, check the account's quota in its Google console, and Recheck in Switch Console. Do not paste keys into this chat. Resolve worker-b's machine before creating the primary room. [OpenCode provider documentation](https://opencode.ai/docs/providers/)

### Identical worker fixture (P1 smoke test only)

Post this twice, replacing `WORKER` with `worker-a` and then `worker-b`:

```text
@WORKER P1 smoke test S1. Return an actual small JSON trade ledger in this thread, not an acknowledgement. Use only this synthetic fixture, in this order:
1. id=1, symbol=ABC, side=buy, qty=100, price=100
2. id=2, symbol=XYZ, side=sell, qty=50, price=200
No market data lookup, files, or executed backtest is needed. Return a JSON object with id, task_id="P1-S1-smoke", agent, provider, model, strategy="S1", trades, and traded_value (sum of qty*price across both trades). Include only metadata you know; state any unknown model metadata rather than guessing. Preserve the two supplied trades. Briefly state any assumptions after the JSON. Do not grade your output.
```

Acceptance: both workers post JSON objects with those two trade rows and `traded_value=20000` in quant-desk. Record each room/thread/message ID and verify its configured model on the agent/session page; self-reported model names alone do not verify routing. Save evidence separately from evaluation fixtures. P1 remains blocked until both responses exist.

### Rules, Decisions, History, and revocation: verified boundaries

- **Room guidance access — documented and confirmed in installed source, not live-tested here.** Configuration → Instructions is the native shared guidance field. `connect_to_room` composes it into the joining agent's instructions. `get_room_detail` returns the field to a room member; `load_internal_documents` loads room document content. This does not establish a separate Rules collection. [Shared context documentation](https://docs.switchagents.ai/switch-rooms/using/shared-context)
- **History — source verified, live VERIFY.** `read_context` reads the stored conversation grouped into threads, with membership checks and pagination. No deployed quant-desk trace exists yet.
- **Human approval — source verified, live VERIFY.** Session approval requests have offered options; humans answer a rendered control or the card's explicit text form. The installed service records the answer, answerer, and timestamp and checks permission to address the agent. A session/tool approval is not evidence of a first-class business Decision record or automatic activation of a Second Strike rule.
- **Rules/Decisions lifecycle — unsupported claim removed.** No dedicated rule record or business Decision lifecycle was found in the inspected installed core schema, operations, or public room/resource documentation. Room roles are instruction bundles; the installed source explicitly describes deterministic room rules as future work. P3 must resolve the gap using documented primitives and label any custom records/activation logic honestly; do not invent endpoints or call it native one-tap rule approval.
- **Revocation — custom implementation required for the specified `!revoke R1` command on this installed command surface.** The full installed native command registry contains no `revoke`. Public command documentation also does not list it. No revoke handler was implemented or tested in P1. [Room commands](https://docs.switchagents.ai/switch-rooms/resources/room-commands)

Installed source evidence, relative to `/Applications/Switch Console.app/Contents/Resources/local-server/switch/src/core/switch_core/`:

| Source | Evidence |
| --- | --- |
| `bridges/agent/protocol/instructions.py:17` | `build_room_instructions` appends the room-specific instructions. |
| `bridges/agent/operations/definitions.py:640` and `:2368` | `read_context` and `get_room_detail` contracts. |
| `session_activity/service.py:452` | `answer_approval` records an authorized person's response. |
| `bridges/collaboration/session/text.py:1` | Accepted text-answer grammar for approval cards. |
| `bridges/agent/commands.py:1851` | Full native command registry; no revoke entry. SHA256 `1d7bb75e6a8113fe08c182163cb885a7be9bab11472ff54775e3ef7f71795707`. |
| `db/models.py:1956` | RoomRole is an instruction bundle; deterministic room rules described as future work. |

No P2–P7 work, live approval, rule activation, revocation, evaluation, commit, or publication was performed in this continuation.


### 5 Nov Console attempt

The primary deployment preview accepted worker-a `codex/gpt-6.1-sol` and worker-b `opencode` model `openai/gpt-5.6-terra`, with Mattermost selected. Creation was disabled with: “None of your machines on this server can run worker-b now. opencode on [local machine] is not ready: login could not be checked.” A Console recheck was requested; the provider list still reports sign-in could not be checked. These are preview inputs, not deployed model assignments. The repository primary template now defaults worker-b to `openai/gpt-5.6-terra`; the previously imported Console template was not synchronized. No room or ledger response was observed. Terminal OpenCode previously succeeded on that explicit route; the Console readiness failure is separate. This intended configuration is Codex and OpenCode backed by OpenAI; cross-vendor operation remains unverified.


## P1 passed and P2 checker — 5 Nov 2026

The user imported Quant desk fallback; Codex selected models and created all four agents in the private quant-desk Mattermost channel. Both workers answered the identical README smoke fixture. The human supplied screenshots of each ledger. worker-b's unformatted `:[` sequence rendered as an emoji; the accessibility tree preserves those source characters. Require fenced JSON in later tasks.

- worker-a task/thread: `ztgdctchxfrcuc14koi4jhyzpe`. Both trades preserved, traded_value 20000; saved agent settings show gpt-6.1-sol.
- worker-b task/thread: `79r4jponytf9j8t1iwd7udjcqy`; ledger message `w934fmzs17g7jeow9f8n8h35xo`. Both trades preserved, traded_value 20000; saved agent settings show gpt-6-luna.
- Both use Codex on This computer. Saved model settings were observed; request-level provider routing was not independently traced.
- No fees or learning were tested in P1. Smoke results are separate from the evaluation.

Run the offline fee checker from the project root:

```sh
python3 -m unittest discover -s tests
python3 checkers/check_fees.py eval/ledgers/ex_pass_fees.json
python3 checkers/check_fees.py eval/ledgers/ex_fail_fees.json
```

Exit codes are 0 pass, 1 fee-rule failure, 2 invalid input requiring human review. JSON objects with trades and CSV trade rows are supported. Fees must equal qty*price*0.0005 within 0.01. The checker validates per-trade fee fields only; it does not establish that fees were deducted from net returns. No model or live gate evaluation results exist. Ten synthetic valid ledgers and five prewritten task variants are checker/task fixtures, not independently sourced review comments or proof of held-out model performance. Tasks are visible to implementers; freeze them before model runs and do not tune them from results.

Next: give gate read-only access to this project, verify it runs the actual checker and posts the result in the room, then implement the custom human-approved rule lifecycle using verified Switch Instructions/documents. Dedicated native business Rules/Decisions and native !revoke remain unestablished.


### P2 live gate verification — 5 Nov 2026

Gate ran python3 -B checkers/check_fees.py against both example files and posted actual stdout in quant-desk. Passing example returned exit 0/pass; missing-fee example returned exit 1/fail with expected_fee 5.0000. Task/thread: 64mgytbhtp81xbgcnif1jj48ar. Result: 619z5rp9figa7xm3we4faw5s6h. Codex used the Console approval buttons for these two narrowly scoped, user-authorized read-only tool runs; these are tool permissions, not human business-rule approvals. R1 is now active as a custom Second Strike record and in the room Instructions; it is not a native Switch Rule or Decision. Four unit tests and ten valid synthetic fixtures pass locally, plus a CSV CLI smoke test. Scribe drafted R1 and Soham approved it in room chat.
