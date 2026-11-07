# Second Strike: Implementation Plan and Tracker

Owner: Soham. Draft v1, 4 Nov 2026 (IST). Hard deadline: 7 Nov 11:59 PM IST; aim to submit by 6 PM that day. The plan is written for a one-day build, with the remaining days as buffer for the video, README and submission. Rule: one finished project beats two half-finished ones.

Status key: \[ \] not started, \[\~\] in progress, \[x\] done, \[!\] blocked or cut. Update this doc as you go; record real outcomes, not intentions.

## 1. Phase 0: Setup and verification (first hour)

- [x] Open Switch Console; confirm Codex and OpenCode both appear as providers.
- [ ] Test OpenCode on a Gemini key; note the quota. Result: works / does not work.
- [ ] Decision: cross-vendor (Codex + OpenCode) or fallback (two Codex models, labelled "same vendor, different models").
- [ ] Post in the WeMakeDevs Discord: can one project be submitted to both Track 1 and Track 2?
- [ ] Edit `second-strike-prompts.txt` P1 (worker-a `provider codex`, worker-b `provider opencode`, fallback second `codex`, remove Claude Code mentions).
- [ ] Optional: install Wispr Flow via the hackathon link; dictate as you build and screenshot Insights for the $500 side track.

## 2. Phase 1: Room and agents (1-2 h) \[Prompt P1\]

- [x] `templates/quant-desk.template.yaml` created, modelled on the Switch example template.
- [x] Room created with worker-a, worker-b, scribe, gate and the human (5 Nov, fallback).
- [x] Both workers returned the identical two-trade fixture with traded_value=20000.
- [x] Record exactly what works and what fails. Do not invent Switch APIs. See latest section 16; P1 passed.

## 3. Phase 2: Seeded tasks and deterministic gate (2 h) \[P2\]

- [x] `checkers/check_fees.py` with unit tests and pass/fail examples.
- [x] Five seeded task prompts and ten valid ledgers frozen by SHA-256 before paired worker runs (`eval/frozen_hashes.txt`).
- [x] Gate ran both example checkers and posted actual stdout/exit codes in quant-desk (5 Nov).

## 3b. Phase 3: Rule creation and handoff (2 h) \[P3\]

- [ ] Reject, scribe draft, activation test, one-tap approval logged as a Decision.
- [ ] Rule shows in the room's Rules.
- [ ] Worker-b applies the rule on a new task without being told in the prompt.
- [ ] Hits, last-fired and expiry recorded.

## 4. Phase 4: Paired first-submission test (2 h) \[P4, protect this\]

- [x] Harness freezes (hashes) both ledgers before either reaches the checker.
- [ ] Classification: worker-learned / gate-rescued / correct-without-rule. T-V1 has two observed replies, but no admissible matched pair.
- [x] Results saved to `eval/results.md` as raw counts with n; T-V1 treatment and control attempts are recorded, but the pair is invalid.
- [x] Valid-ledger false-block replay completed: 0 of 10; all ten frozen valid ledgers passed the checker again.
- [!] Matched run blocked: saved control reply reports OpenAI / GPT-6 rather than the runbook's Codex gpt-6-luna; Switch identifies the control room as public. Its fee-checker replay exits 2 on invalid trade schema. Treatment passed; no learning comparison claimed. See `eval/results.md` and `eval/live_hashes.txt`.

## 5. Phase 5: Revoke, override, escalate (only if time) \[P5\]

- [ ] `!revoke R1` logged as a Decision.
- [ ] Replay of the exact blocked submission passes after revoke.
- [ ] Second rule R2 (lookahead) still blocks.
- [ ] Override flags a rule; NL ambiguity escalates to the human.
- [ ] Rule ablation (optional).

## 6. Phase 6: Video, README, submission (2 h) \[P7\]

- [ ] 60s demo video in the order of the App Flow doc; no secrets on screen.
- [ ] `README.md`: how Switch is used, how to reproduce from clone, what agents wrote and what you verified, known limits.
- [ ] `DEMO.md` with the script.
- [ ] README claims match `eval/results.md` exactly.
- [ ] Confirm what the submission form needs (repo, README, demo video, anything else).
- [ ] Submit by 6 PM on 7 Nov (deadline 11:59 PM IST).

