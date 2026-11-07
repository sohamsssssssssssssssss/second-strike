# Autonomous run — 7 Nov 2026, 22:07–22:14 IST

Room `auto-run` (new): worker-b + gate, R1 in room Instructions. Human (Claude acting as reviewer) only sent the 5 frozen task prompts. No human ever mentioned @gate.
worker-b's instructions end with the auto-trigger line (templates/worker-instructions.md): after each ledger it posts "@gate run auto check Vn attempt K" itself. Gate instructions: templates/gate-agent-instructions.md.

## Result (report.md)
| Variant | Attempt 1 | Attempt 2 |
| --- | --- | --- |
| V1 | escalate | pass |
| V2 | pass | — |
| V3 | pass | — |
| V4 | pass | — |
| V5 | pass | — |

First-try pass 4/5; 5/5 after the gate loop. Every gate check (6) was triggered by worker-b, and the V1 resubmission was triggered by the gate's own mention of worker-b — a fully agent-to-agent loop in the Switch room.
Offline replay: all 6 hashes match log.jsonl; check_fees.py reproduces every verdict.

## Caveats
- worker-b's first tries now mostly include fees (4/5), unlike the earlier rescue run (0/5). worker-b had since received gate feedback and the schema prompt in other rooms; whether its Codex session carries that over is not known. Do not compare first-try rates across runs.
- The V1 first try had fees but no trade ids (escalate); the gate's feedback fixed it in one strike.
- Same worker, same model, n=5. Raw = text as the gate agent copied it.
- The earlier one-off smoke test (worker-a, chat revoke) is in eval/auto/.
