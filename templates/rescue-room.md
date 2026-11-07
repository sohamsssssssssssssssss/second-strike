# Rescue room setup (Switch)

Room name: `rescue` (private).

Members:
- Soham (human reviewer): sends tasks, triggers the gate, is the only one who may revoke.
- `worker-b`: Codex gpt-6-luna. Instructions: base text in [worker-instructions.md](worker-instructions.md).
- `gate`: Codex. Instructions: [gate-agent-instructions.md](gate-agent-instructions.md). Working dir `<gate-dir>` holds a copy of `rules/R1.json` and `eval/`.

Room Instructions (R1, as approved in chat, message `dx95znbbq7dtixxhouksnsomnh`):

```text
Second Strike active custom rule R1: Every synthetic backtest trade in quant-desk must include fee = 0.0005 × qty × price (absolute tolerance 0.01). Scope is the per-trade fee field only; it does not validate net returns. Gate checks checkers/check_fees.py. Expires 2026-11-30T00:00:00+05:30. Approved by Soham in room chat; record is custom to this project, not a native Switch Rule or Decision. No secrets or real trades.
```

Task: paste `tasks/seeded/variant-0n.txt` verbatim, addressed to `@worker-b`. No hints.

Gate triggers (posted in the room):

| Message | Effect |
| --- | --- |
| `@gate check Vn attempt K` | Grade worker-b's latest reply for T-Vn, run `rescue`; on fail/escalate the gate mentions the worker with feedback |
| `@gate run RUN check Vn attempt K` | Same, logged under `eval/RUN/` (feedback to the worker only for `rescue` and `auto`) |
| `@gate revoke R1` | Human only. Runs `checkers/gate.py --revoke`; R1 then reports `not_enforced` |
| `@gate status R1` | Posts status, expiry, hits, last_fired, revoked fields |

Rules of the run: maximum 2 attempts per variant. The only feedback worker-b gets is gate output. The first reply per attempt is the record; nothing is edited or re-selected.

For the self-triggered loop (`quant-desk-live`, `eval/auto/`), append the auto-trigger line from [worker-instructions.md](worker-instructions.md) to the worker's instructions.