## 7. Optional add-ons (cheap)

- [ ] \#HowISwitch post (top 5 win Logitech keyboards).
- [ ] Best Blog from build notes (AirPods 5), only if time remains.
- [ ] Star the Switch repo (Keychron keyboard draw).
- [ ] Track 2 Life Room: one extra template only, and only if Track 1 is finished and Discord confirms dual entry.

## 8. Cut order if late

1. Public review comments / artifact B
2. Rule ablation
3. Revoke-and-recover ending
4. Life Room (Track 2)

Never cut: the paired first-submission test, the deterministic gate, the README and the demo video.

## 9. Tracker: decisions and blockers

| Item | Status | Notes |
| --- | --- | --- |
| OpenCode + Gemini works in Console | \[ \] | Test in Phase 0 |
| One project may enter both tracks | \[ \] | Ask in Discord |
| Submission form requirements | \[ \] | Check hackathon page |
| Goose Track 3 branch (`feat/goose-provider`) | \[!\] parked | Local only; not pushed; issue #780 assignment never confirmed |
| Real eval results | \[ \] | None exist yet |

## 10. Prompt map

| Prompt | Covers | Phase |  |
| --- | --- | --- | --- |
| P1 | Room + agents | 1 |  |
| P2 | Seeded tasks + deterministic gate | 2 |  |
| P3 | Rule lifecycle | 3 |  |
| P4 | Paired first-submission test | 4 |  |
| P5 | Eval, false blocks, ablation, R2, revoke replay | 4-5 |  |
| P6 | Life Room skin | optional |  |
| P7 | README + DEMO.md | 6 |  |

## 11. Daily checkpoints

- **End of 4 Nov:** Phase 0 and 1 done; Phase 2 started.
- **End of 5 Nov:** Phases 2-4 done, with real results saved.
- **End of 6 Nov:** video and README drafted; optional phases attempted.
- **7 Nov by 6 PM:** submitted.


## 12. P1 implementation evidence — 4 Nov 2026

- [x] All six source documents relocated into `docs/`; source text preserved except this tracker update.
- [x] Primary and fallback templates created with required worker model inputs and separate working directories.
- [x] Section 8 skeleton created; purpose-only placeholders do not implement later phases.
- [x] README contains setup, recovery, file purposes, and honest P1 limits.
- [x] Local PyYAML parsing and structural assertions passed for both templates; no dependency added.
- [x] Primary template imported privately as “Quant desk”; Console shows all four agents and quant-desk in preview.
- [x] Local server started via Console; switch-core 0.31.0 Running, Console 0.40.1. Existing goose-dev selection was Unreachable; no server reset or deletion performed.
- [~] P1 room creation blocked on deployment prerequisites; no worker ledger responses observed.

| Observation | Status | Evidence / next action |
| --- | --- | --- |
| Codex provider | works | CLI 0.166.0; Console says Installed / Signed in. |
| OpenCode provider | VERIFY | Console says Installed / Sign-in not verified; verify Gemini backend and quota. |
| Terminal OpenCode check | fails in sandbox | CLI cannot open its log file outside writable roots; this does not prove the backend is broken. |
| Terminal Docker check | fails in sandbox | Permission denied accessing Docker socket; Console server nevertheless started successfully. |
| Mattermost | VERIFY | Existing Run Mattermost toggle on; setup was pending when server became usable. Template form offers Mattermost @user; live chat readiness unverified. |
| Worker-b machine | VERIFY | Primary deployment preview says Machine Not set by the template despite local location default. Resolve in Console using documented machine/location controls before creation. |
| Worker model IDs | VERIFY | Required inputs intentionally have no invented defaults. Use actual provider-supported IDs. |
| Both worker replies and room membership | VERIFY | Not deployed; no live room/thread evidence. |
| Fallback deployment | VERIFY | File parses; not imported or deployed. Select distinct supported Codex models; same vendor, different models. |
| Switch sources | read | Official triage-pair example and docs/TEMPLATES.md on main, via web. VERIFY immutable commit revision; terminal fetch hit DNS restriction. |
| Native Rules / Decisions / History / revoke | VERIFY | P3 integration unimplemented; no API claims. |
| Human review | VERIFY | Soham must read and understand generated files before submission. |

