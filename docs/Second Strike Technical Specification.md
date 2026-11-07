# Second Strike: Technical Specification

Owner: Soham. Draft v1, 4 Nov 2026. Companion to the PRD. Rule for every section: do not invent Switch APIs. Anything marked VERIFY must be confirmed against the Switch docs and the Console in the first hour, and the result recorded in the tracker.

> **Status, 7 Nov 2026.** This is the original design. Current claims are in `README.md`.
> - **Implemented:** `checkers/check_fees.py`; `checkers/gate.py` (R1 lifecycle: expiry, revoke, hits, append-only `rules/events.jsonl`); `harness/paired_test.py` (hashes and verdicts only); 8 unit tests; room `quant-desk` deployed as the fallback template: worker-a Codex gpt-6.1-sol, worker-b Codex gpt-6-luna (same vendor, different models).
> - **Partial:** §5 gate runs locally on saved ledgers; it is not connected to the room. §6 paired test: no admissible matched pairs yet.
> - **Not implemented:** §2 native Rules and Decisions, and `!revoke` as a room command (VERIFY items unresolved). §3 activation test. §4 `check_lookahead.py` and natural-language rules. `harness/eval.py`. §7 ablation. Cross-vendor worker-b. These are in §12 Future work.

## 1. Architecture overview

One Switch room (`quant-desk`) created from a YAML template. Agents join like teammates; the human reviewer works in the room chat. Switch holds the shared History, Rules, Tasks and Decisions. A small local Python package holds the deterministic checkers, the paired-test harness and the eval runner. Everything is reproducible from a clone.

| Component | Role | Implementation |
| --- | --- | --- |
| Switch Console + Mattermost | Room, chat, Rules, Decisions, Tasks | Desktop app, Docker; ships with Switch |
| worker-a | Produces backtest ledgers | Codex provider |
| worker-b | Same task, different vendor | OpenCode provider on a Gemini key (VERIFY). Fallback: second Codex on a different model |
| scribe | Drafts a rule from a rejection | Codex |
| gate | Checks submissions against active rules | Deterministic scripts first; OpenCode agent only for natural-language rules |
| Checkers | `check_fees.py`, `check_lookahead.py` | Plain Python, no network |
| Harness | Paired first-submission test, eval, ablation | Python CLI |

## 2. Switch integration (VERIFY items)

- Template: `templates/quant-desk.template.yaml`, modelled on `examples/agent-templates/triage-pair.template.yaml` in the Switch repo. Read the docs before writing it.
- Agent protocol: server-sent events in, HTTP out. Use whatever the provider adapters already do; do not hand-roll the protocol unless an adapter is missing.
- VERIFY: how rules are written to and read from a room's Rules, how a one-tap approval is created and logged as a Decision, and whether agents can read Rules natively or need them injected into the prompt. If Rules are not agent-readable, the harness injects the active-rule text into each agent's task prompt and the README says so.
- VERIFY: whether `!revoke R1` is a custom chat command we implement in the scribe/gate or a native action.

## 3. Rule model

A rule has: id, title, what, why, scope, expiry, passing example, failing example, checker (script path or `nl`), status, hits, last fired, created by, approved by (Decision id), revoked by.

Statuses: `draft`, `active`, `revoked`, `expired`, `flagged`.

**Activation test:** on approval the harness runs the checker against the rule's passing and failing examples. If the passing example does not pass or the failing example does not fail, activation is refused and the scribe is asked to fix the rule. This means approving a rule is approving a tested behaviour, not just a sentence.

## 4. Checkers

**`check_fees.py` (R1, fee rule).** Input: ledger CSV or JSON with per-trade fields `symbol, side, qty, price, fee`. Rule: every trade must include a cost of 5 bps of notional (`qty * price * 0.0005`), tolerance for rounding of 0.01. Output: pass/fail, list of offending trade ids, expected vs found fee. Example: $100,000 traded value, expected fee $50.

**`check_lookahead.py` (R2) and natural-language rules:** moved to §12 Future work (7 Nov 2026).

## 5. Gate behaviour

*Implemented for R1 only, as a local script (`checkers/gate.py`). Room connection, override flagging and escalation are not implemented.*

1. Worker posts a ledger to the room.
2. Gate loads all `active` rules in scope and not expired.
3. Runs each checker; collects verdicts.
4. All pass: the human sees the submission. Any fail: the submission is returned to the worker with the failing rule id and the checker output. Any escalate: the human decides.
5. Increment `hits` and set `last fired` on each rule that fired.
6. Human override of a block flags the rule as `flagged` for review.

The worker never grades itself. Gate model family must differ from the worker it is checking where the stack allows it.

## 6. Paired first-submission test (centerpiece)

Two fresh agents get the same unseen task. Agent P has the rule available; agent N does not. Each ledger is frozen (hashed and saved) before the gate runs. Each pair is classified:

- `worker-learned`: P correct, N incorrect, before the gate.
- `gate-rescued`: P incorrect before the gate, correct after the gate's return.
- `correct-without-rule`: N already correct.

Results are written to `eval/results.md` as raw counts with n. Never tune the tasks after seeing results.

## 7. Eval set

- 5 unseen variants of the fee flaw (different strategy, universe, size).
- 10 valid ledgers that include the 5 bps cost, to measure false blocks.
- Optional: rule ablation (disable each rule, check whether the mistake recurs).

## 8. Repository layout

```
second-strike/
  README.md
  DEMO.md
  templates/quant-desk.template.yaml
  templates/life-room.template.yaml     (P2, optional)
  checkers/check_fees.py
  checkers/gate.py                      (added 7 Nov 2026)
  checkers/check_lookahead.py           (placeholder)
  harness/paired_test.py
  harness/eval.py                       (placeholder)
  tasks/seeded/                         (task prompts)
  eval/ledgers/                         (valid + flawed)
  eval/results.md
  rules/                                (rule records, JSON; events.jsonl)
  tests/                                (unit tests)
```

## 9. Environment and secrets

Switch Console (macOS), Docker, Codex, OpenCode, Python 3.11+. Provider keys live in environment variables or the Console's own settings, never in the repo and never on screen in the demo video. Check Gemini quota before any run.

## 10. Testing

- Unit tests for each checker with at least one passing and one failing fixture.
- Activation test runs automatically on rule approval.
- Harness has a dry-run mode that uses saved ledgers so the demo can be re-run without spending model quota.

## 11. Known limits (go in the README)

- Small n. Counts are illustrative, not statistically strong.
- Fee and lookahead checks are deterministic; natural-language rules are less reliable and escalate when unsure.
- If worker-b is a second Codex model, the README says "same vendor, different models", not "cross-vendor".

## 12. Future work

Moved here on 7 Nov 2026. Original wording kept.

- **`check_lookahead.py` (R2).** "Input: signal timestamps and the price timestamps used to compute them. Fail if any signal at time t uses data stamped after t." Placeholder only.
- **Natural-language rules.** "The gate agent evaluates the rule text against the submission and must return one of `pass`, `fail` or `escalate`. On `escalate` the submission goes to the human; it is never auto-blocked or auto-passed. Use these only when no deterministic checker exists."
- **Native Switch Rules and Decisions** (§2 VERIFY items), one-tap approval logged as a Decision, and `!revoke` as a room command. Not established.
- **Activation test** (§3, §10): automatic refusal of activation.
- **Room-connected gate and override flagging** (§5 items 4 to 6).
- **Eval runner** `harness/eval.py`, and rule ablation (§7).
- **Life Room** template (PRD R12; App Flow §6; `templates/life-room.template.yaml` is a placeholder).
- **Cross-vendor worker-b** (§1 table). Not verified.
