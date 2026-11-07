# Second Strike: App Flow

Owner: Soham. Draft v1, 4 Nov 2026. This is the end-to-end flow inside the Switch room, written so it can double as the demo script and the README walkthrough. Step labels (F1, F2, ...) are referenced in the tracker.

> **Status, 7 Nov 2026.** Original flow. Current claims are in `README.md`.
> - **Done (one-off or local):** F1 task. F2 worker ledger. F3 rejection. F4 scribe draft. F6 approval, recorded as a chat message reference, not a native Decision. F7 treatment runs with R1 in room Instructions (one run per variant; no controlled comparison). F8 gate run locally on saved ledgers, plus two checker examples posted once in the room.
> - **Partial:** F9 and F10. Paired files exist; zero admissible matched pairs.
> - **Not implemented:** F5 activation test. Native Switch Decision and Rules (F6). F11 to F14 (in-chat revoke and replay; the gate has a local `--revoke` only). Override and natural-language escalation (§4). Life Room (§6). These are in §8 Future work.

## 1. Actors

- **Reviewer** (human, Soham in the demo)
- **worker-a** (Codex), **worker-b** (OpenCode or second Codex model)
- **scribe** (Codex)
- **gate** (deterministic scripts, plus an OpenCode agent for natural-language rules)

## 2. Main flow: from mistake to binding rule

**F1. Task posted.** The reviewer posts a seeded task in the room: build a backtest ledger for strategy S1. Task prompt is plain; it does not mention trading costs.

**F2. Worker A submits.** worker-a posts a ledger. The seeded flaw: no 5 bps per-trade cost.

**F3. Reviewer rejects.** The reviewer replies "rejected: no transaction cost". This is the only human effort needed to teach the room.

**F4. Scribe drafts a rule.** The scribe posts a draft: what (apply 5 bps per trade on notional), why, scope (all backtest ledgers in this room), expiry, a passing example, a failing example, and the checker (`check_fees.py`).

**F5. Activation test.** *(Not implemented; §8.)* The harness runs the checker on the rule's passing and failing examples. If either behaves wrongly, the rule is not activated and the scribe is asked to fix it.

**F6. One-tap approval.** The reviewer approves. Switch logs a Decision; the rule is written to the room's Rules with status `active`.

**F7. Fresh worker B, different strategy.** worker-b gets strategy S2 with only the plain task prompt. It reads the room's active rules and applies the cost.

**F8. Gate check.** The gate runs every active rule against worker-b's ledger. Pass: the human sees it. Fail: it is returned to the worker with the failing rule id.

**F9. Paired ledgers shown.** Side by side: the ledger from an agent without the rule (missing $50 on $100,000 traded value) and the ledger with the rule. Both frozen before the gate ran.

**F10. Scoreboard.** Counts classified as worker-learned, gate-rescued and correct-without-rule.

## 3. Failure and recovery flow: the revoke ending (future work)

*Not implemented in the room. The gate has a local `--revoke BY` that writes status and an event; there is no in-chat `!revoke`.*

**F11. Wrong block.** A valid submission (for example an instrument the rule should not apply to) is blocked by a rule.

**F12. Revoke in chat.** Any teammate posts `!revoke R1` (VERIFY whether native or custom). The revoke is logged as a Decision.

**F13. Replay.** The exact blocked submission is replayed through the gate. It now passes.

**F14. Other rules still bite.** A submission that breaks a different active rule (R2, lookahead) is still blocked.

## 4. Side flows (future work, except expiry)

Expiry is implemented in `checkers/gate.py`: an expired rule returns `not_enforced`. Override and escalation are not implemented.

- **Override:** the reviewer overrides a gate block. The rule is flagged for review and its override count increases.
- **Escalation:** a natural-language rule yields `escalate`. The submission goes to the human, not auto-blocked or auto-passed.
- **Expiry:** an expired rule stops firing and is shown as `expired`; nothing is deleted.

## 5. Flow diagram (reference)

```
Task -> worker-a ledger -> Reviewer rejects -> scribe drafts rule
     -> activation test -> Reviewer approves (Decision + Rules)
     -> worker-b (new task) -> gate vs active rules
          pass -> Reviewer sees it
          fail -> back to worker with rule id
          escalate -> Reviewer decides
     -> wrong block -> !revoke -> replay -> passes -> R2 still blocks
```

## 6. Track 2 skin: Life Room (future work; not built)

Same engine, one extra template. Two friends and a planning agent plan a trip. The agent books a red-eye; one friend rejects; the scribe drafts "never book red-eyes"; approved as a Decision; a second agent then plans a different trip without red-eyes. Keep it to this one loop and do not build anything extra for it.

## 7. Demo timing (60 seconds)

- 0:00-0:10 F1-F3 (mistake and rejection)
- 0:10-0:25 F4-F6 (rule drafted, tested, approved)
- 0:25-0:40 F7-F10 (other-vendor agent applies it; paired ledgers; scoreboard)
- 0:40-0:55 F11-F14 (wrong block, revoke, replay, other rule still blocks)
- 0:55-1:00 one line on where Switch is central

No API keys or tokens on screen.

Current 90-second shot list: `DEMO.md`.

## 8. Future work

Moved here on 7 Nov 2026. Original wording kept.

- F5 activation test (§2 above).
- F6 native Switch Decision and Rules write (approval recorded as a chat reference only).
- F11 to F14 in-chat revoke, replay, and other rules still blocking (§3 above). R2 is a placeholder.
- Override and natural-language escalation (§4 above).
- Life Room (§6 above).