P4 handoff agreed during planning: record independent outcome flags and unresolved pairs; keep live evidence separate from saved-ledger replay. Apply schema changes in P4, not P1. Do not force a smoke-test worker to omit fees or reuse smoke-test results as unseen evidence.

P2–P7 remain unimplemented. No Discord outreach, evaluation counts, video, publishing, or submission performed.


## 13. P1 continuation — 4 Nov 2026; BLOCKED, not passed

README's “P1 continuation” section is the detailed evidence and recovery procedure. Earlier section 12 describes the initial session, not completion.

- [x] Re-read README and six project documents; confined changes to P1 evidence and setup instructions.
- [x] Console 0.40.1, local switch-core 0.31.0; Console reports Running. Local server URL in actual Console database: http://localhost:50139.
- [x] Codex 0.166.0: Installed / Signed in. Model catalog lists distinct `gpt-6.1-sol` and `gpt-6-luna`; cache timestamp 2026-11-04T17:28:54.830834Z. Runtime support is VERIFY.
- [x] OpenCode 2.2.5: Installed / Sign-in could not be checked. Auth-store provider names inspected without exposing values: only `opencode`, no Google entry. Global config only schema; shell Gemini/Google API keys absent.
- [!] Primary cannot be completed with the verified setup: Google authentication, Gemini model, and quota unverified; worker-b preview has no machine assignment. No conclusion about a key stored elsewhere.
- [~] Recovery path: existing fallback, same vendor, different models. Import attempted; not completed, no deployment claimed.
- [!] Automation blocked: selected fallback YAML left Open disabled; editor paste/set did not persist; computer-control reset did not fix it. Browser host unavailable; later native state returned cgWindowNotFound. Direct HTTP not reliable/permitted from this tool environment.
- [ ] Room created with both workers, scribe, gate, reviewer. No actual worker machines or models assigned.
- [ ] Both ledger responses. None observed; identical two-trade fixture and acceptance checks now in README. No invented ledgers or message references.
- [x] Checked installed source and official docs: shared Instructions/document access and paginated History supported; no separate Rules collection or business Decisions lifecycle established. Session approvals record answer/answerer/time, but are not proof of human-approved rule activation. Live behavior VERIFY.
- [x] Installed native command registry has no `revoke`; specified !revoke R1 needs custom implementation. No handler implemented in P1.

**Required user action:** manually import `templates/quant-desk-fallback.template.yaml` privately as Quant desk fallback, select offered distinct Codex model IDs (candidates above), assign all four agents to This computer, choose Mattermost, and Create all. Report any sanitized failure or tell Codex when quant-desk is created. Then Codex must send the same README fixture to both workers, retain actual ledger messages and routing evidence, and only then mark P1 passed. Do not delete preexisting agent-name collisions automatically.

**Primary alternative:** configure Google in OpenCode using documented /connect, verify an offered Gemini model using /models and Google account quota, then Recheck in Console and assign worker-b to an eligible machine. Never share keys in chat or logs.

Remaining VERIFY: live Mattermost readiness; deployed worker model IDs and machine identities; both response message/thread IDs; live Instructions/document read; human approval rendering and outcome; business Decision mapping; immutable upstream Switch revision; Soham's personal review. P2–P7 remain untouched.

## 14. P1 terminal recheck — 4 Nov 2026; BLOCKED, not passed

