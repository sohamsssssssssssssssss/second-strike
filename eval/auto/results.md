# Live room smoke test — 7 Nov 2026, 21:42–21:45 IST

Room `quant-desk-live`: worker-a (Codex gpt-6.1-sol), worker-b (Codex gpt-6-luna), gate, human (Soham). R1 in room Instructions.
Worker instructions now end with: post "@gate run auto check Vn attempt K" after each ledger (templates/worker-instructions.md). Gate instructions: templates/gate-agent-instructions.md.

1. Human sent V1 to worker-a. worker-a posted a ledger, then itself posted "@gate run auto check V1 attempt 1" — no human trigger. Gate: pass (log.jsonl, raw/). worker-a included fees on its first try here; n=1, no claim.
2. Human sent "@gate revoke R1". Gate ran gate.py --revoke and posted {"rule_id":"R1","status":"revoked","by":"user"} (R1.revoked-test.json, events.jsonl).
3. R1 restored to active afterwards (from a backup taken before the revoke) for the demo recording.

Smoke test of the chat-native loop, not an experiment.
