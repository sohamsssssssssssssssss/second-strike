# Second Strike: Product Requirements Document

Owner: Soham. Status: draft v1, 4 Nov 2026 (IST). Event: Flip the Switch (WeMakeDevs). Deadline: 7 Nov 2026, 11:59 PM IST (aim to submit by 6 PM). Entry: Track 1 (primary), Track 2 (thin skin, only if Track 1 is done).

> **Status, 7 Nov 2026.** This is the original plan. Current claims are in `README.md`.
> - **Implemented:** R1 fee rule (`checkers/check_fees.py`). Gate with R1 lifecycle (`checkers/gate.py`: expiry, revoke, hit counter, append-only events). Room `quant-desk` with R1 in room Instructions (same vendor, different models). `harness/paired_test.py` (hashes and verdicts only).
> - **Partial:** R7 paired test: four treatment passes, three control escalations, zero admissible matched pairs. R9 lifecycle: gate-only, no chat `!revoke`, no overrides. R10: 10 valid fixtures, 0 false blocks, no ablation.
> - **Not implemented:** R6 activation test (automatic refusal). Native Switch Decisions and Rules (R4). Cross-vendor workers. R11 and R12 are moved to §11 Future work.

## 1. Summary

One reviewer's correction binds every agent on the team, whatever vendor built it.

Second Strike is a workflow in a Switch room where a human reviewer rejects an agent's output, a scribe agent turns the rejection into a rule, the human approves it with one tap, and every other agent (including one from a different vendor) must follow it. A separate gate agent checks each submission against active rules before the human sees it.

## 2. Problem

Teams correct the same agent mistakes every week. The correction lives in a chat message, so the next agent (or the same agent tomorrow) repeats the error. Vendor memory (Cursor, CodeRabbit, rules files such as AGENTS.md) only helps one tool and has no shared approval or audit trail.

## 3. Users

- **Reviewer (human):** a quant research lead who rejects flawed backtests and approves rules.
- **Worker agents A and B:** produce backtest ledgers from a task prompt.
- **Scribe agent:** drafts a rule from a rejection.
- **Gate agent:** checks submissions against active rules; never the same agent that produced the work.
- **Track 2 users:** two friends planning a trip with agents (thin skin, same engine).

## 4. Goals and non-goals

**Goals**

- Show a correction approved once changing the first-submission behaviour of a fresh agent (same vendor, different models). Cross-vendor is moved to §11.
- Make Switch's role verifiable: shared Rules, Decisions and History across agents in one room.
- Report results honestly with raw counts and n.

**Non-goals**

- Claiming a novel learning mechanism (Bugbot, CodeRabbit learnings, Reflexion-style work exist).
- Claiming it is impossible without Switch.
- A general rules platform, UI polish, or auth/multi-tenant features.
- Claiming agents never repeat a mistake. We claim only what the eval shows.

## 5. Requirements

**P0 (must ship)**

- R1: Room with worker-a, worker-b, scribe, gate and a human reviewer, created from a Switch template.
- R2: Worker produces a backtest ledger from a seeded task; the seeded flaw is a missing 5 bps per-trade cost.
- R3: Reviewer rejection triggers the scribe to draft a rule: what, why, scope, expiry, passing example, failing example.
- R4: Human approval is recorded as a chat message reference. The rule text is placed in room Instructions and in `rules/R1.json` (custom record). Native Decisions and Rules are moved to §11.
- R5: Gate checks every submission against active rules with a deterministic script where possible (`check_fees.py`).
- R6: Rule activation runs the checker on the rule's own passing and failing examples and refuses activation if they do not behave as declared.
- R7: Paired first-submission test: two fresh agents, same task, one with the rule and one without; ledgers frozen before the gate runs; each outcome classified worker-learned, gate-rescued or correct-without-rule.
- R8: README and 60s demo video showing how Switch is used.

**P1 (if time)**

- R9: Rule lifecycle: hits, last-fired, scope, expiry, `!revoke R1`, override flag, escalate on ambiguity.
- R10: Eval: 5 unseen variants plus 10 valid ledgers, false blocks reported, rule ablation.
- R11: Moved to §11 Future work.

**P2 (cut first)**

- R12: Moved to §11 Future work.
- R13: Public review comments or artifact B as extra held-out cases.

## 6. Why Switch (honest claim)

A local rules file can store the text. Switch adds: agents from different vendors in one room reading the same Rules, one-tap approval logged as a Decision in the chat where the team already works, and a shared audit trail. The README states exactly this and nothing stronger.

## 7. Success metrics

Reported as raw counts with n, never bare percentages.

- Paired test: first-submission outcomes by class (worker-learned / gate-rescued / correct-without-rule).
- Unseen variants caught: x of 5.
- False blocks on valid ledgers: x of 10 (note that 0 of 10 still allows a true rate near 25-30%).
- Revoke replay: exact blocked submission passes after revoke; a different active rule still blocks.

## 8. Demo (60 seconds)

Mistake, reject, rule approved, fresh other-vendor agent applies it, paired ledgers ($100,000 traded value, expected fee $50), scoreboard, a rule wrongly blocks valid work, revoke in chat, replay the exact blocked submission and it passes, a different active rule still blocks.

## 9. Judging map

- **Use of Switch:** Rules, Decisions, History and multi-vendor agents in one room; README shows it.
- **Technical execution:** reproducible by clone; deterministic checks; eval results file.
- **Creativity and impact:** team-wide, human-approved, auditable corrections. Cross-vendor is future work (§11).
- **Presentation:** demo video plus README that shows Switch usage.

## 10. Risks and open questions

- OpenCode on a Gemini key may not work in the Console. Fallback: two Codex agents on different models, labelled "same vendor, different models", never "cross-vendor".
- Gemini free quota can break runs; check quota first.
- Whether one project may enter both Track 1 and Track 2 is not stated on the page. Ask in the WeMakeDevs Discord before submitting.
- The Switch setup and workflow must be built during the hackathon (4-7 Nov).
- Time: one day for a build plus video. Cut order: public review comments, rule ablation, revoke ending, Life Room.

## 11. Future work

Moved here on 7 Nov 2026. Original wording kept.

- Cross-vendor (from §4): "Show a correction approved once changing the first-submission behaviour of a fresh agent from another vendor." Not established: OpenCode/Gemini was not verified.
- Native Switch Decisions and Rules (from R4): "One-tap approval is logged as a Decision and the rule is written to room Rules." Not established.
- R11: "Second rule R2 (lookahead) and a revoke-and-replay ending (replay the exact blocked submission, then show a different active rule still blocks)." `check_lookahead.py` is a placeholder.
- R12: "Life Room skin for Track 2 (one extra template, rule 'never book red-eyes')." Template only.