- [x] Terminal OpenCode binary and service verified: OpenCode `2.2.5`; `/api/info` responded. Credentials were not exported, printed, or written into this repository.
- [x] Actual configured default identified as provider `opencode`, model `crouton-alpha-free` (`opencode/crouton-alpha-free`). A minimal prompt failed with sanitized `provider.free-limit`, HTTP `429`, “Free usage limit reached.”
- [x] Explicit OpenAI route verified: `openai/gpt-5.6-terra` returned exactly `P1-terminal-ok` for the minimal prompt. Evidence: OpenCode session `ses_e583b95e1ffeB4a10iaO0ngffX`.
- [ ] OpenCode + Gemini works in Console. Not verified: the only successful terminal route was OpenAI, not Gemini.
- [ ] Cross-vendor decision. Not established: do not label a future Codex/OpenCode room cross-vendor unless the deployed worker routes prove different model vendors.
- [!] Primary template deployment not attempted in this terminal harness: there is no interactive Switch Console/browser-control channel. Thus no new Switch integration error exists, no agents were assigned to This computer, and no room was created or reused.
- [ ] Both worker ledger responses. The prepared two-trade fixture was not sent because a deployed room does not exist. No room/thread/message IDs or routing evidence exist.

**Current P1 result:** blocked. Terminal OpenCode is usable only when explicitly selecting the verified OpenAI model above; its default OpenCode route is quota-limited. This is insufficient for the README primary Gemini path and does not pass P1. Resume in Switch Console: use the primary template only after selecting verified model IDs, assign **all four agents** (including worker-b) to **This computer**, create the private room, send the README fixture separately to both workers, and record their actual JSON responses plus agent/session routing. If Switch fails, add its exact sanitized error here; do not infer it from the terminal quota response.


## 15. P1 Console recheck — 5 Nov; BLOCKED

- Existing rooms: Off-Topic and Town Square; existing managed agent: switch-buddy-admin. No quant-desk observed.
- Primary preview: worker-a Codex `gpt-6.1-sol`, worker-b OpenCode `openai/gpt-5.6-terra`, Mattermost selected. No agents deployed.
- Create all disabled: “None of your machines on this server can run worker-b now. opencode on [local machine] is not ready: login could not be checked.” Recheck requested; provider list still reports sign-in could not be checked.
- Repository primary template now defaults worker-b to `openai/gpt-5.6-terra`; imported Console copy remains unsynchronized.
- Neither ledger exists; model assignments and runtime verification remain pending. P1 not passed.


## 16. P1 passed; P2 in progress — 5 Nov 2026

- [x] User imported fallback; Codex deployed private Mattermost quant-desk with all four agents on This computer.
- [x] Saved worker models verified in Console settings: worker-a gpt-6.1-sol, worker-b gpt-6-luna. Same vendor, different models.
- [x] Both ledgers preserve the fixture trades and total 20000. Task IDs and worker-b reply reference are in README. Human screenshots and live accessibility text provide evidence.
- [x] Offline JSON/CSV fee checker, validation, unit tests, passing/failing examples and ten valid synthetic ledgers implemented.
- [~] Five task variants authored before model runs; no live or held-out results claimed.
- [ ] Gate execution inside the room, shared repository access, rule activation/expiry/revocation and paired harness remain pending.

Historical BLOCKED entries above describe earlier attempts and are superseded for P1 deployment only. Request-level model routing was not independently traced.


## 17. P2 live checker verified; P3 active custom rule

- [x] Gate ran both checker examples in the project directory and posted pass/exit 0 and fail/exit 1 in thread 64mgytbhtp81xbgcnif1jj48ar, result 619z5rp9figa7xm3we4faw5s6h.
- [x] Four unit tests, ten valid synthetic fixtures, and CSV CLI smoke check pass locally.
- [~] Five prewritten variants exist; no model/evaluation runs claimed.
- [x] Soham approved R1 in Mattermost message `dx95znbbq7dtixxhouksnsomnh`. `rules/R1.json` is the active custom record; it is not a native Switch Rule or Decision.
- [x] R1 was added to quant-desk room Instructions. The repository record expires `2026-11-30T00:00:00+05:30`; Soham must manually make the same expiry edit in room Instructions. It begins at zero hits and is revocable through the custom lifecycle.
- [x] `harness/paired_test.py` freezes each supplied first-submission JSON by SHA-256 and reports the deterministic R1 verdict. It has a unit test; it does not run agents or create benchmark results.
- [ ] Fresh-worker propagation and paired first-submission experiment remain pending.

Codex approved the two read-only gate command permission cards under the user-authorized test scope. They must not be presented as human approval of a business rule.

## 18. 7 Nov 2026 — documentation consolidation and gate

- [x] Reviewed `checkers/gate.py` (already present in the repo; not written in this pass). It loads `rules/R1.json`, applies expiry and revoke (`not_enforced`, exit 3), counts hits and `last_fired` on fail, and appends each check, skip and revoke to `rules/events.jsonl`. Exit codes: 0 pass, 1 fail, 2 escalate, 3 not enforced.
- [x] Reviewed `tests/test_gate.py` (3 tests, already present). `python3 -m unittest discover -s tests` runs 8 tests in total. Passed on a fresh copy of the repo.
- [x] README rewritten. The previous README is kept at `docs/README-history.md`.
- [x] `DEMO.md` replaced with a 90-second shot list.
- [x] Status boxes added to the PRD, Tech Spec, App Flow, and Data Schema. Items not built were moved to a Future work section in each. Original wording is kept there.
- [!] `gate.py` writes to `rules/` (hits, `last_fired`, `events.jsonl`). The README and demo run it on a copy. The repo's `rules/R1.json` was not modified in this session.
- [ ] Clean run (Codex experiment, `eval/clean/`) not recorded. README has the `<<CLEAN_RUN_TABLE>>` placeholder.
- [ ] Room Instructions expiry edit to 2026-11-30 still manual. Not verified in the room.
- [ ] Submission form, dual-track eligibility, and video not done.

## 19. 7 Nov 2026, 18:11 IST — Phase A of `docs/PLAN-9plus.md` (second-strike loop harness)

- [x] `checkers/gate.py` refactored into importable `run()` and `revoke()`. CLI output and exit codes 0/1/2/3 unchanged; `tests/test_gate.py` passes unedited.
- [x] `harness/gate_reply.py`: saves the reply byte-exact to `eval/<run>/raw/<Vn>-a<K>.txt` and hashes it before grading; extracts a fenced or bare JSON object; runs the gate; prints verdict JSON and worker feedback; appends to `eval/<run>/log.jsonl`. Refuses to overwrite a recorded attempt (exit 4).
- [x] Gate agent command: `python3 harness/gate_reply.py --rule rules/R1.json --run rescue --variant Vn --attempt K MESSAGE_FILE` from the repo root.
- [x] Feedback: fail → table of offending trades with expected fee; escalate → the checker's first error plus the full per-trade schema; always ends with the R1 `what` text. Nothing else.
- [x] `harness/rescue_report.py`: per-variant attempt 1 / attempt 2 table and first-try vs second-strike totals.
- [x] `tests/test_gate_reply.py` (7 tests). Full suite 15/15 on a fresh copy. Dry run in scratch only.
- [x] `eval/rescue/R1.before.json` snapshot taken (hits 0, sha256 `72ecb19f…3dd3`).
- [ ] Phase B–D (Switch gate agent, rescue run, raw export) — owned by Claude (chat). No rescue results exist yet.
- [ ] Phase E README/DEMO results — waits for `eval/rescue/log.jsonl`.

## 20. 7 Nov 2026 — Phase E: second-strike results in README/DEMO

- [x] Rescue run recorded by Claude (chat) in `eval/rescue/`: first-try pass 0/5, pass by second strike 5/5 (`report.md`).
- [x] Re-checked in the repo: 10/10 raw hashes match `log.jsonl`, `check_fees.py` replays every verdict, the report regenerates identically, and `R1.after.json` matches the before snapshot (hits 0; escalations are not fee hits).
- [x] README headline, loop steps, diagram, rescue results, and the caveats from `eval/rescue/results.md` added. Added a no-comparison-arm caveat.
- [x] DEMO: terminal gate shot replaced with the live rescue-room loop; CLI revoke shot kept; now 105 s.
- [ ] Mattermost API export (clean and rescue) still pending.
